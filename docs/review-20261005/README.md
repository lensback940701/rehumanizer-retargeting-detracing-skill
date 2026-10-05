# RRD v3.4 review and development-test records

- `DEVELOPMENT_TEST_LOG.zh-CN.md`: 中文开发与回归测试记录。
- `DEVELOPMENT_TEST_LOG.en.md`: Parallel English development and regression test record.
- `REVIEW.zh-CN.md`: 设计判断、源码定位及工程边界问题。
- `benchmark_history.developer_reported.json`: 开发者报告的四轮评分与回退记录；缺失字段为null。
- `REFERENCE_NOTES.md`: Evidence provenance and official-method references.
- `evidence/`: Completed logs, summaries, source diff and reproducible contract probes.

No skill files were modified. This is a documentation and evidence package, not a patched skill release.
The synthetic DOCX fixture is deliberately not included; `probe_v34.py` recreates it. Probe reproduction requires Python and python-docx.

## Reproduce packaged tests from the skill root

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python -m unittest -v test_rrd_scripts.ScanTests test_rrd_scripts.ToolTests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python -m unittest -v test_rrd_scripts.GateTests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python -m unittest -v test_rrd_scripts.V3Tests test_rrd_scripts.V31Tests test_rrd_scripts.V32Tests
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests python -m unittest -v test_rrd_scripts.V33Tests test_rrd_scripts.V34Tests
```

## Reproduce additional contract probes

```bash
python evidence/probe_v34.py --skill-root /path/to/rehumanizer-retargeting-detracing-skill --out /path/to/probe-results
```

The probe runner reports observations and exits successfully when execution completes. Consult `summary.json` for the expected-versus-observed results; its process exit is not a declaration that the skill met every proposed requirement.
