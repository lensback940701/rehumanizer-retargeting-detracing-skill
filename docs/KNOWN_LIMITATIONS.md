# Known limitations / 已知限制

The following observations come from the archived 2026-10-05 review. Packaging did not repair them or rerun the manuscript evaluation.

| ID | Acceptance issue / 验收问题 |
| --- | --- |
| A01 | Every final file needs its own matching gate report; coverage was not fully enforced. / 多份最终文件未强制逐一匹配报告。 |
| A02 | A header-only source manifest could certify unchanged sources. / 仅表头的清单仍可能通过来源保护检查。 |
| A03 | Undefined nonempty workflow states could be accepted. / 未定义的非空状态仍可能被接受。 |
| A04 | Registering one cue type could authorize another new cue in the same sentence. / 同句不同新增表达类型的登记不够独立。 |
| A05 | A missing explicitly specified configuration could silently fall back to defaults. / 显式配置缺失时可能静默回落到默认值。 |
| A06 | `final_check` could change from an object to a string in the result JSON. / 结果字段可能发生结构变化。 |

The dashboard groups A03 and A05 into one thematic row; its five rows are not a count of all observations. The 47 passing packaged tests do not cancel these findings.

## Evidence boundaries

- One manuscript produced the reported scores 39, 41, 42 and 37 across development checkpoints. The rubric maximum, model settings, repeat counts and historical commit hashes were not supplied.
- The selected 42-point checkpoint is a developer-reported selection, not a verified stable average or a cross-manuscript reliability estimate.
- Before/after graphics are conceptual, not empirical comparisons. The cyber image is branding, not a claim about capabilities such as eliminating bias.
- Source protection, ethics, anonymity, justified scope conditions and contradictory evidence remain mandatory.
- Re-check the source manifest, every final-file hash and gate report manually until acceptance hardening is completed.

完整方法、原始日志与测试探针见 [review-20261005](review-20261005/README.md)。
