# Meridian Enquiry Analyser V2 Architectural State Machine

This document explains the deterministic state-machine pattern behind Meridian Enquiry Analyser V2. It is written for review of the proof artifact, not as production infrastructure documentation.

## State Flow

```text
Fictional enquiry
-> business/service classification
-> local markdown guidance retrieval
-> retrieval-quality review
-> risk and missing-detail detection
-> human-review decision
-> structured JSON + Markdown output
-> deterministic eval report
-> unit tests / schema checks
```

## Fail-Closed Principle

"If guidance is missing, retrieval quality is low, or the enquiry is sensitive, the workflow routes to human review rather than confident closure."

This is the core safety pattern in V2. The analyser can structure an enquiry, retrieve local guidance, record risk flags, and recommend the next review step. It should not treat uncertain or sensitive cases as confidently resolved.

## States

### 1. Input Received

What it does:

- Reads fictional enquiry data from local JSON files.
- Accepts the message, enquiry ID, and business label already present in the fictional dataset.
- Keeps the data boundary explicit: no real customer data is used.

Movement trigger:

- Once a fictional enquiry record is loaded, the workflow moves to business and service classification.

Human-review trigger:

- If the business context is unclear later in the workflow, the case should fail closed to human review.

### 2. Business / Service Classification

What it does:

- Identifies the likely business context and service category using deterministic keyword rules.
- Example categories include `jfades_prp`, `jfades_akn`, and `cosy_mug_catering`.
- Keeps JFades clinic or treatment contexts separate from Cosy Mug hospitality contexts.

Movement trigger:

- Once a category is assigned, that category is used to shape retrieval, missing-detail checks, risk flags, and human-review rules.

Human-review trigger:

- Clinic or treatment categories are treated conservatively.
- Ambiguous hair-loss, AKN, diagnosis, suitability, or guaranteed-outcome wording should remain eligible for human review even if a category is found.

### 3. Local Guidance Retrieval

What it does:

- Retrieves relevant Markdown guidance from `knowledge_base/`.
- Splits local Markdown into small chunks.
- Scores chunks with keyword-overlap retrieval only.
- Returns source filenames, chunk IDs, overlap scores, matched keywords, and short snippets.

Movement trigger:

- The workflow moves to retrieval-quality review after the top local guidance chunks are returned.

Boundary:

- Not vector search.
- Not production RAG.
- No outside services are called.

### 4. Retrieval-Quality Review

What it does:

- Checks whether relevant guidance was found.
- Assigns deterministic confidence: `low`, `medium`, or `high`.
- Records a review note explaining why the retrieved guidance is considered sufficient or insufficient.

Movement trigger:

- If guidance is found and confidence is not low, the workflow continues to risk and missing-detail detection.
- If guidance is missing or weak, the workflow still records the case but routes it toward human review.

Human-review trigger:

- Missing guidance requires human review.
- Low-confidence retrieval requires human review.
- Generic guidance that is not clearly tied to the business context should not support confident closure.

### 5. Risk and Missing-Detail Detection

What it does:

- Flags missing details needed for a useful owner follow-up.
- Flags sensitive wording.
- Flags prompt-injection-like wording.
- Flags treatment suitability, diagnosis, guaranteed outcome, and unsupported cure risks.

Movement trigger:

- Once missing details and risk flags are recorded, the workflow moves to the human-review decision.

Human-review trigger:

- Diagnosis requests.
- Treatment suitability questions.
- Guaranteed outcome wording.
- Unsupported cure wording.
- Prompt-injection-like wording.
- Sensitive clinic or treatment contexts.

### 6. Human-Review Decision

What it does:

- Decides whether the case can be prepared as a standard follow-up or must be reviewed by a person.
- Combines category, retrieval review, and risk flags.
- Preserves the boundary that Meridian supports judgement rather than replacing it.

Movement trigger:

- Once the decision is made, the workflow writes structured outputs with the recommended next step.

Human-review trigger:

- Sensitive clinic or treatment enquiries require human review.
- Low-confidence retrieval requires human review.
- Prompt-injection-like wording requires human review.
- Missing guidance requires human review.
- The workflow should not confidently close these cases.

Low-confidence retrieval behavior:

- The case is kept in the structured output.
- `retrieval_review.retrieval_confidence` remains `low`.
- `human_review_required` is set to `true`.
- The recommended next step routes to human review instead of confident closure.

Sensitive clinic/treatment behavior:

- JFades PRP, SMP, AKN, hair unit, hair-loss, diagnosis, suitability, and guaranteed-outcome cases are routed to human review.
- Retrieved guidance can support the reviewer, but it does not remove the human-review requirement.

Prompt-injection-like behavior:

- Instructions to ignore rules, override boundaries, or guarantee outcomes are flagged.
- The workflow preserves the safety boundary and routes the case to human review.

### 7. Structured Output

What it does:

- Writes JSON output to `outputs/analysed_enquiries_v2.json`.
- Writes a Markdown summary to `outputs/daily_summary_v2.md`.
- Includes risk flags, missing details, retrieved guidance, retrieval review, metadata, human-review status, and recommended next step.

Movement trigger:

- Once outputs are written, the artifact can be checked by the deterministic eval suite.

Output fields include:

- `enquiry_id`
- `business`
- `message`
- `service_category`
- `risk_flags`
- `missing_details`
- `retrieved_guidance`
- `retrieval_review`
- `metadata`
- `human_review_required`
- `recommended_next_step`

### 8. Eval Report And Engineering Checks

What it does:

- Runs deterministic eval cases from `evals/eval_cases.json`.
- Checks category routing, human-review triggers, and retrieval-review behaviour.
- Includes lightweight adversarial cases for prompt-injection-like wording and boundary-sensitive clinic enquiries.
- Writes `evals/eval_report.md`.
- Runs standard-library unit tests for routing, retrieval, safety flags, and metadata consistency.
- Uses `schemas.py` to document the structured output contract.

Movement trigger:

- The eval report, unit tests, and schema contract are the review checkpoints for this proof artifact.

Human-review trigger coverage:

- The evals check that sensitive clinic cases, low-confidence or missing retrieval, and prompt-injection-like wording route to human review.
- Hospitality examples check that Cosy Mug enquiries do not accidentally trigger clinic safety logic.

## Relationship to Aegis

Meridian V2 tests the bounded workflow pattern in fictional service-business enquiries. Aegis applies the same logic to high-pressure operational scenarios: retrieve relevant context, identify missing information, route sensitive cases to human review, and avoid confident closure when accountability is unclear.

## What The System Does Not Do

- It does not diagnose conditions.
- It does not decide treatment suitability.
- It does not guarantee outcomes.
- It does not send autonomous customer-facing messages.
- It does not invent business facts when guidance is missing.
- It does not call outside services.
- It does not replace human review for sensitive cases.

## Truth Boundaries

- Fictional data only.
- No live model calls.
- No real customer data.
- No production RAG.
- No clinical validation.
- No autonomous customer-facing messaging.
- No platform integrations.
- Not connected to the main Meridian runtime.
