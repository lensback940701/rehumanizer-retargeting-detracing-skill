#!/usr/bin/env python3
"""Check a manuscript's direct quotations against sibling papers from the same dataset.

Many projects publish several papers from one fieldwork corpus. Re-using a
different statement by the same informant is normally fine; re-quoting the
same sentence that a sibling paper already used is not. This script finds:

  EXACT  the manuscript quote (normalized) occurs verbatim in a sibling text
  NEAR   a long common stretch covers >= --near-threshold of the quote
  CROSS_LANGUAGE  the sibling is in another language: string matching cannot
         decide; the sibling's own quotations are listed for semantic review

Overlap of *findings* (the same argument made with different quotes) is not
detectable by string matching; read the sibling's listed quotes and claims.

Usage:
    python sibling_overlap_check.py --manuscript M.docx --sibling A.md --sibling B.docx
        [--near-threshold 0.6] --out-md overlap.md [--out-json overlap.json]
Exit codes:
  0  every sibling CHECKED_NO_MATCH
  2  at least one EXACT/NEAR match
  3  no string match, but some siblings need SEMANTIC_REVIEW (other language)
  1  INCOMPLETE: a sibling was missing or unreadable (never reported as success)
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trace_scan  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ZH_Q = re.compile(r"“([^”]{8,})”")
EN_Q = re.compile(r"[“\"]([^”\"]{25,})[”\"]")


def read_any(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        root = ET.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
        return "\n".join("".join(t.text or "" for t in p.iter(W + "t")) for p in root.iter(W + "p"))
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader  # optional dependency
        except ImportError:
            return ""
        return "\n".join(pg.extract_text() or "" for pg in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="replace")


def lang_of(text: str) -> str:
    sample = text[:20000]
    return "zh" if sample and len(re.findall(r"[一-鿿]", sample)) / max(1, len(sample)) > 0.15 else "en"


def manuscript_quotes(path: Path) -> list[dict]:
    paras = trace_scan.load_paragraphs(path)
    lang = trace_scan.detect_lang(paras)
    out = []
    for p in paras:
        if trace_scan.is_block_quote(p.text):
            out.append({"section": p.section, "quote": p.text, "kind": "block"})
            continue
        long_q = (ZH_Q if lang == "zh" else EN_Q).findall(p.text)
        for q in long_q:
            out.append({"section": p.section, "quote": q, "kind": "inline"})
        # short sourced quotations fall under the length threshold; list them and check exact reuse only
        for q in trace_scan.sourced_quotes(p.text, lang):
            if q not in long_q and not any(q in x for x in long_q):
                out.append({"section": p.section, "quote": q, "kind": "short"})
    return out


REF_HEAD = re.compile(r"\n\s*(#+\s*)?(\d+\.?\s*)?(参考文献|references|bibliography|works cited)\s*\n", re.I)


def body_only(text: str) -> str:
    """Cut the reference list so cited titles are not mistaken for quotations."""
    m = None
    for m in REF_HEAD.finditer(text):
        pass
    return text[:m.start()] if m and m.start() > len(text) * 0.4 else text


def sibling_quotes(text: str, lang: str) -> list[str]:
    text = body_only(text)
    found = [q for q in (ZH_Q if lang == "zh" else EN_Q).findall(text) if "\n" not in q and len(q) <= 400 and q.count(". ") <= 6]
    blocks = re.findall(r"\n([^\n]{60,900}[（(](?:Interview|interview|访谈)[^)）]{0,40}[)）])", text)
    return found + blocks


def main() -> int:
    ap = argparse.ArgumentParser(description="Find re-used quotations across sibling papers.")
    ap.add_argument("--manuscript", type=Path, required=True)
    ap.add_argument("--sibling", type=Path, action="append", required=True)
    ap.add_argument("--near-threshold", type=float, default=0.6)
    ap.add_argument("--out-md", type=Path, required=True)
    ap.add_argument("--out-json", type=Path)
    a = ap.parse_args()

    quotes = manuscript_quotes(a.manuscript)
    m_lang = lang_of(" ".join(q["quote"] for q in quotes) or read_any(a.manuscript))
    report = {"manuscript": str(a.manuscript),
              "manuscript_sha256": hashlib.sha256(a.manuscript.read_bytes()).hexdigest(),
              "quotes": len(quotes), "siblings": []}
    flagged = 0
    for sib in a.sibling:
        if not sib.is_file():
            report["siblings"].append({"file": str(sib), "status": "INCOMPLETE_NOT_FOUND", "matches": []})
            continue
        text = body_only(read_any(sib))
        s_lang = lang_of(text)
        entry = {"file": str(sib), "lang": s_lang, "matches": [], "status": "CHECKED_NO_MATCH",
                 "sha256": hashlib.sha256(sib.read_bytes()).hexdigest()}
        if not text.strip():
            entry["status"] = "INCOMPLETE_UNREADABLE"
        elif s_lang != m_lang:
            entry["status"] = "SEMANTIC_REVIEW"
            entry["sibling_quotes"] = sibling_quotes(text, s_lang)
        else:
            norm_text = trace_scan.normalize(text)
            for q in quotes:
                nq = trace_scan.normalize(q["quote"])
                if len(nq) < 4:
                    continue
                if nq in norm_text:
                    entry["matches"].append({"type": "EXACT", "quote": q["quote"][:200], "section": q["section"]})
                    continue
                if q["kind"] == "short" or len(nq) < 6:
                    continue  # near-matching very short strings is noise
                sm = difflib.SequenceMatcher(None, nq, norm_text, autojunk=False)
                lm = sm.find_longest_match(0, len(nq), 0, len(norm_text))
                if lm.size / len(nq) >= a.near_threshold:
                    ctx = norm_text[lm.b:lm.b + lm.size]
                    entry["matches"].append({"type": "NEAR", "coverage": round(lm.size / len(nq), 2),
                                             "quote": q["quote"][:200], "section": q["section"], "shared": ctx[:120]})
        if entry["matches"]:
            entry["status"] = "MATCHES"
        flagged += len(entry["matches"])
        report["siblings"].append(entry)

    md = [f"# Sibling overlap check: {a.manuscript.name}", "",
          f"- manuscript quotations checked: {len(quotes)} · EXACT/NEAR flags: {flagged}",
          f"- short quotations (exact reuse only; include them in any semantic review): "
          + ("; ".join(q["quote"] for q in quotes if q["kind"] == "short") or "none"),
          "- A different statement by the same informant is not a duplicate. Finding-level overlap "
          "(same argument, different quote) needs a human read of the sibling's claims.", ""]
    for e in report["siblings"]:
        md.append(f"## {Path(e['file']).name} - {e['status']}{' (' + e.get('lang', '') + ')' if e.get('lang') else ''}")
        md.append("")
        for m in e.get("matches", []):
            md.append(f"- **{m['type']}**{' ' + str(m.get('coverage')) if m.get('coverage') else ''} · {m['section']}: {m['quote']}")
        if e["status"] == "SEMANTIC_REVIEW":
            md.append(f"Semantic review needed. Sibling quotations ({len(e['sibling_quotes'])}):")
            md += [f"- {q}" for q in e["sibling_quotes"]]
        if e["status"] == "CHECKED_NO_MATCH":
            md.append("- no EXACT/NEAR matches")
        md.append("")
    a.out_md.parent.mkdir(parents=True, exist_ok=True)
    a.out_md.write_text("\n".join(md), encoding="utf-8")
    statuses = {e["status"] for e in report["siblings"]}
    report["overall"] = ("MATCHES" if flagged else
                         "INCOMPLETE" if any(s.startswith("INCOMPLETE") for s in statuses) else
                         "SEMANTIC_REVIEW_REQUIRED" if "SEMANTIC_REVIEW" in statuses else "CHECKED_NO_MATCH")
    if a.out_json:
        a.out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(quotes)} quotations; {flagged} EXACT/NEAR flags; overall {report['overall']} -> {a.out_md}")
    return {"MATCHES": 2, "INCOMPLETE": 1, "SEMANTIC_REVIEW_REQUIRED": 3, "CHECKED_NO_MATCH": 0}[report["overall"]]


if __name__ == "__main__":
    raise SystemExit(main())
