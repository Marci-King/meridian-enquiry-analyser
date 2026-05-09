# ADR 004: Retrieval-Grounded Workflow Proof

## Status

Accepted

## Context

Meridian V1 demonstrates deterministic enquiry analysis using fictional data. V2 needs to show progression toward workflow outputs that are grounded in explicit local business and safety guidance before recommending next steps.

## Decision

Use retrieval before workflow output.

The V2 proof loads local Markdown guidance, retrieves relevant snippets through deterministic keyword overlap, and includes the retrieved sources in each structured output.

## Reason

AI workflow systems should be grounded in business and safety guidance before producing structured workflow outputs.

## Consequences

- Reviewers can see which local guidance influenced each output.
- Missing or weak retrieval can fail closed to human review.
- The proof remains simple, deterministic, and inspectable.
- The approach is not a production retrieval system and does not use external services, embeddings, or vector databases.
