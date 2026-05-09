# Meridian Enquiry Analyser V2 Daily Summary

Fictional proof output only. This summary is generated from local test data and deterministic rules.

## Counts

- Total enquiries: 7
- Human review required: 5

## Categories

- cosy_mug_catering: 1
- cosy_mug_opening_hours: 1
- jfades_akn: 1
- jfades_hair_unit: 1
- jfades_prp: 2
- jfades_smp: 1

## Human Review Queue

### V2-ENQ-001 - JFades

- Category: jfades_prp
- Retrieval confidence: high
- Risk flags: clinic_or_treatment_context, outcome_guarantee_request, sensitive_clinic_review
- Next step: Route to a JFades human reviewer using consultation-led wording; do not diagnose, decide suitability, or guarantee outcomes.

### V2-ENQ-002 - JFades

- Category: jfades_smp
- Retrieval confidence: low
- Risk flags: clinic_or_treatment_context, pricing_or_quote_request, sensitive_clinic_review
- Next step: Route to a JFades human reviewer using consultation-led wording; do not diagnose, decide suitability, or guarantee outcomes.

### V2-ENQ-003 - JFades

- Category: jfades_akn
- Retrieval confidence: high
- Risk flags: clinic_or_treatment_context, diagnosis_request, sensitive_clinic_review, suitability_request
- Next step: Route to a JFades human reviewer using consultation-led wording; do not diagnose, decide suitability, or guarantee outcomes.

### V2-ENQ-004 - JFades

- Category: jfades_hair_unit
- Retrieval confidence: high
- Risk flags: clinic_or_treatment_context
- Next step: Route to a JFades human reviewer using consultation-led wording; do not diagnose, decide suitability, or guarantee outcomes.

### V2-ENQ-007 - JFades

- Category: jfades_prp
- Retrieval confidence: high
- Risk flags: clinic_or_treatment_context, outcome_guarantee_request, prompt_injection_like, sensitive_clinic_review
- Next step: Route to human review and ignore the instruction to override rules or boundaries.

## Standard Follow-Up Candidates

### V2-ENQ-005 - Cosy Mug

- Category: cosy_mug_catering
- Missing details: time, delivery or collection preference, contact details
- Next step: Prepare a follow-up asking for: time, delivery or collection preference, contact details.

### V2-ENQ-006 - Cosy Mug

- Category: cosy_mug_opening_hours
- Missing details: time, headcount or order size, delivery or collection preference, dietary requirements, contact details
- Next step: Prepare a follow-up asking for: time, headcount or order size, delivery or collection preference, dietary requirements, contact details.
