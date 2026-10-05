#!/usr/bin/env python3
"""Anti-over-defence regression gate for a route-corrected manuscript (v2).

Compares BASELINE (pre-route-correction draft) with REVISED, optionally against
VOICE REFERENCES (the author's published papers or chosen exemplars).

Hard checks (exit code 2 on FAIL) - things that are wrong regardless of style:
  G0_INPUT     revised and baseline are readable and not truncated
  G0_REGISTER  every register row is well formed (enumerated cue type,
               resolvable locator, specific non-generic reason)
  G1_TRACE     no workflow/audit trace in prose (verification facts inside a
               methods section are reported as a warning instead)
  G2_NEW_CUES  every hedge / negation-defence / hedged-finding cue that is new
               relative to the matching baseline sentence (or appears in a new
               sentence) is registered with a matching cue type
  G6_LOSS      sourced quotations present in the baseline and absent from the
               revision are accounted for in the route memo (FAIL only when a
               memo is supplied and omits them; otherwise a warning)

Warnings - densities and style signals are alarms, never quotas:
  W1 actor codes, W2 abstract fog, W3 negation density, W4 unanchored negation,
  W5 restating / aphoristic closers, W6 living-material density, W7 trace cues
  in methods, W8 cohesion (topic linkage, sentence length, staccato runs,
  attribution clutter), W9 stance, W10 caveat budget, W11 literature chains,
  W12 voice drift, W0 scan reliability.

Registered (accepted) cautions are exempt from every count they appear in.
A PASS is necessary, never sufficient: the semantic cold read stays mandatory.
Never fix a FAIL by editing the config; the config SHA-256 is recorded.

Usage:
    python defense_gate.py --baseline B --revised R [--reference REF ...]
        [--register added_caution_register.csv] [--route-memo route_memo.md]
        [--config gate_config.json] [--paper-type qualitative|quantitative|mixed|theoretical]
        --out-json OUT.json --out-md OUT.md
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

DEFAULT_CONFIG = {
    "carried_sentence_similarity": 0.80,
    "min_revised_share_of_baseline": 0.30,
    "negation_min_reduction": 0.30,
    "negation_floor_per_k": {"zh": 0.40, "en": 2.50},
    "closer_share_warn": 0.20,
    "code_tokens_warn_per_k": 3.0,
    "abstract_terms_min_reduction": 0.15,
    "caveat_share_warn": 0.25,
    "lit_chain_warn_share": 0.35,
    "topic_link_tolerance": 0.05,
    "sentence_length_ratio_warn": 0.80,
    "attribution_ratio_warn": 1.20,
    "epigram_closers_warn": 2,
    "conversion_frame_warn": 0.05,
    "relation_verb_floor_per_k": {"zh": 1.5, "en": 1.5},
    "tag_word_min_count": 10,
    "tag_word_min_spread": 0.45,
    "tag_word_base_ratio": 2.0,
    "tag_word_ref_ratio": 3.0,
    "relation_verb_ref_ratio": 3.0,
    "inferential_floor_per_k": {"zh": 1.2, "en": 2.0},
    "inferential_ref_ratio": 2.0,
    "min_reason_chars": 12,
    "generic_reason_blacklist": [
        "谨慎起见", "为谨慎", "保险起见", "避免过度", "避免夸大", "严谨起见", "更严谨", "稳妥",
        "以防", "防止审稿", "审稿人可能", "for caution", "to be safe", "to be cautious",
        "avoid overclaim", "reviewer might", "just in case", "for rigor", "safer",
    ],
}
CUE_TYPES = {"HEDGE": "hedge", "NEGATION": "negation_defense", "HEDGED_FINDING": "hedged_finding",
             "PROCESS_TRACE_KEEP": "process_trace"}
DEFENSIVE = ("hedge", "negation_defense", "hedged_finding")
SECTION_ALIASES = {
    "abstract": re.compile(r"(摘要|abstract)", re.I),
    "conclusion": re.compile(r"(结论|conclusion|结语|concluding)", re.I),
    "intro": re.compile(r"(引言|导言|introduction|^前言)", re.I),
    "discussion": re.compile(r"(讨论|discussion)", re.I),
    "theory": re.compile(r"(理论|文献|framework|literature|theor|分析框架|研究综述)", re.I),
    "methods": re.compile(r"(方法|材料|数据|资料来源|研究设计|methods?|methodology|data|materials|research design)", re.I),
}
VERIFICATION_FACT = re.compile(r"(核对|核实|核验|复核|verified|checked)", re.I)
LOCATOR_OK = re.compile(r"(\d|term-of-art|[A-Za-z]{1,6}\d)", re.I)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text: str) -> str:
    return trace_scan.normalize(text)


def buckets(section: str, chapter: str = "") -> set[str]:
    label = f"{section} {chapter}"
    return {k for k, rx in SECTION_ALIASES.items() if rx.search(label)}


def best_match(sentence: str, baseline: list[tuple[str, dict]], threshold: float):
    """Locate the corresponding baseline sentence; similarity only finds the pair."""
    n = norm(sentence)
    best, best_ratio = None, 0.0
    for b_norm, rec in baseline:
        if n == b_norm:
            return rec, 1.0
        sm = difflib.SequenceMatcher(None, n, b_norm, autojunk=False)
        if sm.real_quick_ratio() < threshold or sm.quick_ratio() < threshold:
            continue
        r = sm.ratio()
        if r > best_ratio:
            best, best_ratio = rec, r
    return (best, best_ratio) if best_ratio >= threshold else (None, best_ratio)


def load_register(path: Path | None, cfg: dict):
    if not path:
        return [], []
    if not path.is_file():
        return [], [f"register not found: {path}"]
    rows, problems = [], []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            excerpt = norm(row.get("sentence_excerpt", ""))
            cue = (row.get("cue_type") or "").strip().upper()
            locator = (row.get("evidence_locator") or "").strip()
            reason = (row.get("why_reader_needs_it") or "").strip()
            bad = []
            if len(excerpt) < 8:
                bad.append("sentence_excerpt shorter than 8 normalized characters")
            if cue not in CUE_TYPES:
                bad.append(f"cue_type must be one of {sorted(CUE_TYPES)}")
            if len(locator) < 4 or not LOCATOR_OK.search(locator):
                bad.append("evidence_locator must name a resolvable source position (ID/page/paragraph/timestamp) or 'term-of-art'")
            if len(reason) < cfg["min_reason_chars"]:
                bad.append("why_reader_needs_it too short")
            if any(g.lower() in reason.lower() for g in cfg["generic_reason_blacklist"]):
                bad.append("generic precautionary reason (blacklisted)")
            if bad:
                problems.append(f"register row {i}: " + "; ".join(bad))
                continue
            rows.append({"excerpt": excerpt, "kind": CUE_TYPES[cue], "locator": locator})
    return rows, problems


def registered(sentence: str, rows: list[dict], kinds: set[str] | None = None) -> bool:
    n = norm(sentence)
    return any(r["excerpt"] in n and (kinds is None or r["kind"] in kinds) for r in rows)


def quotes_of(scan: dict) -> list[str]:
    return list(scan.get("sourced_quotations", []))


def mean_sentence_length(scan: dict) -> float:
    return scan.get("sentence_length", {}).get("mean", 0) or 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Anti-over-defence regression gate (hard checks + warnings).")
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--revised", type=Path, required=True)
    ap.add_argument("--reference", type=Path, action="append", default=[])
    ap.add_argument("--register", type=Path)
    ap.add_argument("--route-memo", type=Path)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--core-term", action="append", default=[],
                    help="the paper's own concept terms from the route contract; exempt from W17 tag-word checks (title and keywords are exempt automatically)")
    ap.add_argument("--paper-type", choices=["qualitative", "quantitative", "mixed", "theoretical"], default="qualitative")
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto")
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    a = ap.parse_args()

    results: list[dict] = []

    def record(code, status, detail, items=None):
        items = list(items or [])
        results.append({"check": code, "status": status, "detail": detail, "items": items[:60], "item_count": len(items)})

    cfg = dict(DEFAULT_CONFIG)
    cfg_hash = "builtin-defaults"
    if a.config and a.config.is_file():
        cfg.update(json.loads(a.config.read_text(encoding="utf-8")))
        cfg_hash = sha256(a.config)

    def finish(base=None, rev=None, refs=()):
        fails = [r for r in results if r["status"] == "FAIL"]
        warns = [r for r in results if r["status"] == "WARN"]
        overall = "FAIL" if fails else ("PASS_WITH_WARNINGS" if warns else "PASS")
        report = {
            "overall": overall,
            "baseline": {"file": str(a.baseline), "sha256": sha256(a.baseline) if a.baseline.is_file() else None,
                         "totals": base["totals"] if base else None},
            "revised": {"file": str(a.revised), "sha256": sha256(a.revised) if a.revised.is_file() else None,
                        "totals": rev["totals"] if rev else None},
            "references": [{"file": r["file"], "totals": r["totals"]} for r in refs],
            "register": {"file": str(a.register), "sha256": sha256(a.register)} if a.register and a.register.is_file() else None,
            "route_memo": {"file": str(a.route_memo), "sha256": sha256(a.route_memo)} if a.route_memo and a.route_memo.is_file() else None,
            "config_sha256": cfg_hash, "paper_type": a.paper_type, "checks": results,
            "note": "Necessary, not sufficient. Densities are alarms, not quotas. Fix a FAIL by rewriting prose or by a "
                    "specific register/memo entry, never by editing this config.",
        }
        a.out_json.parent.mkdir(parents=True, exist_ok=True)
        a.out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        md = [f"# Defense gate: {overall}", "",
              f"- baseline: `{a.baseline.name}` · revised: `{a.revised.name}` "
              f"(sha256 {(report['revised']['sha256'] or 'n/a')[:12]}) · references: {len(refs)} · "
              f"paper type: {a.paper_type} · config: {cfg_hash[:12]}",
              "- Necessary, not sufficient: the semantic cold read remains mandatory.", "",
              "| check | status | detail |", "| --- | --- | --- |"]
        md += [f"| {r['check']} | {r['status']} | {r['detail']} |" for r in results]
        for r in results:
            if r["items"]:
                more = f" (showing {len(r['items'])} of {r['item_count']})" if r["item_count"] > len(r["items"]) else ""
                md += ["", f"## {r['check']} ({r['status']}){more}", ""] + [f"- {x}" for x in r["items"]]
        a.out_md.parent.mkdir(parents=True, exist_ok=True)
        a.out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"Defense gate: {overall} ({len(fails)} fail, {len(warns)} warn). Report: {a.out_md}")
        return 2 if fails else 0

    missing = [str(p) for p in [a.baseline, a.revised, *a.reference] if not p.is_file()]
    if missing:
        record("G0_INPUT", "FAIL", "input file(s) not found", missing)
        return finish()
    try:
        base = trace_scan.scan(a.baseline, a.lang)
        rev = trace_scan.scan(a.revised, a.lang if a.lang != "auto" else base["lang"])
        all_refs = [trace_scan.scan(r, "auto") for r in a.reference]
        refs = [r for r in all_refs if r["lang"] == base["lang"]]
        for r in all_refs:
            if r["lang"] != base["lang"]:
                results.append({"check": "W0_SCAN_RELIABILITY", "status": "WARN", "item_count": 0, "items": [],
                                 "detail": f"reference {Path(r['file']).name} is {r['lang']}, manuscript is {base['lang']}: excluded from comparisons"})
    except SystemExit as exc:
        record("G0_INPUT", "FAIL", f"unreadable input: {exc}")
        return finish()
    B, R = base["totals"], rev["totals"]

    problems = []
    if B["units"] == 0:
        problems.append("baseline has no readable prose")
    if R["units"] == 0 or R["sentences"] == 0:
        problems.append("revised has no readable prose")
    elif B["units"] and R["units"] < cfg["min_revised_share_of_baseline"] * B["units"]:
        problems.append(f"revised prose is {R['units']} units vs baseline {B['units']}: probably truncated or mis-parsed")
    if R["units"] and rev["lang"] != base["lang"]:
        problems.append(f"language mismatch: baseline {base['lang']} vs revised {rev['lang']}")
    record("G0_INPUT", "FAIL" if problems else "PASS", "input problem" if problems else "inputs readable and complete", problems)
    if problems:
        return finish(base, rev, refs)

    reg_rows, reg_problems = load_register(a.register, cfg)
    if reg_problems:
        record("G0_REGISTER", "FAIL", "invalid register rows are ignored, not accepted", reg_problems)

    para_ok = [r for r in refs if not any("merged" in w for w in r.get("reliability_warnings", []))]

    def ref_mean(key, paragraph_level=False):
        pool = para_ok if paragraph_level else refs
        vals = [r["totals"][key] for r in pool]
        return round(sum(vals) / len(vals), 3) if vals else None

    # G1 workflow traces over the full candidate list
    traces = [c for c in rev["candidates"] if c["type"] == "process_trace"
              and not registered(c["excerpt"], reg_rows, {"process_trace"})]
    method_facts = [c for c in traces if "methods" in buckets(c["section"], c.get("chapter", ""))
                    and VERIFICATION_FACT.search(c.get("cue", ""))]
    hard = [c for c in traces if c not in method_facts]
    record("G1_TRACE", "FAIL" if hard else "PASS",
           f"{len(hard)} unregistered workflow/audit traces in prose (baseline total {B['process_trace']}).",
           [f"{c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in hard])
    if method_facts:
        record("W7_METHODS_TRACE", "WARN", "verification cues inside methods: keep genuine method facts once; delete handling notes.",
               [f"{c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in method_facts])

    # G2 new defensive cues, diffed against the matching baseline sentence
    base_index = [(norm(s["sentence"]), s) for s in base["sentences"]]
    new_items, exempt = [], set()
    for s in rev["sentences"]:
        kinds = [k for k in DEFENSIVE if k in s["flags"]]
        if not kinds:
            continue
        if registered(s["sentence"], reg_rows, set(kinds)):
            exempt.add(norm(s["sentence"]))
        match, _ = best_match(s["sentence"], base_index, cfg["carried_sentence_similarity"])
        new_cues = {}
        for k in kinds:
            before = set(match.get("cues", {}).get(k, [])) if match else set()
            added = [c for c in s.get("cues", {}).get(k, []) if c not in before]
            if added:
                new_cues[k] = added
        if not new_cues or registered(s["sentence"], reg_rows, set(new_cues)):
            continue
        where = "carried sentence" if match else "new sentence"
        head = " [ABSTRACT/CONCLUSION]" if {"abstract", "conclusion"} & buckets(s["section"], s.get("chapter", "")) else ""
        cue_txt = "; ".join(f"{k}: {', '.join(v)}" for k, v in new_cues.items())
        new_items.append(f"{s['section']} ¶{s['paragraph']}{head} ({where}; {cue_txt}): {s['sentence'][:200]}")
    record("G2_NEW_CUES", "FAIL" if new_items else "PASS",
           f"{len(new_items)} sentences add hedge/negation/hedged-finding cues without a matching register entry. "
           "Rewrite as a standing claim, or register the caution with its evidence locator and reader need.", new_items)

    # G6 sourced quotation loss: function-level accounting, not density
    rev_norm = norm(" ".join(s["sentence"] for s in rev["sentences"]))
    lost = [q for q in quotes_of(base) if norm(q)[:16] and norm(q)[:16] not in rev_norm]
    if not lost:
        record("G6_LOSS", "PASS", "no baseline quotation removed")
    elif a.route_memo and a.route_memo.is_file():
        memo = norm(a.route_memo.read_text(encoding="utf-8", errors="replace"))

        def documented(q: str) -> bool:
            nq = norm(q)
            windows = [nq[i:i + 8] for i in range(0, max(1, len(nq) - 7), 4)]
            return any(w and w in memo for w in windows)

        unexplained = [q for q in lost if not documented(q)]
        record("G6_LOSS", "FAIL" if unexplained else "PASS",
               f"{len(lost)} baseline quotations absent from the revision; {len(unexplained)} not accounted for in the route memo "
               "(name each removed quotation and why, or restore it).", [q[:120] for q in unexplained])
    else:
        record("G6_LOSS", "WARN", f"{len(lost)} baseline quotations absent; supply --route-memo that accounts for them.",
               [q[:120] for q in lost])

    # ---------------- warnings
    def per_k_excluding(flag: str, scan: dict) -> float:
        n = sum(1 for s in scan["sentences"] if flag in s["flags"] and norm(s["sentence"]) not in exempt)
        return round(1000 * n / scan["totals"]["units"], 2) if scan["totals"]["units"] else 0.0

    lang = base["lang"]
    floor_cfg = cfg["negation_floor_per_k"]
    floor = floor_cfg.get(lang, 0) if isinstance(floor_cfg, dict) else floor_cfg
    b_neg, r_neg = B["negation_defense_per_k"], per_k_excluding("negation_defense", rev)
    target = b_neg if b_neg <= floor else b_neg * (1 - cfg["negation_min_reduction"])
    ref_neg = ref_mean("negation_defense_per_k")
    if ref_neg is not None:
        target = max(target, min(b_neg, ref_neg))
    if r_neg > target + 1e-9:
        record("W3_NEGATION_DENSITY", "WARN", f"unregistered negation-defence {r_neg}/k (baseline {b_neg}/k, reference {ref_neg}); "
               "a named correction is fine, a reflexive one is not.")
    b_un = 1000 * B["negation_unanchored"] / B["units"] if B["units"] else 0.0
    r_un = per_k_excluding("negation_unanchored", rev)
    if r_un > max(b_un, 0.3) + 1e-9:
        un = [c for c in rev["candidates"] if c["type"] == "negation_defense" and not c.get("anchored")]
        record("W4_UNANCHORED_NEGATION", "WARN", f"unanchored negation {r_un}/k vs baseline {round(b_un, 2)}/k: name the view corrected or state the claim positively.",
               [f"{c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in un])
    b_close, r_close = B["echo_share"] + B["abstract_closer_share"], R["echo_share"] + R["abstract_closer_share"]
    ref_close = ref_mean("abstract_closer_share", paragraph_level=True)
    if r_close > b_close + 0.02 or r_close > cfg["closer_share_warn"] or R["epigram_closers"] > cfg["epigram_closers_warn"]:
        closers = [c for c in rev["candidates"] if c["type"] in {"echo_ending", "abstract_closer", "epigram_closer"}]
        record("W5_CLOSERS", "WARN", f"restating closers {round(r_close, 3)} (baseline {round(b_close, 3)}); aphoristic closers {R['epigram_closers']}. "
               "A closing sentence should hand the argument forward, not restate it or end on a slogan.",
               [f"[{c['type']}] {c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in closers])
    keys = ["numbers_per_k"] if a.paper_type in {"quantitative", "theoretical"} else ["quotes_per_k", "numbers_per_k"]
    drops = [f"{k}: revised {R[k]} < baseline {B[k]}" for k in keys if B[k] > 0 and R[k] < B[k] * 0.9]
    if drops:
        record("W6_LIVING_MATERIAL_DENSITY", "WARN", "material density fell; acceptable when stronger material replaced weaker (see G6).", drops)

    coh = []
    if R["topic_link_rate"] < B["topic_link_rate"] - cfg["topic_link_tolerance"]:
        coh.append(f"topic linkage fell: {R['topic_link_rate']} vs baseline {B['topic_link_rate']}")
    ref_link = ref_mean("topic_link_rate")  # sentence-pair measure: merged paragraphs barely affect it
    if ref_link is not None and R["topic_link_rate"] < ref_link - cfg["topic_link_tolerance"]:
        coh.append(f"topic linkage {R['topic_link_rate']} below voice references {ref_link}: sentences rarely pick up what the previous one said")
    if refs:
        ref_len = sum(mean_sentence_length(r) for r in refs) / len(refs)
        if mean_sentence_length(rev) < cfg["sentence_length_ratio_warn"] * ref_len:
            coh.append(f"mean sentence length {mean_sentence_length(rev)} vs references {round(ref_len, 1)}: short assertions instead of linked clauses")
    ref_attr = ref_mean("attributions_per_100_sentences")
    lim_attr = max(B["attributions_per_100_sentences"], ref_attr or 0) * cfg["attribution_ratio_warn"]
    if R["attributions_per_100_sentences"] > max(lim_attr, 10):
        coh.append(f"source parentheses on {R['attributions_per_100_sentences']} of 100 sentences (baseline {B['attributions_per_100_sentences']}, "
                   f"reference {ref_attr}): attribute once per passage from the same source")
    if R["staccato_runs"] > B["staccato_runs"]:
        coh.append(f"staccato runs {R['staccato_runs']} (baseline {B['staccato_runs']})")
    if coh and refs and len(para_ok) < len(refs):
        coh.append(f"{len(refs) - len(para_ok)} of {len(refs)} references have merged paragraphs: treat reference values as direction only")
    if coh:
        runs = [c for c in rev["candidates"] if c["type"] == "staccato_run"]
        record("W8_COHESION", "WARN", "; ".join(coh), [f"{c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in runs])

    # W13 section architecture: entry moves, guided focus shifts, case-selection logic
    order = rev.get("chapter_order", [])
    first_method = next((i for i, ch in enumerate(order) if "methods" in buckets(ch)), None)
    first_closing = next((i for i, ch in enumerate(order) if buckets(ch) & {"discussion", "conclusion"}), None)

    chapter_codes: dict[str, float] = {}
    chapter_units: dict[str, int] = {}
    for m in rev["sections"].values():
        ch = m.get("chapter", "")
        chapter_codes[ch] = chapter_codes.get(ch, 0) + m["code_tokens_per_k"] * m["units"] / 1000
        chapter_units[ch] = chapter_units.get(ch, 0) + m["units"]

    def empirical_or_context(c) -> bool:
        b = buckets(c["section"], c.get("chapter", ""))
        if b & {"theory", "intro", "discussion", "conclusion", "abstract"}:
            return False
        ch = c.get("chapter", "")
        if "methods" in buckets(ch):
            return True
        if ch in order and first_method is not None:
            i = order.index(ch)
            if i < first_method or (first_closing is not None and i >= first_closing):
                return False  # chapters before the methods chapter frame the problem; closing chapters argue
        # an empirical chapter draws on sources: attribution codes appear in it
        units = chapter_units.get(ch, 0)
        return not units or 1000 * chapter_codes.get(ch, 0) / units >= 1.5
    openers = [c for c in rev["candidates"] if c["type"] == "abstract_section_opener" and empirical_or_context(c)]
    shifts = [c for c in rev["candidates"] if c["type"] == "unguided_focus_shift"]
    arch_items = [f"[cold opener] {c['section']}: {c['excerpt']}" for c in openers]
    arch_items += [f"[unguided shift {c.get('from')}→{c.get('to')}] {c['section']} ¶{c['paragraph']}: {c['excerpt']}" for c in shifts]
    method_like = [n for n, m in rev["sections"].items() if "methods" in buckets(n, m.get("chapter", ""))]
    no_selection = bool(method_like) and not any(
        "methods" in buckets(s, rev["sections"].get(s, {}).get("chapter", "")) for s in rev.get("case_selection_sections", []))
    if no_selection and a.paper_type in {"qualitative", "mixed"}:
        arch_items.insert(0, "[case selection] no explicit case-selection logic in the context/methods chapter: say why this case reveals the problem")
    if arch_items:
        record("W13_SECTION_ARCHITECTURE", "WARN",
               f"{len(openers)} empirical/context sections open on an abstract statement; {len(shifts)} paragraph-to-paragraph focus "
               "shifts lack a move or a situated introduction" + ("; case-selection logic missing" if no_selection else "") +
               ". See references/08-narrative-architecture.md.", arch_items)

    # W14 material renewal: route correction should look for stronger material, not only keep the old
    base_q = {norm(q)[:16] for q in quotes_of(base) if norm(q)}
    rev_q = [q for q in quotes_of(rev) if norm(q)]
    new_q = [q for q in rev_q if norm(q)[:16] not in base_q]
    if a.paper_type in {"qualitative", "mixed"} and base_q and not new_q:
        record("W14_MATERIAL_RENEWAL", "WARN",
               f"all {len(rev_q)} sourced quotations come from the baseline; none was added or upgraded from the raw sources. "
               "Confirm the material-upgrade search (P2) was done and record why the baseline material was kept.")

    # W15 conversion-frame template: the outcome stated through the same "使X成为Y" sentence again and again
    conv_ref = ref_mean("conversion_frame_share")
    conv_limit = max(cfg["conversion_frame_warn"], 2 * B["conversion_frame_share"], (conv_ref or 0) + 0.03)
    if R["conversion_frame_share"] > conv_limit:
        conv = [s for s in rev["sentences"] if "conversion_frame" in s["flags"]]
        record("W15_CONVERSION_TEMPLATE", "WARN",
               f"{R['conversion_frame_share']} of sentences use a '使X成为/获得/进入Y' (turns X into Y) frame "
               f"(baseline {B['conversion_frame_share']}, reference {conv_ref}): show the change through who did what and "
               "what it was used for before and after, and keep the conceptual restatement for where it adds a step.",
               [f"{s['section']} ¶{s['paragraph']}: {s['sentence'][:160]}" for s in conv])

    # W16 relation-verb tic: a suppressed template returns in a neighbouring form ("使X进入Y" -> "X进入Y").
    # Placeholder relation verbs and chained inferential connectives name a link without showing it.
    lang = rev["lang"]
    tics = []
    for key, floor_key, ratio_key, label in (
            ("relation_verbs_per_k", "relation_verb_floor_per_k", "relation_verb_ref_ratio", "placeholder relation verbs (进入/接入/纳入/相接/参与构成…)"),
            ("inferential_per_k", "inferential_floor_per_k", "inferential_ref_ratio", "inferential connectives (由此/因此/从而…)")):
        ref = ref_mean(key)
        limit = max(cfg[floor_key][lang], cfg[ratio_key] * ref) if ref is not None else cfg[floor_key][lang]
        if R.get(key, 0) > limit:
            inherited = " (already over the limit in the baseline: reduce the inherited habit, do not carry it)" if B.get(key, 0) > limit else ""
            tics.append(f"{label} {R[key]}/k vs limit {round(limit, 2)}/k (baseline {B.get(key)}, reference {ref}){inherited}")
    if tics:
        top = ", ".join(f"{k}×{v}" for k, v in rev.get("top_relation_verbs", []))
        record("W16_RELATION_VERB_TIC", "WARN",
               "; ".join(tics) + f". Most used: {top or '-'}. Say what the actor did (who handed what to whom, when, with what) instead of saying X 'entered' or 'was connected to' Y; let the logic show through "
               "the sequence instead of chaining 由此/因此. Rewrite the sentences where the verb stands in for an action and leave the plain uses; "
               "swapping the verb for a noun tag (用途/对应/安排) is the same habit (W17). See references/03-detracing.md T17.",
               [f"{s['section']} ¶{s['paragraph']}: {s['sentence'][:160]}" for s in rev["sentences"] if "relation_verb" in s["flags"]])

    # W17 tag-word surge: whatever word replaced the last suppressed template. A word that now sits in a large
    # share of paragraphs, far more than in the baseline and rare in the references, usually tags paragraphs
    # instead of saying something. The paper's own terms (title, keywords, --core-term) are exempt.
    exempt = set(rev.get("front_terms", []))
    for term in a.core_term:
        exempt |= set(trace_scan.lexical_grams(term, lang))

    def dens(scan, g):
        u = scan["totals"]["units"]
        return 1000 * scan.get("lexicon", {}).get(g, 0) / u if u else 0.0

    surges = []
    for g, n in rev.get("lexicon", {}).items():
        if g in exempt or n < cfg["tag_word_min_count"]:
            continue
        sp, bsp = rev.get("lexicon_spread", {}).get(g, 0.0), base.get("lexicon_spread", {}).get(g, 0.0)
        rd, fd = dens(rev, g), (sum(dens(r, g) for r in refs) / len(refs) if refs else 0.0)
        if (sp >= cfg["tag_word_min_spread"] and sp >= cfg["tag_word_base_ratio"] * bsp
                and rd >= cfg["tag_word_ref_ratio"] * fd + 0.5):
            surges.append((sp, g, bsp, rd, fd))
    if surges:
        surges.sort(reverse=True)
        record("W17_TAG_WORD", "WARN",
               f"{len(surges)} word(s) now appear in a large share of paragraphs, far more than in the baseline and rarely "
               "in the references. A suppressed template often returns as a new tag word: keep the word where it states "
               "the claim, and elsewhere say what happened. Pass the paper's own concept terms with --core-term. "
               "See references/04 H5a.",
               [f"{g}: in {round(100 * sp)}% of paragraphs (baseline {round(100 * bsp)}%), {round(rd, 2)}/k vs reference {round(fd, 2)}/k"
                for sp, g, bsp, rd, fd in surges[:12]])

    code_ref = ref_mean("code_tokens_per_k")
    if R["code_tokens_per_k"] > max(cfg["code_tokens_warn_per_k"], code_ref or 0.0) and R["code_tokens_per_k"] >= B["code_tokens_per_k"] * 0.8:
        record("W1_CODE_PERSONAE", "WARN", f"actor-code density {R['code_tokens_per_k']}/k (baseline {B['code_tokens_per_k']}/k, reference {code_ref}).")
    if B["abstract_terms_per_k"] and R["abstract_terms_per_k"] > B["abstract_terms_per_k"] * (1 - cfg["abstract_terms_min_reduction"]):
        m = ref_mean("abstract_terms_per_k")
        if m is None or R["abstract_terms_per_k"] > m:
            record("W2_ABSTRACT_FOG", "WARN", f"abstract-term density {R['abstract_terms_per_k']}/k (baseline {B['abstract_terms_per_k']}/k, reference {m}).")
    for bucket in ("intro", "discussion", "conclusion"):
        names = [n for n, m in rev["sections"].items() if bucket in buckets(n, m.get("chapter", ""))]
        if names and sum(rev["sections"][n]["stance"] for n in names) == 0:
            record("W9_STANCE", "WARN", f"no explicit author-stance sentence in {bucket} sections {names}.")
    heavy = [f"{n}: {m['caveat_sentence_share']}" for n, m in rev["sections"].items()
             if m["sentences"] >= 4 and m["caveat_sentence_share"] > cfg["caveat_share_warn"]]
    if heavy:
        record("W10_CAVEAT_BUDGET", "WARN", "sections where hedge/negation sentences exceed the caveat budget.", heavy)
    for n, m in rev["sections"].items():
        if "theory" in buckets(n, m.get("chapter", "")) and m["sentences"] >= 4 and m["lit_chain"] / m["sentences"] > cfg["lit_chain_warn_share"]:
            record("W11_LITERATURE_CHAIN", "WARN", f"{n}: {m['lit_chain']}/{m['sentences']} 'study X stresses Y [n]' sentences.")
    if refs:
        drift = []
        for k in ["negation_defense_per_k", "abstract_terms_per_k", "quotes_per_k", "abstract_closer_share", "topic_link_rate"]:
            m = ref_mean(k)
            if m is not None and abs(R[k] - m) > abs(B[k] - m) + 1e-9:
                drift.append(f"{k}: {B[k]} -> {R[k]} (reference {m})")
        if drift:
            record("W12_VOICE_DRIFT", "WARN", "metrics that moved away from the voice references (context, not targets).", drift)
    for w in rev.get("reliability_warnings", []):
        record("W0_SCAN_RELIABILITY", "WARN", f"revised: {w}")
    for r in refs:
        for w in r.get("reliability_warnings", []):
            record("W0_SCAN_RELIABILITY", "WARN", f"reference {Path(r['file']).name}: {w}")
    return finish(base, rev, refs)


if __name__ == "__main__":
    raise SystemExit(main())
