#!/usr/bin/env python3
"""Extract accumulated writing/process constraints ("rule debt") from prior
Goals, prompts, control files and style cards.

Long multi-round revision pipelines tend to stack prohibitions (quote freezes,
anchor-only evidence, naming codes, net-word-loss thresholds, per-sentence
verification) until the prose can only become flat. This script lists every
constraint-bearing sentence so Stage 1 can classify each as RETAIN, RELAX or
RETIRE with the author. It suggests a family and a default, never a decision.

Usage:
    python rule_debt_extract.py INPUT [INPUT ...] --out-csv rule_debt_register.csv [--out-md summary.md]
INPUT may be a file or a directory (scans .md/.txt/.json/.yaml recursively).
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path

CONSTRAINT = re.compile(
    r"(不得|不能|不要|禁止|不新增|不再|不可|只能|仅限|仅可|必须|须|一律|不允许|避免|严禁|不应|保留.{0,6}逐字|不改|不变|固定|锁定|保持不变|原样|"
    r"\bmust\b|\bmust not\b|\bdo not\b|\bdon't\b|\bnever\b|\bonly\b|\bshall not\b|\bprohibit|\bforbid|\brequired?\b)",
    re.I,
)
FAMILIES = [
    ("ETHICS_PRIVACY", r"(匿名|真名|实名|隐私|伦理|知情同意|consent|anonym|privacy|ethic|confidential)"),
    ("SOURCE_PROTECTION", r"(原件|源稿|基线|baseline|hash|哈希|覆盖|overwrite|不得修改|rename|删除原)"),
    ("FACT_INTEGRITY", r"(捏造|编造|补造|虚构|强造|无据|推定|补出|fabricat|invent|伪造|不存在的|unsupported)"),
    ("QUALITY_TARGET", r"(泛词|通用|泛化|复述|罗列|重复|空泛|generic|repeat|restate|boilerplate)"),
    ("QUOTE", r"(引语|引文|直接引|原话|quote|quotation)"),
    ("EVIDENCE_ADMISSION", r"(证据|锚点|准入|核验|核实|台账|evidence|anchor|admission|verify|locator)"),
    ("NAMING", r"(代称|编号|称谓|角色|人名|naming|code|pseudonym)"),
    ("LENGTH", r"(字数|篇幅|净减|压缩|上限|word|length|cap\b|budget)"),
    ("CLAIM_STRENGTH", r"(论断|主张|上限|不扩大|不增强|外推|因果|claim|ceiling|overclaim|causal|generali)"),
    ("STYLE_LOCK", r"(措辞|句式|段落|风格|模板|段首|段末|表述|wording|style|template|sentence|paragraph)"),
    ("STRUCTURE_LOCK", r"(章节|小节|标题|结构|顺序|section|heading|order|structure)"),
    ("PROCESS", r"(逐句|逐段|逐条|每一?(句|段|节)|每次|批准|确认|请示|gate|approval|pass|阶段)"),
    ("LITERATURE", r"(文献|引用|参考|citation|reference|literature)"),
]
DEFAULT_DISPOSITION = {
    "ETHICS_PRIVACY": "RETAIN", "SOURCE_PROTECTION": "RETAIN", "FACT_INTEGRITY": "RETAIN",
    "QUALITY_TARGET": "CONVERT_TO_POSITIVE_GOAL",
}


SKIP_PARTS = {"scans", "evidence", "annotated_interviews", "annotated_literature", "source_texts", "converted",
              "corpus", "work", "working", "figure", "manuscripts", "registers"}


def source_role(path: Path) -> str:
    name = path.as_posix().lower()
    if re.search(r"author_(queries|decisions)|作者决定|author_memo", name):
        return "author_decision"
    if "/qa/" in name or name.endswith(".json"):
        return "machine_suggestion"
    if re.search(r"goal|prompt|handoff|style_card|skill|guardrail|section_goals", name):
        return "instruction"
    return "other"


def iter_files(inputs: list[Path]):
    for p in inputs:
        if p.is_dir():
            for f in p.rglob("*"):
                if any(part.lower() in SKIP_PARTS for part in f.relative_to(p).parts[:-1]):
                    continue
                if f.is_file() and f.suffix.lower() in {".md", ".txt", ".yaml", ".yml"}:
                    yield f  # JSON/CSV in a directory are machine records, not rules; pass them explicitly if needed
        elif p.is_file():
            yield p


def split_units(text: str):
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip().lstrip("-*>#0123456789.、) ").strip()
        if not line:
            continue
        for piece in re.split(r"(?<=[。；;!！?？])", line):
            piece = piece.strip()
            if 6 <= len(piece) <= 400:
                yield line_no, piece


def main() -> int:
    ap = argparse.ArgumentParser(description="List accumulated constraints for RETAIN/RELAX/RETIRE review.")
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--out-md", type=Path)
    a = ap.parse_args()

    rows, seen = [], set()
    for f in iter_files(a.inputs):
        text = f.read_text(encoding="utf-8", errors="replace")
        for line_no, unit in split_units(text):
            if not CONSTRAINT.search(unit):
                continue
            quoted = sum(len(q) for q in re.findall(r"“[^”]*”|\"[^\"]*\"", unit))
            if quoted > len(unit) * 0.5 or re.search(r"[（(][A-Z]{1,3}\d{1,3}[，,]\s*\d{4}[）)]", unit):
                continue  # interview speech or quoted source text, not an instruction
            key = re.sub(r"\W+", "", unit.lower())[:80]
            if key in seen:
                continue
            seen.add(key)
            fams = [name for name, rx in FAMILIES if re.search(rx, unit, re.I)]
            family = fams[0] if fams else "OTHER"
            rows.append({
                "rule_id": f"R{len(rows) + 1:03d}", "source_file": str(f), "source_role": source_role(f), "line": line_no,
                "text": unit, "family": family, "other_families": "|".join(fams[1:]),
                "suggested_default": DEFAULT_DISPOSITION.get(family, "REVIEW"),
                "disposition": "", "rationale": "", "author_confirmed": "",
            })
    a.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with a.out_csv.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["rule_id"])
        w.writeheader()
        w.writerows(rows)
    fam = Counter(r["family"] for r in rows)
    if a.out_md:
        md = ["# Rule debt summary", "",
              f"{len(rows)} constraint sentences from {len({r['source_file'] for r in rows})} files.", "",
              "| family | count | default |", "| --- | --- | --- |"]
        for k, v in fam.most_common():
            md.append(f"| {k} | {v} | {DEFAULT_DISPOSITION.get(k, 'REVIEW')} |")
        md += ["", "Classify each row RETAIN / RELAX / RETIRE / CONVERT_TO_POSITIVE_GOAL. Ethics, privacy, source protection and "
               "fact integrity stay RETAIN. Style, process, naming, quote-freeze and length locks inherited "
               "from earlier rounds are the usual causes of mechanical prose and need an explicit decision."]
        a.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(rows)} constraints -> {a.out_csv}; families: {dict(fam.most_common())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
