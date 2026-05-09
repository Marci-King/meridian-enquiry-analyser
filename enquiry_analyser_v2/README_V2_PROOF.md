# Meridian Enquiry Analyser V2 Proof Brief

Meridian Enquiry Analyser V2 is an additive proof artifact that sits beside V1. It shows how fictional service enquiries can be routed through local guidance retrieval, a retrieval-quality review, structured output, lightweight evals, and explicit safety documentation.

V1 remains the simple deterministic analyser. V2 keeps that truth boundary and adds a separate layer for reviewers to see progression without changing the original script or outputs.

## What Changed From V1 To V2

- Retrieval grounding from local Markdown guidance.
- A `retrieval_review` field that checks whether retrieved guidance is sufficient before recommending a next step.
- Structured JSON output with service category, risk flags, missing details, retrieved snippets, human-review routing, and next-step guidance.
- Lightweight evals for category selection, human-review triggers, prompt-injection-like wording, hospitality separation, and missing guidance.
- Explicit safety and failure-mode documentation.

## Meridian And Aegis

Meridian is my lower-stakes proving ground for bounded AI workflows. It tests patterns such as retrieval-grounded guidance, missing-detail capture, structured outputs, safer drafts, follow-up queues, and human review. Aegis applies the same accountability logic to higher-stakes operational environments where human sign-off, auditability, and fail-closed review become more critical.

## Lightweight Retrieval

`retrieve_guidance.py` loads local Markdown files, splits them into heading-aware chunks, scores chunks by simple keyword overlap, and returns the top snippets with source filenames and chunk IDs.

This is a deterministic keyword-based proof artifact. It is not a production retrieval system, does not use embeddings, does not use a vector database, and does not call external services.

## Retrieval Review

The `retrieval_review` field is a lightweight retrieval-quality check inspired by corrective RAG patterns. It records whether guidance was found, assigns a simple `low`, `medium`, or `high` confidence label, and explains why the retrieved guidance was considered sufficient or insufficient.

This is not a production implementation of corrective or self-reflective RAG research patterns. It does not rewrite or repair its own outputs; it fails closed to human review when guidance is missing, weak, generic, or sensitive.

Example field:

```json
{
  "retrieval_review": {
    "guidance_found": true,
    "retrieval_confidence": "low",
    "review_note": "Retrieved guidance is weak, generic, or not clearly tied to the business context."
  }
}
```

## Structured Outputs

Each analysed enquiry includes:

- `enquiry_id`
- `business`
- `message`
- `service_category`
- `risk_flags`
- `missing_details`
- `retrieved_guidance`
- `retrieval_review`
- `human_review_required`
- `recommended_next_step`

The JSON output is written to `outputs/analysed_enquiries_v2.json`. The human-readable review summary is written to `outputs/daily_summary_v2.md`.

## Human-Review Gates

Human review is required when:

- No local guidance is retrieved.
- Retrieval confidence is low.
- The enquiry is a sensitive JFades clinic or treatment context.
- The message asks for diagnosis, suitability, or guaranteed outcomes.
- The message contains prompt-injection-like wording.

Cosy Mug hospitality enquiries are intentionally separated from clinic safety logic, while still using missing-detail checks and local guidance.

## Evals

The eval suite in `evals/run_evals.py` uses fictional cases to test:

- Correct service category selection.
- Human review for high-risk clinic and treatment enquiries.
- Human review for prompt-injection-like wording.
- Hospitality enquiries staying outside clinic safety logic.
- Human review when retrieval is missing or low confidence.

The report is written to `evals/eval_report.md`.

## What Is Mocked Or Out Of Scope

- Fictional data only.
- No customer records.
- No model calls.
- No external APIs.
- No embeddings or vector database.
- No clinical validation.
- No autonomous customer-facing use.
- No integration with messaging, booking, CRM, or social platforms.

## Run

From the repository root:

```bash
python3 enquiry_analyser_v2/v2_analyser.py
python3 enquiry_analyser_v2/evals/run_evals.py
```
