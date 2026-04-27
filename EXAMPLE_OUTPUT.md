x# Example Output

## Raw Enquiry

```json
{
  "id": "ENQ-005",
  "source": "Instagram DM",
  "text": "I saw your PRP post for thinning hair. Can you guarantee it will work?"
}
```

## Analysed JSON Object

```json
{
  "id": "ENQ-005",
  "source": "Instagram DM",
  "original_text": "I saw your PRP post for thinning hair. Can you guarantee it will work?",
  "category": "clinic_consultation",
  "interest_area": "PRP",
  "missing_details": [
    "timeline",
    "preferred contact",
    "optional photos",
    "consultation availability"
  ],
  "human_review_required": true,
  "review_reason": "clinic consultation review; guarantee / outcome boundary",
  "human_owner": "clinic consultation lead",
  "suggested_next_step": "route to consultation review before giving advice",
  "owner_note": "Route to clinic consultation lead. Interest area: PRP. Reason: clinic consultation review; guarantee / outcome boundary. Missing details: timeline, preferred contact, optional photos, consultation availability.",
  "truth_boundary": "Static local analysis using fictional demo data only. No live model call, no real customer data, no production classifier, no clinical validation, and no safeguarding validation."
}
```

## Markdown Summary Excerpt

```markdown
# Meridian Daily Enquiry Summary

- Total enquiries: 12
- Human review count: 8

## Human Review Required

- ENQ-005
  - Interest area: PRP
  - Reason: clinic consultation review; guarantee / outcome boundary
  - Owner note: Route to clinic consultation lead...
```
