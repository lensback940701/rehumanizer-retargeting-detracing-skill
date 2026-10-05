# Handoff to hq-final-polish-harness

This manuscript completed RRD route correction. For the final-polish Goal:

- `BASELINE` for final polish: `{{OUTPUT_ROOT}}/manuscripts/manuscript_rerouted.docx` (SHA-256 {{hash}})
- Authority for contribution hierarchy and claim ceiling: `route_contract.md` (the claim table is the ceiling; final polish keeps claims same-or-narrower **relative to this contract**, not to any earlier draft).
- Final binding: `qa/final_check.md` (manuscript hashes = gate and overlap reports = rrd_result.json).
- Protected new material: `registers/living_material_bank.csv` items used in the text (quotes, numbers, actor descriptions). Treat them as protected content.
- Registered cautions: `registers/added_caution_register.csv`. Final polish should not add hedges, negation-defences or source-handling notes beyond these; if it believes one is needed, raise an author query.
- Retired rules (do not reintroduce): {{list}}
- Retained locks: {{list}}
- Defense gate status: {{PASS / PASS_WITH_WARNINGS}} (`qa/defense_gate.md`). Suggest re-running `defense_gate.py` with this manuscript as baseline after final polish to confirm no re-defensification.
- Suggested `NOUN_STACK_MODE`: {{scan_only | integrated_cleanup}} (detracing already reduced abstract stacks; keep cleanup light).
- Word count vs cap: {{count}} / {{cap}} ({{counting basis or NOT_VERIFIED}}). Over-cap amount for final polish to resolve: {{n}}.
- Open author queries: {{list or none}}
