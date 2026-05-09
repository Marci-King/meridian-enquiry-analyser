# ADR 005: Human Review For Sensitive Enquiries

## Status

Accepted

## Context

Meridian supports bounded workflow handling for fictional enquiries. Some enquiries involve clinic, treatment, diagnosis, suitability, outcome-guarantee, or adversarial wording that should not be treated as standard automated follow-up.

## Decision

Require human review for sensitive enquiries.

V2 routes sensitive JFades clinic and treatment contexts, diagnosis requests, suitability questions, outcome-guarantee requests, prompt-injection-like wording, missing guidance, and low-confidence retrieval to human review.

## Reason

Meridian supports professional judgement and should not replace it.

## Consequences

- Sensitive cases fail closed rather than moving to confident closure.
- Human reviewers remain responsible for professional judgement.
- Hospitality enquiries can still use standard missing-detail follow-up when retrieval is sufficient.
- The proof artifact remains clear about its safety boundary.
