#!/usr/bin/env python3
"""Build a chronological timeline of how a paper's target statements changed.

Walks a project root, finds manuscript-like and planning documents (.md,
.txt, .docx), and extracts the lines where authors or agents state the
paper's ambition: titles, research questions, core propositions,
contribution claims, "this paper argues/shows", positioning statements.
Output is a reading aid for Stage 1 retargeting: the human/agent still has to
read the earliest artifacts in full and judge what was lost and why.

Optionally runs trace_scan on every manuscript version so that drift in
defensiveness and living material across rounds becomes visible.

Usage:
    python target_drift_timeline.py --root PROJECT_ROOT --out-md timeline.md
        [--out-json timeline.json] [--exclude GLOB ...] [--max-lines-per-file 10]
        [--scan-manuscripts] [--manuscript-glob PATTERN ...]
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trace_scan  # noqa: E402

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TARGET_CUES = re.compile(
    r"(研究问题|核心问题|核心命题|核心论点|核心贡献|理论贡献|边际贡献|贡献在于|创新(点|之处)|本文(认为|提出|主张|发现|揭示|试图|旨在|挑战|回应)|"
    r"挑战了|修正了|突破|研究靶点|论文定位|主线|题名|题目|拟贡献|独立贡献|ambitious|"
    r"research question|core (claim|argument|proposition)|contribution|we argue|this (paper|article|study) "
    r"(argues|shows|challenges|proposes|contends)|thesis|novel|puzzle|we challenge)",
    re.I,
)
DEFAULT_EXCLUDES = [
    "*/.git/*", "*/node_modules/*", "*/__pycache__/*", "*/evidence/*", "*annotated*",
    "*/source_texts/*", "*/snapshots/*", "*/converted/*", "*参考文献*", "*/references/*",
]
NOT_MANUSCRIPT = re.compile(r"(template|prompt|goal|handoff|audit|report|register|ledger|plan|提示|模板|审计|报告)", re.I)
DEFAULT_MANUSCRIPT_GLOBS = ["*manuscript*clean*.md", "*manuscript*clean*.docx", "*draft*.md", "*正文*.md", "*稿*.docx"]


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        try:
            with zipfile.ZipFile(path) as z:
                root = ET.fromstring(z.read("word/document.xml"))
            return "\n".join("".join(t.text or "" for t in p.iter(W_NS + "t")) for p in root.iter(W_NS + "p"))
        except Exception as exc:  # noqa: BLE001
            return f"[unreadable docx: {exc}]"
    return path.read_text(encoding="utf-8", errors="replace")


DATE_IN_NAME = re.compile(r"(20\d{2})[-_.]?(0[1-9]|1[0-2])[-_.]?(0[1-9]|[12]\d|3[01])")


def infer_date(path: Path) -> tuple[str, str]:
    """Prefer a date written in the file or folder name; mtime is a weak fallback."""
    for part in [path.name, *[p.name for p in path.parents][:3]]:
        m = DATE_IN_NAME.search(part)
        if m:
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "name"
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="minutes"), "mtime (unreliable)"


def excluded(path: Path, patterns: list[str]) -> bool:
    s = str(path).replace("\\", "/")
    return any(fnmatch.fnmatch(s, p) for p in patterns)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract a dated timeline of target statements.")
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--out-json", type=Path)
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--max-lines-per-file", type=int, default=10)
    ap.add_argument("--max-bytes", type=int, default=3_000_000)
    ap.add_argument("--scan-manuscripts", action="store_true")
    ap.add_argument("--manuscript-glob", action="append", default=[])
    ap.add_argument("--file-list", type=Path, help="read only these files (one path per line, or a CSV with a 'path' column)")
    a = ap.parse_args()
    if not a.root.is_dir():
        ap.error(f"not a directory: {a.root}")
    excludes = DEFAULT_EXCLUDES + a.exclude
    m_globs = a.manuscript_glob or DEFAULT_MANUSCRIPT_GLOBS

    entries = []
    seen_hashes: set[str] = set()
    def walk(root: Path):
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not excluded(Path(dirpath) / d / "x", excludes)]
            for fn in filenames:
                yield Path(dirpath) / fn

    def listed():
        txt = a.file_list.read_text(encoding="utf-8-sig")
        if txt.lstrip().lower().startswith(("path,", "role,")):
            import csv as _csv
            for row in _csv.DictReader(txt.splitlines()):
                yield Path(row["path"]) if Path(row["path"]).is_absolute() else a.root / row["path"]
        else:
            for line in txt.splitlines():
                if line.strip():
                    yield Path(line.strip()) if Path(line.strip()).is_absolute() else a.root / line.strip()

    if a.file_list:
        excludes = a.exclude  # an explicit whitelist is authoritative; only user excludes apply
    skipped = []  # whitelisted files never drop out silently
    for path in (listed() if a.file_list else walk(a.root)):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".docx"}:
            if a.file_list:
                skipped.append((path, "missing" if not path.is_file() else f"unsupported type {path.suffix}"))
            continue
        if excluded(path, excludes):
            if a.file_list:
                skipped.append((path, "user --exclude"))
            continue
        # A .docx is mostly embedded images; its text is small, so the byte cap applies to plain text only.
        if path.suffix.lower() != ".docx" and path.stat().st_size > a.max_bytes:
            skipped.append((path, f"larger than --max-bytes {a.max_bytes}"))
            continue
        text = read_text(path)
        lines = []
        for raw in text.splitlines():
            line = raw.strip().lstrip("#>*- ").strip()
            if 8 <= len(line) <= 400 and TARGET_CUES.search(line):
                lines.append(line)
            if len(lines) >= a.max_lines_per_file:
                break
        is_ms = (any(fnmatch.fnmatch(path.name.lower(), g.lower()) for g in m_globs)
                 and not NOT_MANUSCRIPT.search(path.name))
        digest = hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
        if digest in seen_hashes:
            continue  # identical copy (bundles, portability checks) adds no timeline information
        seen_hashes.add(digest)
        if not lines and not is_ms:
            continue
        when, source = infer_date(path)
        entry = {"path": str(path), "date": when, "date_source": source,
                 "mtime": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="minutes"),
                 "is_manuscript": is_ms, "target_lines": lines}
        if is_ms and a.scan_manuscripts:
            try:
                r = trace_scan.scan(path)
                t = r["totals"]
                entry["signals"] = {k: t[k] for k in ["units", "process_trace", "negation_defense_per_k",
                                                       "negation_unanchored", "abstract_closer_share",
                                                       "quotes_per_k", "numbers_per_k", "abstract_terms_per_k", "stance"]}
            except Exception as exc:  # noqa: BLE001
                entry["signals"] = {"error": str(exc)}
        entries.append(entry)

    entries.sort(key=lambda e: (e["date"], e["mtime"]))
    md = [f"# Target drift timeline: {a.root}", "",
          "Reading aid only. Open the earliest artifacts in full before reconstructing the original target; "
          "an extracted line is not the author's intention by itself. Order uses dates written in file or folder "
          "names when present; otherwise file modification time, which copying or syncing can change - confirm "
          "the version history with the author when it matters. Interview transcripts and field notes carry the "
          "date of the material, not of a target statement; do not read them as versions.", ""]
    if skipped:
        md += ["## Files not read", ""] + [f"- {p} - {why}" for p, why in skipped] + [""]
    scanned = [e for e in entries if e.get("signals") and "error" not in e["signals"]]
    if scanned:
        md += ["## Manuscript signal trajectory", "",
               "| date (source) | file | units | trace | neg/k | unanch. | closer share | quotes/k | numbers/k | abstract/k | stance |",
               "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for e in scanned:
            s = e["signals"]
            try:
                rel = Path(e["path"]).relative_to(a.root)
            except ValueError:
                rel = Path(e["path"])
            md.append(f"| {e['date']} ({e['date_source'][:5]}) | {rel} | {s['units']} | {s['process_trace']} | {s['negation_defense_per_k']} | "
                      f"{s['negation_unanchored']} | {s['abstract_closer_share']} | {s['quotes_per_k']} | "
                      f"{s['numbers_per_k']} | {s['abstract_terms_per_k']} | {s['stance']} |")
        md.append("")
    md += ["## Target statements by date", ""]
    for e in entries:
        if not e["target_lines"]:
            continue
        try:
            rel = Path(e["path"]).relative_to(a.root)
        except ValueError:
            rel = Path(e["path"])
        md += [f"### {e['date']} ({e['date_source']}) · {rel}{' (manuscript)' if e['is_manuscript'] else ''}", ""]
        md += [f"- {ln}" for ln in e["target_lines"]] + [""]
    a.out_md.parent.mkdir(parents=True, exist_ok=True)
    a.out_md.write_text("\n".join(md), encoding="utf-8")
    if a.out_json:
        a.out_json.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(entries)} dated entries ({len(scanned)} scanned manuscripts); {len(skipped)} files not read -> {a.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
