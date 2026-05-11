"""Meridian Enquiry Analyser V2 proof artifact.

V2 preserves the V1 proof and adds a separate retrieval-grounded workflow layer.
It uses fictional data, local Markdown guidance, deterministic rules, and the
Python standard library only.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re
from typing import Any

from retrieve_guidance import KeywordGuidanceRetriever


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "fictional_enquiries.json"
OUTPUT_JSON_PATH = BASE_DIR / "outputs" / "analysed_enquiries_v2.json"
OUTPUT_SUMMARY_PATH = BASE_DIR / "outputs" / "daily_summary_v2.md"

CONFIDENCE_VALUES = {"low", "medium", "high"}


def contains_any(text: str, patterns: list[str]) -> bool:
    """Return true when any regex pattern matches."""
    return any(re.search(pattern, text) for pattern in patterns)


def classify_service_category(business: str, message: str) -> str:
    """Return a deterministic service category for V2 routing."""
    clean_business = business.lower()
    clean_message = message.lower()

    if "jfades" in clean_business or contains_any(
        clean_message,
        [
            r"\bprp\b",
            r"\bsmp\b",
            r"\bakn\b",
            r"\bhair unit\b",
            r"\bhair system\b",
            r"\bkeloid\b",
            r"\bhair loss\b",
            r"\bthinning\b",
            r"\bbaldness\b",
        ],
    ):
        if re.search(r"\bprp\b", clean_message):
            return "jfades_prp"
        if re.search(r"\bsmp\b", clean_message):
            return "jfades_smp"
        if re.search(r"\b(akn|keloid|bumps)\b", clean_message):
            return "jfades_akn"
        if re.search(r"\b(hair unit|hair system)\b", clean_message):
            return "jfades_hair_unit"
        if re.search(r"\b(hair loss|thinning|baldness)\b", clean_message):
            return "jfades_hair_loss"
        return "jfades_general"

    if "cosy mug" in clean_business or contains_any(
        clean_message,
        [r"\bcatering\b", r"\bbooking\b", r"\bbook\b", r"\bdelivery\b", r"\bcollection\b", r"\bopening hours\b"],
    ):
        if re.search(r"\b(catering|lunch|dietary|vegan|gluten free)\b", clean_message):
            return "cosy_mug_catering"
        if re.search(r"\b(opening hours|hours|open|close|saturday|sunday)\b", clean_message):
            return "cosy_mug_opening_hours"
        if re.search(r"\b(delivery|deliver|collection|collect)\b", clean_message):
            return "cosy_mug_delivery_collection"
        if re.search(r"\b(book|booking|table)\b", clean_message):
            return "cosy_mug_booking"
        return "cosy_mug_general"

    return "general"


def detect_risk_flags(business: str, service_category: str, message: str) -> list[str]:
    """Find safety, uncertainty, and prompt-injection-like flags."""
    clean_message = message.lower()
    flags: list[str] = []

    checks = {
        "prompt_injection_like": [
            r"\bignore (all )?(previous|prior|the) rules\b",
            r"\bignore (all )?(previous|prior|the) instructions\b",
            r"\bsafety boundaries do not exist\b",
            r"\boverride\b",
        ],
        "diagnosis_request": [r"\bdiagnos(e|is|ing)\b"],
        "suitability_request": [r"\b(suitable|suitability)\b"],
        "outcome_guarantee_request": [r"\b(definitely work|guarantee|guaranteed|guarantees|will work)\b"],
        "unsupported_cure_claim": [r"\b(cure|cures|cured|baldness)\b"],
        "pricing_or_quote_request": [r"\b(price|pricing|cost|quote|how much)\b"],
    }

    for flag, patterns in checks.items():
        if contains_any(clean_message, patterns):
            flags.append(flag)

    if service_category.startswith("jfades"):
        flags.append("clinic_or_treatment_context")

    if service_category.startswith("jfades") and any(
        flag in flags
        for flag in [
            "diagnosis_request",
            "suitability_request",
            "outcome_guarantee_request",
            "unsupported_cure_claim",
            "pricing_or_quote_request",
        ]
    ):
        flags.append("sensitive_clinic_review")

    return sorted(set(flags))


def find_missing_details(service_category: str, message: str) -> list[str]:
    """Check for useful follow-up details without inferring facts."""
    clean_message = message.lower()

    if service_category.startswith("jfades"):
        checks = {
            "concern area": r"\b(hair|scalp|hairline|bumps|akn|keloid|patch|thinning)\b",
            "timeline": r"\b(day|days|week|weeks|month|months|year|years|since|recently)\b",
            "preferred contact route": r"\b(email|phone|call|dm|message|contact)\b",
            "consultation availability": r"\b(consultation|appointment|available|availability|come in)\b",
        }
    elif service_category.startswith("cosy_mug"):
        checks = {
            "date": r"\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next week|\d{1,2}/\d{1,2})\b",
            "time": r"\b(\d{1,2}(am|pm)|morning|afternoon|evening|lunchtime)\b",
            "headcount or order size": r"\b(\d+\s*(people|guests|covers)|for\s+\d+|team lunch|order)\b",
            "delivery or collection preference": r"\b(delivery|deliver|collection|collect|pickup|pick up)\b",
            "dietary requirements": r"\b(vegan|vegetarian|gluten free|allergy|allergies|dietary)\b",
            "contact details": r"\b(email|phone|call|contact|@)\b",
        }
    else:
        checks = {
            "business context": r"\b(jfades|cosy mug|clinic|cafe|catering|hair|prp|smp)\b",
            "preferred contact route": r"\b(email|phone|call|dm|message|contact)\b",
        }

    return [label for label, pattern in checks.items() if not re.search(pattern, clean_message)]


def review_retrieval(
    service_category: str,
    retrieved_guidance: list[dict[str, Any]],
) -> dict[str, object]:
    """Assess whether local retrieved guidance is sufficient for the workflow."""
    if not retrieved_guidance:
        return {
            "guidance_found": False,
            "retrieval_confidence": "low",
            "review_note": "No local guidance chunk matched the enquiry, so the workflow should fail closed to human review.",
        }

    top_score = int(retrieved_guidance[0]["score"])
    source_names = {str(item["source_filename"]) for item in retrieved_guidance}
    category_prefix = service_category.split("_", 1)[0]

    has_business_source = False
    if category_prefix == "jfades":
        has_business_source = any(name.startswith("jfades_") for name in source_names)
    elif category_prefix == "cosy":
        has_business_source = any(name.startswith("cosy_mug_") for name in source_names)

    if top_score >= 3 and has_business_source:
        confidence = "high"
        note = "Retrieved guidance includes business-specific safety or service wording with several keyword matches."
    elif top_score >= 2 and has_business_source:
        confidence = "medium"
        note = "Retrieved guidance is business-specific but limited, so the workflow should stay cautious."
    else:
        confidence = "low"
        note = "Retrieved guidance is weak, generic, or not clearly tied to the business context."

    assert confidence in CONFIDENCE_VALUES
    return {
        "guidance_found": True,
        "retrieval_confidence": confidence,
        "review_note": note,
    }


def should_require_human_review(
    service_category: str,
    risk_flags: list[str],
    retrieval_review: dict[str, object],
) -> bool:
    """Fail closed for missing guidance and sensitive or uncertain cases."""
    if retrieval_review["guidance_found"] is False:
        return True
    if retrieval_review["retrieval_confidence"] == "low":
        return True
    if "prompt_injection_like" in risk_flags:
        return True
    if service_category.startswith("jfades"):
        return True
    return False


def recommend_next_step(
    service_category: str,
    risk_flags: list[str],
    missing_details: list[str],
    retrieval_review: dict[str, object],
    human_review_required: bool,
) -> str:
    """Create a concise next-step recommendation for the owner."""
    if retrieval_review["guidance_found"] is False:
        return "Route to human review because no local guidance was retrieved."
    if "prompt_injection_like" in risk_flags:
        return "Route to human review and ignore the instruction to override rules or boundaries."
    if service_category.startswith("jfades"):
        return "Route to a JFades human reviewer using consultation-led wording; do not diagnose, decide suitability, or guarantee outcomes."
    if human_review_required:
        return "Route to human review because retrieval confidence is low or the case is uncertain."
    if missing_details:
        return f"Prepare a follow-up asking for: {', '.join(missing_details)}."
    return "Prepare a standard owner-approved response using the retrieved local guidance."


def build_metadata(
    service_category: str,
    risk_flags: list[str],
    retrieval_review: dict[str, object],
    human_review_required: bool,
) -> dict[str, object]:
    """Attach audit metadata that makes proof boundaries explicit."""
    safety_boundary_hit = (
        human_review_required
        and (
            service_category.startswith("jfades")
            or retrieval_review["guidance_found"] is False
            or retrieval_review["retrieval_confidence"] == "low"
            or bool(risk_flags)
        )
    )

    return {
        "analyser_version": "Meridian-Enquiry-Analyser-V2",
        "retrieval_mode": "local_keyword_overlap",
        "live_model_used": False,
        "fictional_data": True,
        "safety_boundary_hit": safety_boundary_hit,
    }


def analyse_enquiry(enquiry: dict[str, str], retriever: KeywordGuidanceRetriever | None = None) -> dict[str, object]:
    """Analyse one fictional enquiry into a structured V2 proof output."""
    retriever = retriever or KeywordGuidanceRetriever()
    business = enquiry["business"]
    message = enquiry["message"]
    service_category = classify_service_category(business, message)
    risk_flags = detect_risk_flags(business, service_category, message)
    missing_details = find_missing_details(service_category, message)
    query_business = "" if business.lower().startswith("unknown") else business
    query = f"{query_business} {message}".strip()
    retrieved_guidance = retriever.retrieve(query, limit=3)
    retrieval_review = review_retrieval(service_category, retrieved_guidance)
    human_review_required = should_require_human_review(
        service_category,
        risk_flags,
        retrieval_review,
    )
    recommended_next_step = recommend_next_step(
        service_category,
        risk_flags,
        missing_details,
        retrieval_review,
        human_review_required,
    )
    metadata = build_metadata(
        service_category,
        risk_flags,
        retrieval_review,
        human_review_required,
    )

    return {
        "enquiry_id": enquiry["enquiry_id"],
        "metadata": metadata,
        "business": business,
        "message": message,
        "service_category": service_category,
        "risk_flags": risk_flags,
        "missing_details": missing_details,
        "retrieved_guidance": retrieved_guidance,
        "retrieval_review": retrieval_review,
        "human_review_required": human_review_required,
        "recommended_next_step": recommended_next_step,
    }


def analyse_enquiries(enquiries: list[dict[str, str]]) -> list[dict[str, object]]:
    """Analyse a list of fictional enquiries."""
    retriever = KeywordGuidanceRetriever()
    return [analyse_enquiry(enquiry, retriever=retriever) for enquiry in enquiries]


def write_json_output(analysed: list[dict[str, object]], path: Path = OUTPUT_JSON_PATH) -> None:
    """Write structured V2 JSON output."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysed, indent=2), encoding="utf-8")


def write_markdown_summary(analysed: list[dict[str, object]], path: Path = OUTPUT_SUMMARY_PATH) -> None:
    """Write a readable Markdown summary for review."""
    path.parent.mkdir(parents=True, exist_ok=True)
    categories = Counter(str(item["service_category"]) for item in analysed)
    human_review_count = sum(1 for item in analysed if item["human_review_required"])

    lines = [
        "# Meridian Enquiry Analyser V2 Daily Summary",
        "",
        "Fictional proof output only. This summary is generated from local test data and deterministic rules.",
        "",
        "## Counts",
        "",
        f"- Total enquiries: {len(analysed)}",
        f"- Human review required: {human_review_count}",
        "",
        "## Categories",
        "",
    ]

    for category, count in sorted(categories.items()):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Human Review Queue", ""])
    for item in analysed:
        if not item["human_review_required"]:
            continue
        review = item["retrieval_review"]
        flags = ", ".join(item["risk_flags"]) if item["risk_flags"] else "none"
        lines.extend(
            [
                f"### {item['enquiry_id']} - {item['business']}",
                "",
                f"- Category: {item['service_category']}",
                f"- Retrieval confidence: {review['retrieval_confidence']}",
                f"- Risk flags: {flags}",
                f"- Next step: {item['recommended_next_step']}",
                "",
            ]
        )

    lines.extend(["## Standard Follow-Up Candidates", ""])
    for item in analysed:
        if item["human_review_required"]:
            continue
        missing = ", ".join(item["missing_details"]) if item["missing_details"] else "none"
        lines.extend(
            [
                f"### {item['enquiry_id']} - {item['business']}",
                "",
                f"- Category: {item['service_category']}",
                f"- Missing details: {missing}",
                f"- Next step: {item['recommended_next_step']}",
                "",
            ]
        )

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    enquiries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    analysed = analyse_enquiries(enquiries)
    write_json_output(analysed)
    write_markdown_summary(analysed)
    print(f"Analysed {len(analysed)} fictional enquiries.")
    print(f"Wrote {OUTPUT_JSON_PATH}")
    print(f"Wrote {OUTPUT_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
