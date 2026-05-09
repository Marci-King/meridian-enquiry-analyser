# Meridian Enquiry Analyser V2 Failure Modes

## Unsafe Treatment Advice

- Risk: The workflow could appear to answer a clinic or treatment question too confidently.
- Current mitigation: JFades diagnosis, suitability, outcome, and treatment-context enquiries require human review.
- Remaining limitation: Keyword rules may miss unusual phrasing.
- Future improvement: Add broader test coverage and formal review by qualified operators before any operational use.

## Hallucinated Service Details

- Risk: The workflow could invent opening hours, prices, availability, or service claims not present in local guidance.
- Current mitigation: Outputs recommend owner review or follow-up rather than inventing missing details.
- Remaining limitation: The Markdown knowledge base may be incomplete.
- Future improvement: Add source ownership, review dates, and approval status to each guidance file.

## Prompt Injection

- Risk: A message could instruct the system to ignore rules or guarantee an outcome.
- Current mitigation: Prompt-injection-like wording is flagged and routed to human review.
- Remaining limitation: Simple patterns may not catch every adversarial wording.
- Future improvement: Expand adversarial eval cases and add stronger boundary checks.

## Human Review Bypass

- Risk: Sensitive enquiries could be marked as standard follow-up.
- Current mitigation: Clinic and treatment contexts fail closed to human review, even when guidance is retrieved.
- Remaining limitation: Business or service misclassification can still occur.
- Future improvement: Add independent checks for business context, category confidence, and reviewer assignment.

## Wrong Business Context

- Risk: JFades guidance could be applied to Cosy Mug, or hospitality guidance could be applied to a clinic enquiry.
- Current mitigation: Retrieval review checks for business-specific sources before assigning higher confidence.
- Remaining limitation: Keyword overlap alone can retrieve a generic chunk.
- Future improvement: Add explicit business metadata and stricter source filters.

## Privacy And Data Risk

- Risk: Real customer information could be placed into proof data by mistake.
- Current mitigation: The proof dataset is fictional and local.
- Remaining limitation: The code does not automatically detect personal data.
- Future improvement: Add data-review checklists and redaction tests before wider demonstrations.

## Low-Confidence Or Missing Retrieval

- Risk: The analyser could proceed without enough local guidance.
- Current mitigation: Missing guidance and low-confidence retrieval require human review.
- Remaining limitation: The confidence labels are deterministic proof labels, not measured certainty.
- Future improvement: Add richer evals and documented thresholds for each business context.
