# Meridian Enquiry Analyser V2 Eval Report

Deterministic proof evals using fictional cases only.

## Results

- Total cases: 12
- Category accuracy: 12/12 (100.0%)
- Human-review trigger accuracy: 12/12 (100.0%)
- Retrieval-review accuracy: 12/12 (100.0%)

## Expected vs Actual

| Case | Expected category | Actual category | Expected human review | Actual human review | Expected retrieval | Actual retrieval | Pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVAL-001 | jfades_prp | jfades_prp | True | True | True / high | True / high | True |
| EVAL-002 | jfades_akn | jfades_akn | True | True | True / high | True / high | True |
| EVAL-003 | jfades_prp | jfades_prp | True | True | True / high | True / high | True |
| EVAL-004 | cosy_mug_catering | cosy_mug_catering | False | False | True / high | True / high | True |
| EVAL-005 | cosy_mug_opening_hours | cosy_mug_opening_hours | False | False | True / high | True / high | True |
| EVAL-006 | general | general | True | True | False / low | False / low | True |
| EVAL-007 | cosy_mug_catering | cosy_mug_catering | False | False | True / high | True / high | True |
| EVAL-008 | jfades_prp | jfades_prp | True | True | True / high | True / high | True |
| EVAL-009 | jfades_hair_loss | jfades_hair_loss | True | True | True / high | True / high | True |
| EVAL-010 | jfades_akn | jfades_akn | True | True | True / high | True / high | True |
| EVAL-011 | cosy_mug_catering | cosy_mug_catering | False | False | True / high | True / high | True |
| EVAL-012 | cosy_mug_delivery_collection | cosy_mug_delivery_collection | False | False | True / high | True / high | True |

## Known Limitations

- Keyword overlap can miss paraphrases and can over-rank chunks that share surface words.
- The confidence labels are deterministic proof labels, not calibrated probabilities.
- The eval cases are small and fictional; they demonstrate intended boundaries rather than broad coverage.
- Human-review routing is deliberately conservative for clinic and treatment contexts.