#!/usr/bin/env python3
"""Bind the final deliverables to the reports that claim to describe them.

Run after the LAST change to the manuscript (including any P6/P7 repair and the
md/docx export). Checks, deterministically:

  F1  every defense-gate report (repeat --gate-json per format) was produced on a
      final manuscript (SHA-256 match) and states PASS or PASS_WITH_WARNINGS
  F2  every sibling-overlap report (if given) was produced on a final file and is
      not INCOMPLETE or MATCHES; a semantic-review file only proves the review was
      filed, not that it was done well
  F3  rrd_result.json (if given) records the same manuscript hashes and an
      explicit status; `sources_unchanged` is computed here, never assumed
  F4  every source listed in the manifest (path,sha256 CSV) still has its hash
  F5  the .md and .docx copies (if both given) carry the same visible prose

Usage:
    python final_check.py --manuscript FINAL.docx [--manuscript FINAL.md]
        --gate-json qa/defense_gate.json [--overlap-json qa/sibling_overlap.json]
        [--result-json rrd_result.json] [--source-manifest source_manifest.csv]
        --out-md qa/final_check.md [--out-json qa/final_check.json]
Exit code 0 when every applicable check passes, 2 otherwise.
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trace_scan  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prose(path: Path) -> str:
    return trace_scan.normalize(" ".join(p.text for p in trace_scan.load_paragraphs(path)))


def main() -> int:
    ap = argparse.ArgumentParser(description="Bind final manuscript, gate reports, result JSON and source hashes.")
    ap.add_argument("--manuscript", type=Path, action="append", required=True)
    ap.add_argument("--gate-json", type=Path, action="append", required=True, help="repeat for each gated format")
    ap.add_argument("--overlap-json", type=Path, action="append")
    ap.add_argument("--result-json", type=Path)
    ap.add_argument("--source-manifest", type=Path)
    ap.add_argument("--semantic-review", type=Path, help="required when the overlap report needs semantic review")
    ap.add_argument("--write-result", action="store_true",
                    help="write final_hashes, sources_unchanged and final_check status into --result-json before checking it")
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--out-json", type=Path)
    a = ap.parse_args()

    checks = []

    def rec(code, ok, detail):
        checks.append({"check": code, "status": "PASS" if ok else "FAIL", "detail": detail})

    finals = {}
    for m in a.manuscript:
        if not m.is_file():
            rec("F0_FILES", False, f"missing final manuscript {m}")
        else:
            finals[str(m.resolve())] = sha(m)
    hashes = set(finals.values())

    for gj in a.gate_json:
        if gj.is_file():
            g = json.loads(gj.read_text(encoding="utf-8"))
            gsha = (g.get("revised") or {}).get("sha256")
            rec("F1_GATE_BINDING", gsha in hashes, f"{gj.name}: gate revised sha {str(gsha)[:12]} {'matches' if gsha in hashes else 'does NOT match'} a final file")
            # a missing or unknown status is not a pass
            rec("F1_GATE_STATUS", g.get("overall") in {"PASS", "PASS_WITH_WARNINGS"}, f"{gj.name}: gate overall {g.get('overall')}")
        else:
            rec("F1_GATE_BINDING", False, f"gate report not found: {gj}")

    for oj in a.overlap_json or []:
        if oj.is_file():
            o = json.loads(oj.read_text(encoding="utf-8"))
            osha = o.get("manuscript_sha256")
            rec("F2_OVERLAP_BINDING", osha in hashes, f"overlap manuscript sha {str(osha)[:12]}")
            ov = o.get("overall")
            if ov == "SEMANTIC_REVIEW_REQUIRED":
                pending = [Path(s["file"]).stem for s in o.get("siblings", []) if s.get("status") == "SEMANTIC_REVIEW"]
                text = a.semantic_review.read_text(encoding="utf-8", errors="replace") if a.semantic_review and a.semantic_review.is_file() else ""
                unnamed = [p for p in pending if p[:20] not in text]
                ok_sem = bool(text) and not unnamed
                rec("F2_OVERLAP_STATUS", ok_sem, "semantic review required: " + (
                    f"{a.semantic_review.name} covers {len(pending)} sibling(s)" if ok_sem else
                    f"review missing or does not name: {unnamed or pending}"))
            else:
                rec("F2_OVERLAP_STATUS", ov == "CHECKED_NO_MATCH", f"overlap overall {ov}")
        else:
            rec("F2_OVERLAP_BINDING", False, f"overlap report not found: {oj}")

    sources_unchanged = None
    if a.source_manifest:
        if a.source_manifest.is_file():
            changed = []
            with a.source_manifest.open(encoding="utf-8-sig", newline="") as fh:
                for row in csv.DictReader(fh):
                    p = Path(row.get("path", ""))
                    if not p.is_file() or sha(p) != row.get("sha256", "").strip():
                        changed.append(str(p))
            sources_unchanged = not changed
            rec("F4_SOURCES", sources_unchanged, "all sources unchanged" if not changed else f"changed/missing: {changed[:10]}")
        else:
            rec("F4_SOURCES", False, f"manifest not found: {a.source_manifest}")

    if a.result_json:
        if a.result_json.is_file():
            r = json.loads(a.result_json.read_text(encoding="utf-8"))
            if a.write_result:
                r["final_hashes"] = {Path(k).name: v for k, v in finals.items()}
                if sources_unchanged is not None:
                    r["sources_unchanged"] = sources_unchanged
                a.result_json.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
            recorded = {v for k, v in (r.get("final_hashes") or {}).items()}
            rec("F3_RESULT_HASHES", bool(recorded) and recorded == hashes, "rrd_result final_hashes cover exactly the final files"
                if recorded == hashes else "rrd_result final_hashes missing, stale or incomplete (use --write-result)")
            status = r.get("status", "")
            rec("F3_RESULT_STATUS", bool(status), f"status '{status}'")
            if sources_unchanged is not None and r.get("sources_unchanged") is not None:
                rec("F3_RESULT_SOURCES", r.get("sources_unchanged") == sources_unchanged,
                    f"rrd_result sources_unchanged={r.get('sources_unchanged')} vs computed {sources_unchanged}")
        else:
            rec("F3_RESULT_HASHES", False, f"result JSON not found: {a.result_json}")

    mds = [m for m in a.manuscript if m.suffix.lower() in {".md", ".markdown"} and m.is_file()]
    docs = [m for m in a.manuscript if m.suffix.lower() == ".docx" and m.is_file()]
    if mds and docs:
        pm = [trace_scan.normalize(p.text) for p in trace_scan.load_paragraphs(mds[0])]
        pd = [trace_scan.normalize(p.text) for p in trace_scan.load_paragraphs(docs[0])]
        diff = [i for i, (x, y) in enumerate(zip(pm, pd), 1) if x != y]
        same = not diff and len(pm) == len(pd)
        detail = "prose paragraphs identical" if same else (
            f"{len(diff)} differing paragraphs (first at {diff[0] if diff else 'end'}); md {len(pm)} vs docx {len(pd)} paragraphs")
        rec("F5_COPY_PARITY", same, detail)

        def all_text(p: Path) -> str:
            if p.suffix.lower() == ".docx":
                import zipfile
                from xml.etree import ElementTree as ET
                W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
                root = ET.fromstring(zipfile.ZipFile(p).read("word/document.xml"))
                return trace_scan.normalize("".join(t.text or "" for t in root.iter(W + "t")))
            raw = p.read_text(encoding="utf-8", errors="replace")
            raw = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", "", raw)
            return trace_scan.normalize(re.sub(r"[#|*_`>-]", "", raw))

        full = difflib.SequenceMatcher(None, all_text(mds[0]), all_text(docs[0]), autojunk=False).ratio()
        checks.append({"check": "F5b_FULL_TEXT", "status": "INFO",
                       "detail": f"all visible text incl. tables, captions, references: similarity {round(full, 4)} (review if < 0.99)"})

    ok = all(c["status"] in {"PASS", "INFO"} for c in checks)
    out = {"overall": "PASS" if ok else "FAIL", "final_hashes": finals, "sources_unchanged": sources_unchanged, "checks": checks}
    if a.write_result and a.result_json and a.result_json.is_file():
        r = json.loads(a.result_json.read_text(encoding="utf-8"))
        r["final_check"] = out["overall"]
        a.result_json.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    md = [f"# Final binding check: {out['overall']}", "", "| check | status | detail |", "| --- | --- | --- |"]
    md += [f"| {c['check']} | {c['status']} | {c['detail']} |" for c in checks]
    md += ["", "Final hashes:"] + [f"- `{Path(k).name}` {v}" for k, v in finals.items()]
    a.out_md.parent.mkdir(parents=True, exist_ok=True)
    a.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    if a.out_json:
        a.out_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Final binding check: {out['overall']} -> {a.out_md}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
