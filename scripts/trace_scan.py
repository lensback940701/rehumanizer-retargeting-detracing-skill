#!/usr/bin/env python3
"""Deterministic signal scanner for route-correction diagnostics (v2).

Reads a manuscript (.md, .txt, .docx; .pdf only with pypdf installed and with a
reliability warning; Chinese or English) and reports signals of over-defensive,
workflow-traced and poorly connected prose, plus the density of living
material. Every output is a SIGNAL, never an editorial decision.

v2 changes: quote-aware sentence splitting (speech inside quotation marks is
never counted as the author's hedging); full candidate lists (display limits
apply only to the Markdown report); numbered reference headings; paragraph-
level opponent anchoring; tables skipped identically in DOCX and Markdown;
logical connectives no longer count as wrap-up closers; new cohesion signals
(topic linkage between sentences, explicit relation markers, sentence length,
staccato runs, aphoristic closers, attribution-parenthesis clutter).

Usage:
    python trace_scan.py MANUSCRIPT [--lang auto|zh|en] [--abstract-terms FILE]
        [--out-json PATH] [--out-md PATH] [--max-display N]
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

PATTERNS = {
    "zh": {
        "process_trace": [
            r"据(受访者|访谈|原文|材料|记录|文本)(介绍|所述|整理|显示|呈现)",
            r"依其(明确)?(叙述|表述|说法)(整理|呈现|排列)",
            r"随其表达者",
            # internal labels for documents in the author's project (sibling papers, drafts) are not citations
            r"论文[①-⑳]", r"[①-⑳][^。；]{0,30}(论文|稿件)", r"姊妹(论文|稿|篇)",
            r"(经|已|逐一|逐条)(核对|核实|核验|复核)",
            r"(证据|论断|主张|判断)(上限|层级|层次|边界|状态)",
            r"(证据|引用|引语|核验|审计)(台账|锚点|准入|清单)|回指|保护项|冻结稿|基线稿",
            r"(在|于)同(一)?场访谈(的)?(后面|后段|前面|稍后)",
            r"(这段话|该段话|此段话|这句话)(接着|随后|紧接着)",
            r"(访谈|材料|文本|转录)(级别|层面)的?(核验|证据|支持)",
            r"未经(音频|实地|独立)?(核验|验证|核实)",
            r"(编号|代称)(标识|用于标识|仅用于)",
            r"(本文|本研究)(据此|只|仅)(理解|整理|呈现|记录)",
            r"(不作|不做)(效果|因果)?(认定|推断|外推)",
            r"(?i)\b(claim ceiling|evidence ceiling|ledger|protected baseline)\b",
        ],
        "source_first": [
            r"^(访谈|材料|资料|文本|记录|受访者(的)?(介绍|讲述|回顾))(显示|表明|呈现|说明|提示|反映)",
            r"(从|据)(访谈|材料|资料)(来看|看)",
        ],
        "negation_defense": [
            r"而非", r"而不是", r"并非", r"并不(意味着|等于|代表|是说)",
            r"不(等于|意味着)",
            r"不能(仅|只|简单|直接|单纯)?(由|从|以|据|把|将)?[^，。；]{0,12}(视为|理解为|推知|推定|归结|等同|衡量|当作)",
            r"不应(被)?(简单|直接|仅|只)?(视为|理解为|归结|等同|当作)",
            r"不只是|不仅仅是|未必",
        ],
        "hedge": [
            r"可能", r"或许", r"也许", r"在一定程度上", r"某种程度上", r"一定程度",
            r"有待", r"尚需", r"尚待", r"似乎", r"倾向于", r"大致", r"或多或少",
        ],
        "hedged_finding": [
            r"(?<!怎样)(?<!如何)(?<!是否)与[^，。；？]{1,25}(有关|相关|密切相关)(?![的地])",
            r"(可能|或许)(会)?(影响|导致|促进|改变|塑造)",
            r"存在(一定|某种)(的)?(联系|关联|影响|作用)",
        ],
        "summary_opener": r"^(由此可见|综上|总之|总而言之|换言之|也就是说|这说明|这表明|可见)",
        "stance": r"(本文|本研究|我们|笔者)[^。；，]{0,14}(认为|主张|提出|发现|指出|揭示|论证|判断|强调|说明|表明)",
        "lit_chain": (
            r"(研究|理论|视角|文献|学者|分析)[^。；]{0,30}(强调|关注|说明|揭示|指出|表明|认为|提示|发现)"
            r"[^。；]{0,80}(\[\d|（[^）]{0,40}\d{4}）)"
        ),
        "opponent_marker": r"(\[\d|（[^）]{0,40}\d{4}）|研究|理论|观点|文献|学者|论者|看法|假设|预设|叙事|主流|通常|常见|框架|解释)",
        "relation_marker": (
            r"(因此|因而|所以|于是|由于|因为|从而|以致|由此|这就|这使|然而|但是|但|却|不过|反而|相反|可是|"
            r"虽然|尽管|即使|固然|如果|若|只有|只要|一旦|除非|例如|比如|譬如|此外|同时|进一步|更重要的是|"
            r"一方面|另一方面|与此|相比|对比|同样|换言之|也就是说|而是|既然|以至于|反过来)"
        ),
        "epigram": r"(没有[^，。]{0,8}变|不是[^，。]{0,10}是|[^，。]{1,6}，也[^，。]{1,6})",
        "conversion_frame": r"(使|让|把|将)[^。；]{0,30}(成为|获得|进入|转成|转为|编排|接入|变成)",
        # placeholder relation verbs: they name a link without saying what anyone did
        "relation_verb": (r"(进入|接入|纳入|带入|接到|接在|相接|连接|衔接|嵌入|转化为|转译为|落实(?:到|于|为)|落到|"
                          r"参与(?:构成|界定|形成|生成|塑造|决定))"),
        "inferential": r"(由此|因此|因而|从而|进而)",
        "default_abstract_terms": [
            "条件", "安排", "关系", "环节", "机制", "过程", "路径", "维度", "层面", "范围",
            "方式", "逻辑", "要素", "主体", "情境", "场景", "联系", "组织", "实施", "进入",
        ],
    },
    "en": {
        "process_trace": [
            r"\bas (recorded|verified|transcribed|documented) (in|by)\b",
            r"\baccording to the (transcript|interview record|record|materials|source file)\b",
            r"\bsibling (paper|manuscript|article|study|studies)s?\b", r"\b(paper|manuscript) [①-⑳]",
            r"\bclaim ceiling\b", r"\bevidence (ceiling|anchor|status|ledger|register)\b",
            r"\baudit (ledger|trail|register)\b", r"\b(locator|anchor) (id|code)\b",
            r"\bnot (independently|audio-)verified\b", r"\b(this|the) (pass|goal)\b",
            r"\blater in the same interview\b", r"\bthe (speaker|interviewee) then adds\b",
        ],
        "source_first": [
            r"^(the )?(interviews?|materials|documents|records|data|sources) (show|indicate|suggest|reveal|demonstrate)",
            r"^(as )?(respondents|interviewees|participants) (reported|described|noted)",
        ],
        "negation_defense": [
            r"\brather than\b", r"\bnot merely\b", r"\bnot simply\b", r"\bnot just\b",
            r"\bdoes not (mean|imply|equal)\b", r"\bshould not be (read|seen|understood|treated|reduced)\b",
            r"\bthis is not to say\b", r"\bcannot be (reduced|read|inferred)\b", r"\bnot necessarily\b",
        ],
        "hedge": [
            r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bperhaps\b", r"\bpossibly\b",
            r"\bpotentially\b", r"\bappears? to\b", r"\bseems? to\b", r"\btends? to\b",
            r"\bto some extent\b", r"\bsomewhat\b", r"\barguably\b", r"\bin part\b",
        ],
        "hedged_finding": [
            r"\bis (related|linked|associated|connected) (to|with)\b",
            r"\b(may|might|could) (shape|affect|influence|drive|lead to)\b",
            r"\bsome (relationship|association|influence)\b",
        ],
        "summary_opener": r"^(In short|In other words|Taken together|In sum|To sum up|Overall)\b",
        "stance": (
            r"\b(we|I) (argue|contend|show|propose|find|claim|maintain)\b|"
            r"\bthis (article|paper|study) (argues|shows|contends|demonstrates|proposes)\b"
        ),
        "lit_chain": (
            r"\b([A-Z][A-Za-z\-]+( et al\.)?|[Ss]tudies|[Rr]esearch|[Ss]cholars)\s*(\(\d{4}[a-z]?\)\s*)?"
            r"(argues?|shows?|emphasi[sz]es|highlights?|notes?|suggests?|stresses|focus(es)? on)\b"
        ),
        "opponent_marker": (
            r"(\[\d|\(\D{0,40}\d{4}|\bstud(y|ies)\b|\btheor(y|ies)\b|\bview\b|\bliterature\b|"
            r"\bscholars?\b|\bassum|\bconventional|\bdominant|\boften\b|\bcommonly\b|\bframework\b)"
        ),
        "relation_marker": (
            r"\b(because|therefore|thus|hence|so that|consequently|as a result|however|but|yet|although|"
            r"though|whereas|while|instead|rather|if|unless|once|for example|for instance|moreover|"
            r"furthermore|in turn|by contrast|similarly|likewise|that is|in other words|this means)\b"
        ),
        "epigram": r"(\bnot\b.{0,30}\bbut\b|\bno longer\b)",
        "conversion_frame": r"\b(turns?|turned|makes?|made|renders?|rendered|converts?|converted|transforms?|transformed)\b[^.;]{0,40}\b(into|an? [a-z]+ (object|resource)|available|operable|usable)\b",
        "relation_verb": (r"\b(enter(?:s|ed|ing)? into|integrat\w* into|incorporat\w* into|embed\w* in(?:to)?|feed(?:s|ing)? into|"
                          r"fed into|translat\w* into|plug\w* into|help(?:s|ed)? (?:to )?(?:constitute|shape|define)|"
                          r"participat\w* in (?:constitut|shap|defin)\w*)\b"),
        "inferential": r"\b(thus|thereby|hence|therefore|in turn)\b",
        "default_abstract_terms": [
            "conditions", "arrangements", "relations", "dynamics", "processes", "mechanisms",
            "dimensions", "levels", "scope", "modes", "logics", "elements", "actors",
            "contexts", "settings", "practices", "configurations", "implementation",
        ],
    },
}

HEADING_NUMBER = re.compile(r"^\s*((第[一二三四五六七八九十]+[章节部分])|[一二三四五六七八九十]+[、.．]|[IVXivx]+\.|\d{1,2}(\.\d{1,2})*\.?)\s*")
STOP_HEADINGS = re.compile(r"^(参考文献|references|bibliography|works cited|注释|致谢|acknowledg|附录|appendix)", re.I)
NONPROSE = re.compile(
    r"^(!\[|\||图\s*\d|表\s*\d|Fig\.?\s*\d|Figure\s*\d|Table\s*\d|注[:：]|Note[s]?[:.]|来源[:：]|Source[s]?[:.]|"
    r"关键词|Key\s*words|Keywords|中图分类号|文献标识码|DOI)",
    re.I,
)
HEADING_GUESS = re.compile(
    r"^((?!\d{4})\d{1,2}(\.\d{1,2})*\.?\s*[^\d\s.,，、%％:：)）].{0,40}|[一二三四五六七八九十]+[、.]\s*\S.{0,30})$"
)
CODE_TOKEN = re.compile(r"(?<![A-Za-z0-9])[A-Z]{1,3}\d{1,3}(?![0-9A-Za-z])")
ATTRIBUTION = re.compile(
    r"[（(][^()（）]{0,20}(?<![A-Za-z])[A-Z]{1,3}\d{1,3}[^()（）]{0,25}[）)]|[（(](?:Interview|interview|访谈)[^()（）]{0,40}[）)]"
)
ZH_QUOTE = re.compile(r"“([^”]{8,})”")
EN_QUOTE = re.compile(r"[“\"]([^”\"]{25,})[”\"]")
ZH_NUMBER = re.compile(
    r"(?<![\[\d])\d+(?:\.\d+)?\s*(?:%|％|元|万|亿|吨|亩|公顷|公斤|千克|斤|米|厘米|毫米|公里|次|个|户|人|家|天|小时|分钟|分|倍|批|场|棵|株|项)"
)
EN_NUMBER = re.compile(
    r"(?<![\[\w])(?:\$|USD\s?|RMB\s?|€|£)?\d[\d,]*(?:\.\d+)?\s?(?:%|percent|per cent|km|kg|tonnes?|tons?|hectares?|ha\b|"
    r"households?|people|respondents|firms|villages|times|days|hours|months|years old|yuan|dollars)"
)
CITE_NUM = re.compile(r"\[(\d+(?:\s*[-–,，]\s*\d+)*)\]")
CITE_AY = re.compile(r"\(([A-Z][A-Za-z\-]+(?: et al\.)?(?: (?:and|&) [A-Z][A-Za-z\-]+)?),? (\d{4}[a-z]?)")
QUOTED = re.compile(r"“[^”]*”|\"[^\"]*\"|「[^」]*」|‘[^’]{12,}’")
BLOCK_QUOTE_END = re.compile(
    r"[（(][^()（）]{0,60}(interview|访谈|座谈|田野笔记|field ?notes?|(?<![A-Za-z])[A-Z]{1,3}\d{1,3})[^()（）]{0,40}[)）]\s*[。.]?$",
    re.I,
)
FIRST_PERSON = re.compile(r"(\b(I|my|me|we|our)\b|我们|我|咱们)")
CONCRETE = re.compile(r"(“|\"|\d|(?<![A-Za-z])[A-Z]{1,3}\d|\[\d|\(\D{0,40}\d{4})")


PLACE_CHARS = "村镇县市省河山坝谷乡区州江湖岛街巷园厂"
MOVE_ZH = re.compile(
    r"(前述|上述|这位|此前提到|相比|相较|并置|对照|对比|与[^，。]{1,15}(不同|相比|相对|并置|对照)|不同于|另一(位|家|户|处|种|端|侧|边|条|方面|面)|转向|转到|回到|再看|同样|同一(条|片|个|位|家|地区|区域|村|社区|地块)|"
    r"^(除了|除此之外|此外|当)|^[^，。]{2,14}时[，,]|沿着|顺着|到了|往[上下东西南北]|在[^，。]{1,12}(之外|以外|另一|对面|下游|上游|附近|另一侧)|离开|走出|视线|把目光|从[^，。]{1,15}(转|走|移|看))"
)
MOVE_EN = re.compile(
    r"\b(by contrast|in contrast|unlike|compared with|turning to|back (at|in|to)|elsewhere|on the other side|across|"
    r"a few (kilometres|kilometers|miles)|downstream|upstream|similarly|likewise|meanwhile)\b", re.I)
ROLE_ZH = re.compile(r"(经营者|经营户|种植户|农户|村民|村干部|干部|企业|企业主|商户|受访者|种植者|收购者|农民|居民|官员|管理部门|合作社|老板|工人|员工|移民|游客|社区工作者)")
ROLE_EN = re.compile(r"\b(farmers?|owners?|officials?|residents?|managers?|firms?|compan(y|ies)|entrepreneurs?|cooperatives?|workers?|couriers?|traders?)\b", re.I)
BRIDGE_ZH = re.compile(
    r"^(同样|相比|与此|与之|另一|转向|回到|再看|同一|这|此|上述|前述|另一方面|与[^，。]{1,12}不同|不同于|相对于|"
    r"在[^，。]{1,12}(之外|以外|的另一|另一端|对面|下游|上游)|沿着|顺着|走出|离开|到了|同在|也是在|视线|镜头|把目光|从[^，。]{1,15}(转|走|移)|"
    r"然而|但|不过|因此|由此|于是|此后|随后|与此同时)"
)
BRIDGE_EN = re.compile(
    r"^(Similarly|By contrast|In contrast|Meanwhile|Turning to|Back (at|in|to)|Elsewhere|On the other side|Moving|"
    r"Across|Unlike|Like|This|These|That|Such|However|Yet|Still|Then|Later|Downstream|Upstream)\b"
)
CASE_SELECTION = re.compile(
    r"(选取[^，。]{0,20}(作为|为)|选择[^，。]{0,20}作为|(本文|本研究|我们)(选择|选取)[^。]{1,20}(是因为|是由于|因为|原因在于|在于)|之所以选择|之所以选取|典型(案例|地区|意义)|代表性|启示性|极端案例|"
    r"研究区域选择|选择[^，。]{0,10}为(研究区|案例)|"
    r"case (was |were )?(selected|chosen)|we (selected|chose)|chosen because|revelatory|typical case|extreme case|critical case|"
    r"ideal case|(provides|offers) an? (ideal|good|useful|suitable|strategic|instructive) (case|site|setting)|case study (area|site))",
    re.I,
)
SCENE_MARKERS = re.compile(r"(\d{4}年|\d+月|那年|当时|起初|最早|一位|这位|那位|一家|这家|\b(19|20)\d{2}\b|\bin (19|20)\d{2}\b|\bwhen\b|\bone (farmer|resident|official|courier|owner)\b)", re.I)


def concrete_anchor(sentence: str, lang: str) -> bool:
    """Place, time, person-in-scene, number, quotation or source code."""
    if CONCRETE.search(sentence) or SCENE_MARKERS.search(sentence):
        return True
    if lang == "zh" and re.search(rf"[\u4e00-\u9fff]{{1,4}}[{PLACE_CHARS}](?![\u4e00-\u9fff]{{0,1}}(化|性|式))", sentence[:40]):
        return True
    return bool(lang == "en" and re.search(r"\b[A-Z][a-z]+ (Village|County|City|Province|River|Valley)\b", sentence))


@dataclass
class Paragraph:
    index: int
    section: str
    text: str
    sentences: list = field(default_factory=list)
    chapter: str = ""


def normalize(text: str) -> str:
    return re.sub(r"[\s\W_]+", "", text.lower())


def clean_heading(text: str) -> str:
    return HEADING_NUMBER.sub("", text.strip()).strip()


def heading_level_from_text(text: str) -> int:
    m = re.match(r"^\s*(\d{1,2}(?:\.\d{1,2})*)", text)
    return m.group(1).count(".") + 1 if m else 1


SPEECH_BEFORE = re.compile(r"(说|道|表示|回答|回忆|形容|解释|提到|提醒|问|写道|称|概括|评价|认为)[^“”。]{0,6}[：:，,]?\s*$|[：:]\s*$")
SPEECH_BEFORE_EN = re.compile(r"\b(said|says|explained|recalled|noted|told|asked|replied|wrote|put it|described)\b[^\"“”.]{0,12}[:,]?\s*$", re.I)


ZH_QUOTE_ANY = re.compile(r"“([^”]{4,})”")
EN_QUOTE_ANY = re.compile(r"[“\"]([^”\"]{12,})[”\"]")


def sourced_quotes(text: str, lang: str) -> list[str]:
    """Direct quotations attributed to a source: followed by an attribution parenthesis or
    introduced by a speech verb. Short attributed quotes count; scare-quoted concepts do not."""
    rx = ZH_QUOTE_ANY if lang == "zh" else EN_QUOTE_ANY
    before_rx = SPEECH_BEFORE if lang == "zh" else SPEECH_BEFORE_EN
    out = []
    for m in rx.finditer(text):
        after = text[m.end():m.end() + 40]
        before = text[max(0, m.start() - 20):m.start()]
        if ATTRIBUTION.match(after.lstrip()) or ATTRIBUTION.search(after[:30]) or before_rx.search(before):
            out.append(m.group(1))
    if is_block_quote(text):
        out.append(text)
    return out


def is_block_quote(text: str) -> bool:
    """A paragraph that is itself a quotation, not author prose containing one.
    Quoted form: opens with a quotation mark and ends with an attribution.
    Unquoted extract (common in English papers): no quotation marks, first person,
    closing attribution."""
    t = text.strip()
    if not BLOCK_QUOTE_END.search(t):
        return False
    if t[:1] in "“「\"":
        return True
    has_marks = any(ch in t for ch in "“”「」\"")
    return not has_marks and len(FIRST_PERSON.findall(t)) >= 2


def author_voice(sentence: str) -> str:
    return QUOTED.sub("“”", sentence)


# ---------------------------------------------------------------- loading

def _docx_items(path: Path):
    with zipfile.ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find(W_NS + "body")
    for child in body:
        if child.tag != W_NS + "p":
            continue  # tables (w:tbl) are skipped, matching Markdown table handling
        text = "".join(t.text or "" for t in child.iter(W_NS + "t")).strip()
        if not text:
            continue
        style, level = "", None
        ppr = child.find(W_NS + "pPr")
        if ppr is not None:
            ps = ppr.find(W_NS + "pStyle")
            if ps is not None:
                style = ps.get(W_NS + "val", "")
            ol = ppr.find(W_NS + "outlineLvl")
            if ol is not None:
                level = int(ol.get(W_NS + "val", "0")) + 1
        is_heading = bool(re.search(r"heading|标题|title", style, re.I)) or level is not None
        if is_heading and level is None:
            m = re.search(r"(\d)", style)
            level = int(m.group(1)) if m else heading_level_from_text(text)
        yield is_heading, text, level or 1


def _md_items(path: Path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    block: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or (len(stripped) <= 24 and STOP_HEADINGS.match(clean_heading(stripped))):
            if block:
                yield False, " ".join(block), 0
                block = []
            hashes = len(stripped) - len(stripped.lstrip("#"))
            yield True, stripped.lstrip("#").strip(), max(1, hashes)
        elif not stripped or stripped.startswith("|"):
            if block:
                yield False, " ".join(block), 0
                block = []
        else:
            block.append(stripped)
    if block:
        yield False, " ".join(block), 0


def _pdf_items(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit("PDF input needs pypdf, or convert the PDF to Markdown first (e.g., with an OCR skill).") from exc
    text = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(path)).pages)
    for block in re.split(r"\n\s*\n", text):
        b = " ".join(block.split())
        if b:
            yield False, b, 0


def load_paragraphs(path: Path) -> list[Paragraph]:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        items = list(_docx_items(path))
    elif suffix in {".md", ".markdown", ".txt"}:
        items = list(_md_items(path))
    elif suffix == ".pdf":
        items = list(_pdf_items(path))
    else:
        raise SystemExit(f"Unsupported file type: {path}")
    paragraphs: list[Paragraph] = []
    section, chapter, top_level = "(front)", "", None
    head_levels = [lv for h, _, lv in items if h]
    if head_levels:
        lowest = min(head_levels)
        if head_levels.count(lowest) == 1 and head_levels[0] == lowest and len(set(head_levels)) > 1:
            top_level = min(lv for lv in head_levels[1:])  # first heading is the document title
    for is_heading, text, level in items:
        if not is_heading and len(text) <= 40 and not text.endswith(("。", ".", "；", ";")) and HEADING_GUESS.match(text):
            is_heading, level = True, heading_level_from_text(text)
        if is_heading:
            if STOP_HEADINGS.match(clean_heading(text)):
                break
            section = text.strip()[:60]
            if top_level is None:
                top_level = level
            if level <= top_level:
                chapter = section
            elif not chapter:
                chapter = section
            continue
        if len(text) <= 24 and STOP_HEADINGS.match(clean_heading(text)):
            break
        if NONPROSE.match(text):
            caption_like = text.rstrip("。.").count("。") == 0 and text.rstrip(".").count(". ") == 0  # captions are one unit
            if caption_like or not re.match(r"^(图|表|Fig|Figure|Table)\s*\d", text, re.I):
                continue
        paragraphs.append(Paragraph(len(paragraphs) + 1, section, text, chapter=chapter))
    return paragraphs


# Characters that make a bigram grammatical glue rather than vocabulary (for the lexical profile).
LEX_STOP_ZH = set("的了着过和与及或在是为中其这那一也而又并把被将从以于之所等个们他她它我你有就都还很")


def lexical_grams(text: str, lang: str) -> list:
    """Content bigrams (zh) or content words (en), with repeats, for the lexical profile."""
    if lang == "zh":
        out = []
        for run in re.findall(r"[一-鿿]+", text):
            out += [a + b for a, b in zip(run, run[1:]) if a not in LEX_STOP_ZH and b not in LEX_STOP_ZH]
        return out
    return [w for w in (x.lower() for x in re.findall(r"[A-Za-z]{4,}", text)) if w not in EN_STOP]


def front_terms(path: Path, lang: str) -> list:
    """Grams of the title and keyword line: the paper's own key terms are exempt from surge checks."""
    try:
        items = list(_docx_items(path)) if path.suffix.lower() == ".docx" else (
            list(_md_items(path)) if path.suffix.lower() in {".md", ".markdown", ".txt"} else [])
    except Exception:  # noqa: BLE001
        return []
    texts = [items[0][1]] if items else []
    texts += [x[1] for x in items if re.match(r"\s*(关键词|key\s*words|keywords)\s*[:：]", x[1], re.I)]
    return sorted({g for t in texts for g in lexical_grams(t, lang)})


def detect_lang(paragraphs: list[Paragraph]) -> str:
    sample = "".join(p.text for p in paragraphs)[:20000]
    cjk = len(re.findall(r"[一-鿿]", sample))
    return "zh" if sample and cjk / max(1, len(sample)) > 0.15 else "en"


def split_sentences(text: str, lang: str) -> list[str]:
    """Split at terminal punctuation outside quotation marks."""
    out, buf, depth, ascii_open = [], [], 0, False
    terminals = "。！？!?" if lang == "zh" else ".!?"
    n = len(text)
    for i, ch in enumerate(text):
        buf.append(ch)
        if ch in "“「":
            depth += 1
        elif ch in "”」":
            depth = max(0, depth - 1)
        elif ch == '"':
            ascii_open = not ascii_open
        if ch in terminals and depth == 0 and not ascii_open:
            if lang == "en" and i + 1 < n:
                nxt = text[i + 1:i + 3]
                if not (nxt[:1].isspace() and re.match(r"[A-Z“\"(\[]", nxt[1:2] or "A")):
                    continue
            out.append("".join(buf).strip())
            buf = []
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return [s for s in out if len(s) > 1]


def text_units(text: str, lang: str) -> int:
    if lang == "zh":
        return len(re.findall(r"[一-鿿A-Za-z0-9]", text))
    return len(re.findall(r"[A-Za-z0-9'’\-]+", text))


# ---------------------------------------------------------------- helpers

ZH_STOP_BIGRAMS = {"本文", "我们", "他们", "这一", "一个", "这种", "这些", "以及", "进行", "通过", "可以", "其中",
                   "同时", "因此", "但是", "然而", "如果", "因为", "所以", "就是", "已经", "还是", "没有"}
EN_STOP = {"this", "that", "these", "those", "with", "from", "which", "their", "there", "were", "have", "been",
           "they", "into", "than", "also", "such", "more", "most", "other", "about", "when", "what", "where"}


def _grams(text: str, lang: str) -> set:
    if lang == "zh":
        chars = re.findall(r"[一-鿿]", text)
        return {a + b for a, b in zip(chars, chars[1:])} - ZH_STOP_BIGRAMS
    return {w.lower() for w in re.findall(r"[A-Za-z]{4,}", text)} - EN_STOP


def first_clause(sentence: str) -> str:
    return re.split(r"[，：；,:;]", sentence, maxsplit=1)[0]


def echo_score(sents: list[str], lang: str) -> float:
    if len(sents) < 3:
        return 0.0
    last, prev = _grams(sents[-1], lang), _grams(sents[-2], lang)
    return len(last & prev) / len(last) if len(last) >= 4 else 0.0


# ---------------------------------------------------------------- scan

def scan(path: Path, lang: str = "auto", abstract_terms: list[str] | None = None, max_candidates: int | None = None) -> dict:
    """Full scan. `max_candidates` is accepted for backward compatibility and ignored:
    candidate lists are always complete; only the Markdown report truncates."""
    paragraphs = load_paragraphs(path)
    if lang == "auto":
        lang = detect_lang(paragraphs)
    pats = PATTERNS[lang]
    flags_re = 0 if lang == "zh" else re.I
    compiled = {k: [re.compile(p, flags_re) for p in v] for k, v in pats.items()
                if isinstance(v, list) and k != "default_abstract_terms"}
    summary_re = re.compile(pats["summary_opener"], flags_re)
    stance_re = re.compile(pats["stance"], flags_re)
    lit_re = re.compile(pats["lit_chain"])
    opp_re = re.compile(pats["opponent_marker"], flags_re)
    rel_re = re.compile(pats["relation_marker"], flags_re)
    epi_re = re.compile(pats["epigram"], flags_re)
    conv_re = re.compile(pats["conversion_frame"], flags_re)
    relv_re = re.compile(pats["relation_verb"], flags_re)
    infer_re = re.compile(pats["inferential"], flags_re)
    relv_counter = Counter()
    lex_counter = Counter()
    lex_paras = Counter()
    prose_paras = 0
    terms = abstract_terms or pats["default_abstract_terms"]
    term_res = {t: re.compile(re.escape(t) if lang == "zh" else r"\b" + re.escape(t) + r"\b", re.I) for t in terms}
    short_limit = 20 if lang == "zh" else 9
    staccato_limit = 35 if lang == "zh" else 18

    candidates, sentence_records = [], []
    sections: dict[str, Counter] = {}
    section_chapter: dict[str, str] = {}
    sent_lengths: list[int] = []
    openings, term_counts, cite_counter = Counter(), Counter(), Counter()

    def add(kind, para, sentence, extra=None):
        rec = {"type": kind, "section": para.section, "chapter": para.chapter, "paragraph": para.index,
               "excerpt": sentence[:220]}
        if extra:
            rec.update(extra)
        candidates.append(rec)

    arch = {"abstract_openers": [], "unguided_shifts": [], "sections_seen": set()}
    bridge_re = BRIDGE_ZH if lang == "zh" else BRIDGE_EN
    prev_para = None
    for para in paragraphs:
        sec = sections.setdefault(para.section, Counter())
        section_chapter[para.section] = para.chapter
        sents = split_sentences(para.text, lang)
        para.sentences = sents
        units = text_units(para.text, lang)
        sec["units"] += units
        sec["paragraphs"] += 1
        sec["sentences"] += len(sents)
        op = (re.findall(r"[一-鿿]", para.text)[:2] if lang == "zh" else re.findall(r"[A-Za-z]+", para.text)[:1])
        if op:
            openings["".join(op) if lang == "zh" else op[0].lower()] += 1
        for m in CITE_NUM.finditer(para.text):
            for chunk in re.split(r"[,，]", m.group(1)):
                if re.search(r"[-–]", chunk):
                    a, b = (x.strip() for x in re.split(r"[-–]", chunk)[:2])
                    if a.isdigit() and b.isdigit() and 0 <= int(b) - int(a) < 50:
                        for k in range(int(a), int(b) + 1):
                            cite_counter[f"[{k}]"] += 1
                elif chunk.strip().isdigit():
                    cite_counter[f"[{chunk.strip()}]"] += 1
        for m in CITE_AY.finditer(para.text):
            cite_counter[f"{m.group(1)} {m.group(2)}"] += 1

        block = is_block_quote(para.text)
        if not block:
            prose_paras += 1
            lex_paras.update(set(lexical_grams(author_voice(para.text), lang)))
        quotes = (ZH_QUOTE if lang == "zh" else EN_QUOTE).findall(para.text)
        short_sourced = [q for q in sourced_quotes(para.text, lang) if q not in quotes and q != para.text]
        quotes = quotes + short_sourced
        sec["quotes"] += len(quotes) + (1 if block else 0)
        sec["quote_units"] += units if block else sum(text_units(q, lang) for q in quotes)
        sec["block_quotes"] += 1 if block else 0
        sec["sourced_quotes"] += len(sourced_quotes(para.text, lang))
        sec["numbers"] += len((ZH_NUMBER if lang == "zh" else EN_NUMBER).findall(para.text))
        sec["code_tokens"] += len(CODE_TOKEN.findall(para.text))
        sec["attributions"] += len(ATTRIBUTION.findall(para.text))
        for t, rx in term_res.items():
            n = len(rx.findall(para.text))
            term_counts[t] += n
            sec["abstract_terms"] += n

        anchored_so_far = False
        prev_sent = None
        run_len = 0
        for s in sents:
            voice = "" if block else author_voice(s)
            sent_lengths.append(text_units(s, lang))
            flags, cues = [], {}
            if opp_re.search(voice):
                anchored_so_far = True
            for kind in ("process_trace", "source_first", "negation_defense", "hedge", "hedged_finding"):
                hits = [m.group(0) for rx in compiled[kind] for m in rx.finditer(voice)]
                if not hits:
                    continue
                flags.append(kind)
                cues[kind] = sorted(set(hits))
                sec[kind] += 1
                extra = {"cue": hits[0]}
                if kind == "negation_defense":
                    extra["anchored"] = anchored_so_far
                    if not anchored_so_far:
                        sec["negation_unanchored"] += 1
                        flags.append("negation_unanchored")
                if kind != "hedge":
                    add(kind, para, s, extra)
            if lit_re.search(s):
                sec["lit_chain"] += 1
                flags.append("lit_chain")
            if stance_re.search(voice):
                sec["stance"] += 1
                flags.append("stance")
            if not block and conv_re.search(voice):
                sec["conversion_frames"] += 1
                flags.append("conversion_frame")
            if not block:
                rv = [m.group(1).lower() for m in relv_re.finditer(voice)]
                if rv:
                    sec["relation_verbs"] += len(rv)
                    relv_counter.update(rv)
                    flags.append("relation_verb")
                sec["inferential"] += len(infer_re.findall(voice))
                lex_counter.update(lexical_grams(voice, lang))
            has_rel = bool(rel_re.search(voice or s))
            if has_rel:
                sec["relation_sentences"] += 1
            if text_units(s, lang) <= short_limit:
                sec["short_sentences"] += 1
            if prev_sent is not None and not block:
                sec["sentence_pairs"] += 1
                linked = bool(_grams(first_clause(s), lang) & _grams(prev_sent, lang))
                if linked:
                    sec["topic_linked_pairs"] += 1
                if not linked and not has_rel and text_units(s, lang) <= staccato_limit:
                    run_len += 1
                    if run_len == 3:
                        sec["staccato_runs"] += 1
                        add("staccato_run", para, s)
                else:
                    run_len = 0
            prev_sent = s
            sentence_records.append({"section": para.section, "chapter": para.chapter, "paragraph": para.index,
                                     "sentence": s, "flags": flags, "cues": cues})

        # ---- section architecture (signals only)
        front = (re.search(r"(摘要|abstract|关键词|keywords)", f"{para.section} {para.chapter}", re.I)
                 or re.match(r"\s*(摘要|abstract|关键词|keywords|key words)\s*[:：]", para.text, re.I))
        if not block and sents and not front:
            first = sents[0]
            if para.section not in arch["sections_seen"]:
                arch["sections_seen"].add(para.section)
                if not concrete_anchor(first, lang) and len(sents) >= 2:
                    sec["abstract_openers"] += 1
                    add("abstract_section_opener", para, first)
            elif prev_para is not None and prev_para.section == para.section:
                prev_codes = CODE_TOKEN.findall(prev_para.text)
                cur_codes = CODE_TOKEN.findall(para.text)
                # focus = the source the paragraph mainly draws on (its first attribution code)
                if prev_codes and cur_codes and cur_codes[0] != prev_codes[0]:
                    move_re, role_re = (MOVE_ZH, ROLE_ZH) if lang == "zh" else (MOVE_EN, ROLE_EN)
                    names_new = bool(role_re.search(first)) and concrete_anchor(first, lang)
                    if not move_re.search(first) and not names_new:
                        sec["unguided_shifts"] += 1
                        add("unguided_focus_shift", para, first, {"from": prev_codes[0], "to": cur_codes[0]})
        if not block:
            prev_para = para
        if block or len(sents) < 3:
            continue
        sec["closable_paragraphs"] += 1
        last = sents[-1]
        score = echo_score(sents, lang)
        if score >= 0.5:
            sec["echo_endings"] += 1
            add("echo_ending", para, last, {"overlap": round(score, 2)})
        rest = set().union(*(_grams(x, lang) for x in sents[:-1]))
        lg = _grams(last, lang)
        restate = len(lg & rest) / len(lg) if len(lg) >= 4 else 0.0
        abstract_hits = sum(len(rx.findall(last)) for rx in term_res.values())
        # Logical connectives alone never make a closer: it must be generic AND restate.
        if not CONCRETE.search(last) and abstract_hits >= 2 and (restate >= 0.35 or summary_re.search(last)):
            sec["abstract_closers"] += 1
            add("abstract_closer", para, last, {"restatement": round(restate, 2)})
        if len(sents) >= 4 and text_units(last, lang) <= (22 if lang == "zh" else 12) and epi_re.search(last):
            sec["epigram_closers"] += 1
            add("epigram_closer", para, last)

    total = Counter()
    for c in sections.values():
        total.update(c)

    def per_k(n, u):
        return round(1000 * n / u, 2) if u else 0.0

    def ratio(a, b):
        return round(a / b, 3) if b else 0.0

    def metrics(c: Counter) -> dict:
        u = c["units"]
        return {
            "units": u, "paragraphs": c["paragraphs"], "sentences": c["sentences"],
            "process_trace": c["process_trace"], "source_first": c["source_first"],
            "negation_defense": c["negation_defense"], "negation_defense_per_k": per_k(c["negation_defense"], u),
            "negation_unanchored": c["negation_unanchored"],
            "hedge_sentences_per_k": per_k(c["hedge"], u), "hedged_finding": c["hedged_finding"],
            "echo_endings": c["echo_endings"], "abstract_closers": c["abstract_closers"],
            "echo_share": ratio(c["echo_endings"], c["closable_paragraphs"]),
            "abstract_closer_share": ratio(c["abstract_closers"], c["closable_paragraphs"]),
            "epigram_closers": c["epigram_closers"],
            "quotes": c["quotes"], "quotes_per_k": per_k(c["quotes"], u), "sourced_quotes": c["sourced_quotes"], "quote_unit_share": ratio(c["quote_units"], u),
            "numbers_per_k": per_k(c["numbers"], u), "code_tokens_per_k": per_k(c["code_tokens"], u),
            "attributions_per_100_sentences": round(100 * c["attributions"] / c["sentences"], 1) if c["sentences"] else 0.0,
            "abstract_terms_per_k": per_k(c["abstract_terms"], u),
            "lit_chain": c["lit_chain"], "stance": c["stance"],
            "caveat_sentence_share": ratio(c["hedge"] + c["negation_defense"], c["sentences"]),
            "topic_link_rate": ratio(c["topic_linked_pairs"], c["sentence_pairs"]),
            "relation_marker_share": ratio(c["relation_sentences"], c["sentences"]),
            "short_sentence_share": ratio(c["short_sentences"], c["sentences"]),
            "staccato_runs": c["staccato_runs"],
            "abstract_openers": c["abstract_openers"], "unguided_shifts": c["unguided_shifts"],
            "conversion_frame_share": ratio(c["conversion_frames"], c["sentences"]),
            "relation_verbs_per_k": per_k(c["relation_verbs"], u),
            "inferential_per_k": per_k(c["inferential"], u),
        }

    mean_para = total["units"] / total["paragraphs"] if total["paragraphs"] else 0
    reliability = []
    if path.suffix.lower() == ".pdf":
        reliability.append("PDF text extraction: paragraph boundaries and headings are approximate.")
    if mean_para > (450 if lang == "zh" else 300):
        reliability.append("Paragraphs look merged (e.g., PDF-derived text): paragraph-level and cohesion signals are unreliable; use per-1000 densities.")
    if len(sections) <= 1:
        reliability.append("No headings detected: section-level signals and reference-list exclusion may be unreliable.")
    if total["units"] == 0:
        reliability.append("No readable prose found.")
    cited = len(cite_counter)
    once = sum(1 for v in cite_counter.values() if v == 1)
    sourced = [q for p in paragraphs for q in sourced_quotes(p.text, lang)]
    case_selection = [p.section for p in paragraphs if CASE_SELECTION.search(p.text)]
    return {
        "file": str(path), "lang": lang,
        "sourced_quotations": sourced,
        "case_selection_sections": sorted(set(case_selection)),
        "chapter_order": list(dict.fromkeys(p.chapter for p in paragraphs if p.chapter)),
        "totals": metrics(total),
        "sentence_length": {
            "mean": round(statistics.mean(sent_lengths), 1) if sent_lengths else 0,
            "stdev": round(statistics.pstdev(sent_lengths), 1) if sent_lengths else 0,
            "cv": round(statistics.pstdev(sent_lengths) / statistics.mean(sent_lengths), 3) if sent_lengths else 0,
        },
        "citations": {"distinct_cited": cited, "cited_once": once, "cited_once_share": ratio(once, cited)},
        "top_abstract_terms": term_counts.most_common(10),
        "top_relation_verbs": relv_counter.most_common(10),
        "lexicon": {g: n for g, n in lex_counter.items() if n >= 3},
        "lexicon_spread": {g: round(lex_paras[g] / prose_paras, 3) for g, n in lex_counter.items() if n >= 3 and prose_paras},
        "front_terms": front_terms(path, lang),
        "repeated_paragraph_openings": [(k, v) for k, v in openings.most_common(8) if v >= 3],
        "sections": {name: dict(metrics(c), chapter=section_chapter.get(name, "")) for name, c in sections.items()},
        "candidates": candidates,
        "sentences": sentence_records,
        "reliability_warnings": reliability,
        "note": "Signals only. Inspect every candidate in context; counts are not edit quotas.",
    }


def to_markdown(r: dict, max_display: int = 400) -> str:
    t = r["totals"]
    lines = [f"# Trace scan: {Path(r['file']).name}", "",
             f"- language: {r['lang']}; units: {t['units']} ({'chars' if r['lang'] == 'zh' else 'words'}); "
             f"paragraphs: {t['paragraphs']}; sentences: {t['sentences']}",
             "- Signals only. Counts are not edit quotas; read every candidate in context."]
    lines += [f"- WARNING: {w}" for w in r.get("reliability_warnings", [])]
    lines += ["", "## Whole-text signals", "", "| signal | value |", "| --- | --- |"]
    keys = ["process_trace", "source_first", "negation_defense_per_k", "negation_unanchored", "hedge_sentences_per_k",
            "hedged_finding", "echo_share", "abstract_closer_share", "epigram_closers", "quotes", "quotes_per_k",
            "numbers_per_k", "code_tokens_per_k", "attributions_per_100_sentences", "abstract_terms_per_k", "lit_chain",
            "stance", "caveat_sentence_share", "topic_link_rate", "relation_marker_share", "short_sentence_share",
            "staccato_runs", "abstract_openers", "unguided_shifts", "conversion_frame_share",
            "relation_verbs_per_k", "inferential_per_k"]
    lines += [f"| {k} | {t[k]} |" for k in keys]
    lines.append(f"| case-selection move found in | {', '.join(r.get('case_selection_sections', [])) or 'none'} |")
    sl = r["sentence_length"]
    lines += [f"| sentence length mean / cv | {sl['mean']} / {sl['cv']} |",
              f"| citations cited once / distinct | {r['citations']['cited_once']} / {r['citations']['distinct_cited']} |",
              "", "Top abstract terms: " + ", ".join(f"{k}×{v}" for k, v in r["top_abstract_terms"]),
              "", "Repeated paragraph openings: " + (", ".join(f"{k}×{v}" for k, v in r["repeated_paragraph_openings"]) or "none"),
              "", "## By section", "",
              "| section | units | trace | neg/k | unanch. | closers e+a+epi | quotes | topic link | relation | staccato | attrib/100s |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name, m in r["sections"].items():
        lines.append(f"| {name} | {m['units']} | {m['process_trace']} | {m['negation_defense_per_k']} | {m['negation_unanchored']} | "
                     f"{m['echo_endings']}+{m['abstract_closers']}+{m['epigram_closers']} | {m['quotes']} | {m['topic_link_rate']} | "
                     f"{m['relation_marker_share']} | {m['staccato_runs']} | {m['attributions_per_100_sentences']} |")
    cands = r["candidates"]
    lines += ["", f"## Candidates ({len(cands)}; context review required)", ""]
    for c in cands[:max_display]:
        extra = ""
        if c["type"] == "negation_defense":
            extra = " [anchored]" if c.get("anchored") else " [UNANCHORED]"
        lines.append(f"- **{c['type']}**{extra} · {c['section']} ¶{c['paragraph']}: {c['excerpt']}")
    if len(cands) > max_display:
        lines.append(f"- … {len(cands) - max_display} more in JSON (all are used by the gate)")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan a manuscript for trace/defence/cohesion signals.")
    ap.add_argument("manuscript", type=Path)
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto")
    ap.add_argument("--abstract-terms", type=Path)
    ap.add_argument("--out-json", type=Path)
    ap.add_argument("--out-md", type=Path)
    ap.add_argument("--max-display", type=int, default=400)
    a = ap.parse_args()
    if not a.manuscript.is_file():
        ap.error(f"not found: {a.manuscript}")
    terms = None
    if a.abstract_terms:
        terms = [x.strip() for x in a.abstract_terms.read_text(encoding="utf-8").splitlines() if x.strip()]
    r = scan(a.manuscript, a.lang, terms)
    if a.out_json:
        a.out_json.parent.mkdir(parents=True, exist_ok=True)
        a.out_json.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    md = to_markdown(r, a.max_display)
    if a.out_md:
        a.out_md.parent.mkdir(parents=True, exist_ok=True)
        a.out_md.write_text(md, encoding="utf-8")
    if not a.out_json and not a.out_md:
        sys.stdout.reconfigure(encoding="utf-8")
        print(md)
    else:
        print(f"Scanned {a.manuscript.name}: {r['totals']['paragraphs']} paragraphs, {len(r['candidates'])} candidates. Signals only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
