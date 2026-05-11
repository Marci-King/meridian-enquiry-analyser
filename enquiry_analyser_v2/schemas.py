"""Structured output contracts for Meridian Enquiry Analyser V2.

These TypedDict definitions document the JSON shape written by v2_analyser.py.
They are intentionally lightweight and use only the Python standard library.
"""

from __future__ import annotations

from typing import Literal, TypedDict


RetrievalConfidence = Literal["low", "medium", "high"]


class RetrievedGuidance(TypedDict):
    """One local guidance snippet returned by keyword-overlap retrieval."""

    source_filename: str
    chunk_id: str
    score: int
    matched_keywords: list[str]
    snippet: str


class RetrievalReview(TypedDict):
    """Deterministic review of whether retrieved guidance is sufficient."""

    guidance_found: bool
    retrieval_confidence: RetrievalConfidence
    review_note: str


class AnalysisMetadata(TypedDict):
    """Audit metadata attached to every analysed enquiry."""

    analyser_version: Literal["Meridian-Enquiry-Analyser-V2"]
    retrieval_mode: Literal["local_keyword_overlap"]
    live_model_used: bool
    fictional_data: bool
    safety_boundary_hit: bool


class AnalysedEnquiry(TypedDict):
    """Structured JSON output contract for one analysed enquiry."""

    enquiry_id: str
    metadata: AnalysisMetadata
    business: str
    message: str
    service_category: str
    risk_flags: list[str]
    missing_details: list[str]
    retrieved_guidance: list[RetrievedGuidance]
    retrieval_review: RetrievalReview
    human_review_required: bool
    recommended_next_step: str
