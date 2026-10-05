# Goal：全文路线纠偏——重新锚定靶点、恢复活人感与连贯性、去除流程痕迹

> 填写说明（Stage 1 删除本段）：替换全部 `{{…}}`；用作者的工作语言。本 Goal 应比上一版 Goal 更短、禁止项更少；篇幅用在靶点、证据定位和各节任务上。只有作者确认 RETAIN 的锁才写入第 4 节。

## 0 元数据

- Goal ID：`{{GOAL_ID}}`
- Target skill：本地 `rehumanizer-retargeting-detracing-skill`（Stage 2）
- 改写强度：`{{R1|R2|R3}}`；靶点状态：`{{CONFIRMED_TARGET|PROVISIONAL_TARGET}}`
- 本 Goal 替代此前所有 Goal、prompt 和 style card 中关于措辞、流程、引语、命名、篇幅、结构的规则；仍有效的只有第 4 节。

## 1 第一项动作

先读完本 Goal 再做其他启动动作；不得把助手记忆、聊天历史或本 Goal 输入以外的文件当作事实来源。若环境提供 `create_goal`/`get_goal`/`update_goal`，先建立 Goal（含 Goal ID、BASELINE 与第 7 节交付）；否则在 `OUTPUT_ROOT/goal_state.json` 记录进度。完整阅读 `<SKILL_ROOT>/SKILL.md`、`references/01`–`05`、`07` 与 `08`、`06` 中 `{{PAPER_TYPE}}` 一节，以及 Stage 1 文件。

## 2 靶点（两层）

**理论靶点**（全文主张；去掉案例仍成立；须写出主概念承诺的结果，例如“激活”了什么，而不只是过程或用法的多样）：

> {{THEORETICAL_TARGET}}

- 理论对手（照原意，取推进/补足姿态）：{{THEORETICAL_ADVERSARY}}
- 适用条件（讨论中作为理论边界写一次）：{{PORTABILITY_CONDITIONS}}

**实证机制层**：

> {{MECHANISM_STATEMENT}}

- 主张表（类型/范围/支撑，见 references/01）：{{CLAIM_TABLE}}
- Stage 1 抽查材料（暂定判断，P2b 复核）：{{KEY_PASSAGES_WITH_LOCATORS}}
- 要反转的退让：{{REVERSIBLE_RETREATS}}；保留的退让（证据所迫）：{{EVIDENCE_FORCED_RETREATS}}
- 题名/关键词承诺中尚未兑现的部分：{{PROMISE_GAPS}}
- 研究问题（保持理论高度，不得被防御写作降格）：{{RESEARCH_QUESTIONS}}

## 3 输入

- `BASELINE`（只读）：{{BASELINE_PATH}}
- `RAW_SOURCE_ROOTS`（只读，可回读、可新增经核对的引用；无则写 none）：{{RAW_SOURCE_ROOTS}}
- `VOICE_REFERENCES`（同语言、已转为 md/docx）：{{VOICE_REFERENCES}}
- `SIBLING_PAPERS`（如有）：{{SIBLING_PAPERS}}
- Stage 1 文件：{{HANDOFF_DIR}}
- 期刊与篇幅：{{TARGET_JOURNAL}}；{{LENGTH_POLICY}}（默认：不超过期刊上限；无上限信息时不超过 baseline 的 115%，超出部分交给终稿抛光）
- 文献：{{LITERATURE_ROOT}}；{{LIT_ADDITION_POLICY}}（默认不新增，可删装饰性引用）
- 案例导入可用的背景来源（宏观与区域事实只能来自这里）：{{CONTEXT_SOURCES}}
- `PAPER_TYPE`：{{PAPER_TYPE}}；`OUTPUT_ROOT`（新建）：{{OUTPUT_ROOT}}

## 4 保留锁（仅此几条）

1. 不编造：事实、引语、数字、事件、动机、情绪、结果、因果、文献观点均须有可定位来源。
2. 匿名与伦理：{{ANONYMIZATION_RULES}}
3. 原件保护：不修改、移动、覆盖 BASELINE、原始材料、旧版本与任何 skill。
4. 作者已定事项：{{AUTHOR_LOCKS}}
5. 引语：原样引用，后接分析性解读；删除有来源的原话须在 route memo 写明理由（可用更有力的原话替换较弱的）。{{QUOTE_RULES}}
6. {{OTHER_RETAINED_LOCKS}}

已作废（作者已确认）：{{RETIRED_RULES_SHORTLIST}}

## 5 本轮权限

- 回到原始材料补入情境、处境、原话和数字（逐字核对，登记于 living_material_bank）。
- 按第 6 节的强度分支改写；可重排小节、改写标题与摘要（{{STRUCTURE_LIMITS}}）。
- 主张写到证据能支持、且最有价值的程度；不为“更高”而升级。
- 情境化称谓指称行动者，编码只留在出处括注；同一来源的连续段落只标注一次。{{PSEUDONYM_POLICY}}
- 删除装饰性引用、流程痕迹、复述式收尾、稻草人否定和重复免责；**保留**说明真实逻辑关系的连接词与对具名观点的对照。
- 使用作者立场句。

## 6 执行步骤（按强度分支）

| 步骤 | R1 | R2 | R3 |
| --- | --- | --- | --- |
| P2 活材料库范围 | 待重写段落 | 实证核心 | 全文 |
| P3 骨架范围 | 各节开头与讨论 | 实证核心与框架 | 新提纲 |
| P4 改写范围 | 摘要、引言、各节开头、讨论、结论与最弱段落 | R1 范围＋实证核心＋理论 | 全文 |

1. **P0 冻结**：把全部输入的 path,sha256 写入 `source_manifest.csv`；复制 BASELINE 至 `working/`。
2. **P1 路线合同**：`route_contract.md`（靶点、主张表、对手、各节任务、保留锁）；可暂用 Stage 1 的来源 ID，P2 后换成 bank ID。PROVISIONAL_TARGET 时写完即停，等作者确认。
3. **P2 活材料库与材料升级**：`registers/living_material_bank.csv`。逐条主张回原始材料寻找比基线所用材料更有力的原话、数字与转折，在 `registers/material_upgrade.csv` 记录保留、替换或新增的决定及理由。只保留基线材料也须写明理由。
4. **P2b 靶点复核（一次）**：读完材料后寻找最强反证，决定保持、收窄或重塑靶点，并记入路线合同。若材料撑不起任何版本，停在 `HOLD_TARGET_EXCEEDS_EVIDENCE`，同时给出最佳可支持的替代靶点。
5. **P3 骨架与章节结构图**：`spine_and_outline.md`。每节写明：
   - 进入方式；
   - 主张在哪里出现；
   - 焦点路径（每次转移的理由）；
   - 贯穿线索；
   - 出口与交接。
   案例章写出背景阶梯和案例选择理由（references/08）。
6. **P4 改写**：先材料与论证，再章节结构与连贯性（按结构图写，references/07、08）；先写后核；按 `voice_profile.md` 校准语气。
7. **P5 门禁**：
   ```text
   python <SKILL_ROOT>/scripts/trace_scan.py <revised> --out-json qa/trace_revised.json --out-md qa/trace_revised.md
   python <SKILL_ROOT>/scripts/defense_gate.py --baseline working/<baseline> --revised <revised> {{--reference ...}} --register registers/added_caution_register.csv --route-memo route_memo.md --config {{HANDOFF_DIR}}/gate_config.json --paper-type {{PAPER_TYPE}} {{--core-term <route_contract 中的核心概念，每个一项>}} --out-json qa/defense_gate.json --out-md qa/defense_gate.md
   python <SKILL_ROOT>/scripts/sibling_overlap_check.py --manuscript <revised> --sibling <每篇一个> --out-md qa/sibling_overlap.md --out-json qa/sibling_overlap.json
   ```
   - FAIL 以改写解决，或用具体的登记/备忘条目解决；不得修改 gate_config.json。
   - 警告结合上下文判断，不当作配额。
   - 压下一个警告后，查 W17：被压下的套路常换成一个新的标签词回来（如某个名词出现在一半以上段落）。换词不算修复，要写出谁做了什么。
   - 最多三轮；仍 FAIL 且涉及靶点本身时停在 `HOLD_DEFENSE_GATE`。
8. **P6 写后核验（一次性）**：引语、数字、日期、归属、引用功能。
9. **P7 冷读＋结构通读＋连贯性通读**：
   - 按 references/02 的冷读问题读一遍；
   - 再按 references/08 只读各节开头、各段首句与各节结尾（结构通读）；
   - 再按 references/07 逐段做 flow read：机制是否靠“进入/接入/参与构成”之类占位动词、成串的“由此/因此”或反复出现的标签词来交代（T17/W16/W17）；改成写谁做了什么。
   - 修复发现的问题。
   - 同一执行者阅读须如实说明。
10. **P8 最终绑定**：最后一次改动并导出 md/docx 之后，对最终 docx 与 md 各跑一次 P5 门禁（报告分别为 qa/defense_gate.json 与 qa/defense_gate_md.json），然后运行：
    ```text
    python <SKILL_ROOT>/scripts/final_check.py --manuscript manuscripts/manuscript_rerouted.docx --manuscript manuscripts/manuscript_rerouted.md --gate-json qa/defense_gate.json --gate-json qa/defense_gate_md.json --overlap-json qa/sibling_overlap.json --semantic-review qa/sibling_semantic_review.md --result-json rrd_result.json --write-result --source-manifest source_manifest.csv --out-md qa/final_check.md --out-json qa/final_check.json
    ```
    - 不通过则修正后重跑；无法通过时停在 `HOLD_FINAL_BINDING`。
    - P6/P7 之后的改动只需重核受影响内容，并重跑机器门禁。

## 7 交付物（OUTPUT_ROOT）

- `manuscripts/manuscript_rerouted.md` 与 `.docx`
- `route_contract.md`、`spine_and_outline.md`、`voice_profile.md`、`route_memo.md`（含删除的有来源材料及理由）
- `registers/`
- `qa/`（含 final_check）
- `source_manifest.csv`
- `author_queries.md`
- `handoff_to_final_polish.md`
- `rrd_result.json`（final_hashes 与 sources_unchanged 由 final_check 结果填写，不得预设）

## 8 完成标准（仅适用于“完成”状态）

1. final_check PASS：最终文件、门禁报告与 rrd_result 哈希一致；源文件未变。
2. 第一页可读出理论靶点与对手；各实证小节有一句站得住的主张。
3. 主张表中每条主张都有支撑；凡与 baseline 不同之处，理由都写明。
4. defense_gate 无 FAIL；警告已在 route memo 中逐条说明处理或保留理由。
5. 冷读问题与 flow read 均已完成并修复。
6. 无编造、无匿名违规、无未登记的新增谨慎表述。

完成状态：`ROUTE_CORRECTED_READY_FOR_FINAL_POLISH` 或 `ROUTE_CORRECTED_WITH_AUTHOR_QUERIES`。

暂停状态（不是成功）：
- `HOLD_TARGET_UNCONFIRMED`
- `HOLD_SOURCE_ACCESS`
- `HOLD_TARGET_EXCEEDS_EVIDENCE`
- `HOLD_DEFENSE_GATE`
- `HOLD_FINAL_BINDING`

## 9 停止条件

交付后立即停止。不运行终稿抛光，不投稿、不上传、不外联、不新开 Goal。执行中不得自行增设禁止性规则、预算或模板；认为需要时写入 author_queries.md。
