# Meridian Enquiry Analyser

## Overview

This small Python project takes fictional service enquiries and turns them into structured review notes, missing-detail checks, and human-review flags.

It is designed to be easy to read and change while learning Python.

## V2 Proof Artifact

A newer proof layer is available in `enquiry_analyser_v2/`.

Meridian Enquiry Analyser V2 demonstrates:

- local markdown-guided retrieval
- retrieval-quality review
- structured JSON outputs
- deterministic evals
- lightweight adversarial cases
- audit metadata
- standard-library schema contracts
- standard-library unit tests
- safety/failure documentation
- human-review routing

Start here:

```text
enquiry_analyser_v2/README_V2_PROOF.md
```

Quick proof:

```bash
python3 enquiry_analyser_v2/v2_analyser.py
python3 enquiry_analyser_v2/evals/run_evals.py
python3 -m unittest discover -s enquiry_analyser_v2/tests
```

## Why This Exists

This proof artefact supports the Meridian story by showing a simple Python-based workflow analysis layer.

It demonstrates how deterministic safety and boundary logic can help turn messy messages into reviewable information before a person replies.

The script can:

- classify enquiries
- detect interest areas
- spot missing details
- flag sensitive or high-boundary wording
- prepare owner, clinic, or programme review notes
- create a daily Markdown summary

## How It Connects To Meridian

This does not power the Meridian demo yet. It is a companion proof artefact showing the kind of data-analysis layer Meridian could use behind a workflow handoff.

It should not be described as a production backend, a live classifier, or something that currently powers Meridian.

## How To Run

From the project folder, run:

```bash
python3 meridian_analyser.py
```

The script reads:

```text
data/enquiries.json
```

It writes:

```text
outputs/analysed_enquiries.json
outputs/daily_summary.md
```

## Example Input

```json
{
  "id": "ENQ-005",
  "source": "Instagram DM",
  "text": "I saw your PRP post for thinning hair. Can you guarantee it will work?"
}
```

## Example Output

```json
{
  "id": "ENQ-005",
  "category": "clinic_consultation",
  "interest_area": "PRP",
  "human_review_required": true,
  "review_reason": "clinic consultation review; guarantee / outcome boundary",
  "human_owner": "clinic consultation lead"
}
```

The Markdown summary also lists human-review items and follow-up details.

## Truth Boundaries

- fictional demo data only
- no real customer data
- no live AI model
- no production classifier
- no clinical validation
- no safeguarding validation
- simple deterministic keyword/regex analysis
- not production-ready
- not integrated into Meridian runtime yet
- companion proof artefact only

## What I Am Learning

This project is useful for learning:

- Python files and folders
- JSON input/output
- dataclasses
- functions
- classes
- dictionaries and lists
- regex keyword matching
- Markdown report generation
- simple deterministic workflow logic

## Next Steps

- add unit tests
- add CSV export
- add Pandas summary later
- compare deterministic flags with LLM review later
- integrate into a future Meridian backend only after validation
