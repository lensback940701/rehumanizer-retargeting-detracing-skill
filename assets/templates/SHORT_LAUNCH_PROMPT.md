# Short launch prompt (Stage 2)

Stage 1 fills the brackets and gives the user only the block below to paste
into a NEW conversation.

```text
/goal 请先完整读取 Goal 文件：[HANDOFF_DIR]/GOAL.md，再按其 P0 读取已安装的 `$rehumanizer-retargeting-detracing-skill/SKILL.md`（若环境不支持技能变量，读取 `<SKILL_ROOT>/SKILL.md`，SKILL_ROOT=[skill 安装根目录]）及 Goal 指定的 references，然后执行 Goal。你是 Stage 2 执行者：第一步按 Goal 第 1 节建立 Goal；靶点、保留锁和作废规则以 GOAL.md 为准，此前项目中的其他 Goal/prompt/style 规则不再约束本轮。BASELINE=[稿件绝对路径]；OUTPUT_ROOT=[新建输出目录绝对路径]。围绕已确认靶点回到原始材料，按 Goal 写明的改写强度（R1/R2/R3）改写，主张写到证据能支持且最有价值的程度，读完材料后复核一次靶点，先写后核，写成前后衔接的连贯文字，运行 trace_scan、defense_gate（及 sibling_overlap_check）并以改写消除 FAIL，最后一次改动后用 final_check 绑定最终文件；不编造、不违反匿名、不改源文件、不自增新规则、不运行终稿抛光或投稿。交付 GOAL.md 第 7 节全部文件后停止。
```
