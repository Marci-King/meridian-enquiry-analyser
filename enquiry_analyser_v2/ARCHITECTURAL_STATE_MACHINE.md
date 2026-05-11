# Meridian Enquiry Analyser V2 Architectural State Machine

This document describes the deterministic V2 proof workflow. It is a local proof artifact, not production infrastructure.

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
```

## States

### 1. Fictional Enquiry

The workflow starts from a fictional enquiry in `data/fictional_enquiries.json` or an eval case in `evals/eval_cases.json`.

### 2. Business And Service Classification

The analyser assigns a deterministic service category such as `jfades_prp`, `jfades_akn`, `cosy_mug_catering`, or `cosy_mug_delivery_collection`. Classification is simple keyword logic and is not a trained classifier.

### 3. Local Markdown Guidance Retrieval

The retriever loads local Markdown guidance, splits it into chunks, and scores chunks using keyword overlap. It returns source filenames, chunk IDs, scores, matched keywords, and snippets.

### 4. Retrieval-Quality Review

The analyser checks whether guidance was found and whether the retrieved guidance is specific enough for the business context. Confidence is one of `low`, `medium`, or `high`.

### 5. Risk And Missing-Detail Detection

The workflow detects deterministic risk flags such as prompt-injection-like wording, diagnosis requests, suitability requests, unsupported cure claims, and outcome-guarantee requests. It also records missing operational details needed for follow-up.

### 6. Human-Review Decision

If guidance is missing, retrieval quality is low, or the enquiry is sensitive, the workflow routes to human review rather than confident closure.

Sensitive cases include clinic or treatment contexts, diagnosis or suitability requests, guaranteed-outcome wording, unsupported cure wording, prompt-injection-like wording, and unclear business context.

### 7. Structured Outputs

The analyser writes structured JSON to `outputs/analysed_enquiries_v2.json` and a reviewer-facing Markdown summary to `outputs/daily_summary_v2.md`.

Each JSON item includes audit metadata showing the analyser version, local keyword retrieval mode, no live model usage, fictional data status, and whether a safety boundary was hit.

### 8. Deterministic Eval Report

The eval runner checks category selection, human-review routing, retrieval-review behavior, adversarial wording, hospitality separation, and missing-guidance fail-closed behavior. It writes `evals/eval_report.md`.

## Fail-Closed Principle

If guidance is missing, retrieval quality is low, or the enquiry is sensitive, the workflow routes to human review rather than confident closure.

## Scope Boundary

This is a proof artifact for review. It does not call outside services, does not use customer data, does not add integrations, and does not replace professional judgement.
