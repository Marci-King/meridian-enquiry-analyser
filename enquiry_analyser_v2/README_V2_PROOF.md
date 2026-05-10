# Meridian Enquiry Analyser V2 Proof Brief

Meridian Enquiry Analyser V2 is a standalone Python proof artifact demonstrating retrieval-grounded workflow analysis, structured outputs, deterministic evals, retrieval-quality review, safety boundaries, failure-mode documentation, audit metadata, and human-review routing for fictional service-business enquiries.

It is separate from the main Meridian runtime and uses fictional data only.

## Quick Proof

Run:

```bash
python3 enquiry_analyser_v2/v2_analyser.py
python3 enquiry_analyser_v2/evals/run_evals.py
```

Expected eval result:

- 7/7 category accuracy
- 7/7 human-review trigger accuracy
- 7/7 retrieval-review accuracy

## Workflow

Fictional enquiry
-> business/service classification
-> local markdown guidance retrieval
-> retrieval-quality review
-> risk and missing-detail detection
-> human-review decision
-> structured JSON + Markdown output
-> deterministic eval report

## Why This Matters

Meridian V2 is not just an enquiry classifier. It demonstrates the bounded workflow pattern behind Meridian and Aegis: retrieve relevant guidance, structure messy input, identify risk and missing details, and route sensitive cases to human review rather than confident autonomous closure.

## Relationship To Aegis

Meridian is the lower-stakes proving ground for bounded AI workflows. It tests retrieval-grounded guidance, missing-detail capture, structured outputs, safer drafts, follow-up routing, and human review. Aegis applies the same accountability logic to higher-stakes operational environments where sign-off, auditability, and fail-closed review become more critical.

## What This Proves

- Local retrieval over markdown guidance
- Structured JSON workflow outputs
- Deterministic evals
- Retrieval-quality review
- Audit metadata
- Safety-boundary documentation
- Failure-mode documentation
- Human-review routing
- Bounded workflow architecture

## What It Does Not Prove

- Production readiness
- Clinical suitability
- Real customer use
- Autonomous customer messaging
- Full vector/semantic RAG
- Platform integration

## Truth Boundaries

- Fictional data only
- No real customer data
- No live model calls
- No production RAG claim
- No clinical validation
- No production classifier
- No WhatsApp, Booksy, Fresha, CRM, Instagram, or TikTok integration
- Not connected to the main Meridian runtime
- Human review remains required for sensitive cases

## Implementation Notes

- `retrieve_guidance.py` loads local Markdown files, splits them into heading-aware chunks, scores chunks by deterministic keyword overlap, and returns source filenames and chunk IDs.
- `v2_analyser.py` writes structured JSON to `outputs/analysed_enquiries_v2.json` and a reviewer-facing Markdown summary to `outputs/daily_summary_v2.md`.
- `evals/run_evals.py` writes a deterministic report to `evals/eval_report.md`.
- `retrieval_review` records whether guidance was found, assigns `low`, `medium`, or `high` confidence, and explains why the retrieved guidance was sufficient or insufficient.

## Human-Review Gates

Human review is required when:

- No local guidance is retrieved
- Retrieval confidence is low
- The enquiry is a sensitive clinic or treatment context
- The message asks for diagnosis, suitability, or guaranteed outcomes
- The message contains prompt-injection-like wording

Hospitality enquiries are intentionally separated from clinic safety logic while still using missing-detail checks and local guidance.
