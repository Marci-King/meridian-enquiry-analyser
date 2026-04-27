"""Analyse fictional Meridian-style enquiries into structured review notes.

This is a small learning project. It uses only the Python standard library and
works with fictional demo data. It is not a production classifier, clinical
tool, safeguarding tool, or live AI system.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re


TRUTH_BOUNDARY = (
    "Static local analysis using fictional demo data only. No live model call, "
    "no real customer data, no production classifier, no clinical validation, "
    "and no safeguarding validation."
)


@dataclass
class AnalysedEnquiry:
    """A structured version of one messy enquiry."""

    id: str
    source: str
    original_text: str
    category: str
    interest_area: str
    missing_details: list[str]
    human_review_required: bool
    review_reason: str
    human_owner: str
    suggested_next_step: str
    owner_note: str
    truth_boundary: str


class MeridianAnalyser:
    """Turn raw enquiries into structured review outputs."""

    def __init__(self, enquiries: list[dict[str, str]]) -> None:
        self.enquiries = enquiries

    def classify(self, text: str) -> str:
        """Return the broad service category for an enquiry."""
        clean_text = text.lower()

        hospitality_words = [
            "coffee",
            "pastries",
            "table",
            "catering",
            "lunch",
            "cakes",
            "collect",
            "gluten free",
        ]
        clinic_words = [
            "prp",
            "smp",
            "hair",
            "hair unit",
            "hair system",
            "akn",
            "keloid",
            "shedding",
            "diagnosis",
        ]
        send_sports_words = [
            "send",
            "football",
            "child",
            "autism",
            "support needs",
            "safeguarding",
            "parent",
        ]

        if self.contains_any(clean_text, send_sports_words):
            return "send_sports"
        if self.contains_any(clean_text, clinic_words):
            return "clinic_consultation"
        if self.contains_any(clean_text, hospitality_words):
            return "hospitality"
        return "general"

    def detect_interest(self, text: str) -> str:
        """Return the most useful interest area label for routing."""
        clean_text = text.lower()

        interest_patterns = [
            ("pricing / quote", r"\b(cost|price|pricing|how much|quote)\b"),
            ("age group question", r"\b(age|aged|year-old|years old)\b"),
            ("SEND-friendly session", r"\b(send|support needs|autism|anxious)\b"),
            ("event coffee", r"\b(coffee|pastries|event)\b"),
            ("table booking", r"\b(book a table|table|booking)\b"),
            ("catering", r"\b(catering|corporate lunch|lunch)\b"),
            ("PRP", r"\bprp\b"),
            ("SMP", r"\bsmp\b"),
            ("custom hair unit", r"\b(hair unit|hair system)\b"),
            ("AKN", r"\b(akn|keloid|bumps)\b"),
            ("general hair loss", r"\b(shedding|hair loss|thinning hair)\b"),
        ]

        for label, pattern in interest_patterns:
            if re.search(pattern, clean_text):
                return label

        return "general enquiry"

    def find_missing_details(self, category: str, text: str) -> list[str]:
        """Check which useful follow-up details are absent."""
        clean_text = text.lower()
        missing_details: list[str] = []

        if category == "hospitality":
            checks = {
                "date": r"\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|next week|next friday|\d{1,2}/\d{1,2})\b",
                "time": r"\b(\d{1,2}(am|pm)|morning|afternoon|evening|lunchtime)\b",
                "headcount": r"\b(\d+\s*(people|guests|covers)|for\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten))\b",
                "location": r"\b(near|at|in|delivery|collect|collection)\b",
                "contact details": r"\b(email|phone|call|contact|@)\b",
                "collection/delivery preference": r"\b(collect|collection|deliver|delivery)\b",
                "dietary requirements": r"\b(gluten free|vegan|vegetarian|allergy|allergies|dietary)\b",
            }
        elif category == "clinic_consultation":
            checks = {
                "concern area": r"\b(hair|scalp|head|patchy|thinning|shedding|akn|keloid|bumps)\b",
                "timeline": r"\b(month|months|week|weeks|year|years|since|recently)\b",
                "preferred contact": r"\b(email|phone|call|contact|dm)\b",
                "optional photos": r"\b(photo|photos|picture|pictures|image|images)\b",
                "consultation availability": r"\b(available|availability|come in|appointment|book|consultation)\b",
            }
        elif category == "send_sports":
            checks = {
                "child age": r"\b(age|aged|year-old|years old|\b\d{1,2}\b)\b",
                "support needs": r"\b(send|support needs|autism|anxious|one-to-one|needs)\b",
                "preferred session": r"\b(session|sessions|football|join)\b",
                "parent/guardian contact": r"\b(parent|guardian|email|phone|contact|speak)\b",
                "programme lead review": r"\b(safeguarding|support needs|one-to-one|incident|safely)\b",
            }
        else:
            checks = {
                "service area": r"\b(clinic|cafe|football|hair|catering|booking)\b",
                "preferred contact": r"\b(email|phone|call|contact|dm)\b",
            }

        for detail, pattern in checks.items():
            if not re.search(pattern, clean_text):
                missing_details.append(detail)

        return missing_details

    def audit_human_review(self, category: str, interest_area: str, text: str) -> tuple[bool, str]:
        """Decide whether a person should review the enquiry before replying."""
        clean_text = text.lower()

        review_patterns = {
            "diagnosis boundary": r"\bdiagnos(e|is|ing)\b",
            "suitability boundary": r"\b(suitable|suitability)\b",
            "guarantee / outcome boundary": r"\b(guarantee|guaranteed|will it work|outcome|results?)\b",
            "pricing / quote requested": r"\b(cost|price|pricing|how much|quote)\b",
            "SEND/support needs": r"\b(send|support needs|autism|one-to-one|anxious)\b",
            "safeguarding-sensitive wording": r"\b(safeguarding|incident|safely|worries)\b",
        }

        reasons: list[str] = []
        for reason, pattern in review_patterns.items():
            if re.search(pattern, clean_text):
                reasons.append(reason)

        if category == "clinic_consultation" and interest_area in {"PRP", "SMP", "AKN", "general hair loss"}:
            reasons.append("clinic consultation review")

        if category == "send_sports":
            reasons.append("programme lead review")

        if reasons:
            return True, "; ".join(sorted(set(reasons)))

        return False, "standard enquiry"

    def build_owner_note(
        self,
        category: str,
        interest_area: str,
        missing_details: list[str],
        human_review_required: bool,
        review_reason: str,
    ) -> tuple[str, str, str]:
        """Create the owner, suggested next step, and short review note."""
        if category == "hospitality":
            human_owner = "hospitality owner"
            suggested_next_step = "confirm event or booking details before replying"
        elif category == "clinic_consultation":
            human_owner = "clinic consultation lead"
            suggested_next_step = "route to consultation review before giving advice"
        elif category == "send_sports":
            human_owner = "SEND sports programme lead"
            suggested_next_step = "route to programme lead for support and safeguarding review"
        else:
            human_owner = "Meridian owner"
            suggested_next_step = "clarify the service area and preferred contact route"

        if missing_details:
            missing_text = ", ".join(missing_details)
        else:
            missing_text = "no obvious missing details"

        if human_review_required:
            owner_note = (
                f"Route to {human_owner}. Interest area: {interest_area}. "
                f"Reason: {review_reason}. Missing details: {missing_text}."
            )
        else:
            owner_note = (
                f"Prepare a standard reply. Interest area: {interest_area}. "
                f"Missing details: {missing_text}."
            )

        return human_owner, suggested_next_step, owner_note

    def process(self) -> list[AnalysedEnquiry]:
        """Analyse every enquiry and return structured objects."""
        analysed_enquiries: list[AnalysedEnquiry] = []

        for enquiry in self.enquiries:
            text = enquiry["text"]
            category = self.classify(text)
            interest_area = self.detect_interest(text)
            missing_details = self.find_missing_details(category, text)
            human_review_required, review_reason = self.audit_human_review(
                category,
                interest_area,
                text,
            )
            human_owner, suggested_next_step, owner_note = self.build_owner_note(
                category,
                interest_area,
                missing_details,
                human_review_required,
                review_reason,
            )

            analysed_enquiries.append(
                AnalysedEnquiry(
                    id=enquiry["id"],
                    source=enquiry["source"],
                    original_text=text,
                    category=category,
                    interest_area=interest_area,
                    missing_details=missing_details,
                    human_review_required=human_review_required,
                    review_reason=review_reason,
                    human_owner=human_owner,
                    suggested_next_step=suggested_next_step,
                    owner_note=owner_note,
                    truth_boundary=TRUTH_BOUNDARY,
                )
            )

        return analysed_enquiries

    @staticmethod
    def contains_any(text: str, words: list[str]) -> bool:
        """Return True if any simple keyword appears in the text."""
        for word in words:
            if word in text:
                return True
        return False


def load_enquiries(input_path: Path) -> list[dict[str, str]]:
    """Load fictional enquiry records from a JSON file."""
    with input_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json_output(analysed_enquiries: list[AnalysedEnquiry], output_path: Path) -> None:
    """Write analysed enquiry objects to a readable JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_data = []

    for enquiry in analysed_enquiries:
        output_data.append(asdict(enquiry))

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(output_data, file, indent=2)
        file.write("\n")


def write_markdown_summary(analysed_enquiries: list[AnalysedEnquiry], output_path: Path) -> None:
    """Write a readable daily summary report in Markdown."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    category_counts = Counter()
    interest_counts = Counter()
    human_review_count = 0
    follow_up_count = 0

    for enquiry in analysed_enquiries:
        category_counts[enquiry.category] += 1
        interest_counts[enquiry.interest_area] += 1

        if enquiry.human_review_required:
            human_review_count += 1

        if enquiry.missing_details:
            follow_up_count += 1

    lines = [
        "# Meridian Daily Enquiry Summary",
        "",
        f"- Total enquiries: {len(analysed_enquiries)}",
        f"- Category breakdown: {format_counter(category_counts)}",
        f"- Interest area breakdown: {format_counter(interest_counts)}",
        f"- Human review count: {human_review_count}",
        f"- Follow-up/missing details count: {follow_up_count}",
        "",
        "## Human Review Required",
        "",
    ]

    for enquiry in analysed_enquiries:
        if enquiry.human_review_required:
            lines.extend(
                [
                    f"- {enquiry.id}",
                    f"  - Interest area: {enquiry.interest_area}",
                    f"  - Reason: {enquiry.review_reason}",
                    f"  - Owner note: {enquiry.owner_note}",
                ]
            )

    lines.extend(["", "## Follow-Up Needed", ""])

    for enquiry in analysed_enquiries:
        if enquiry.missing_details:
            missing_text = ", ".join(enquiry.missing_details)
            lines.append(f"- {enquiry.id}: {missing_text}")

    lines.extend(["", "## Category Breakdown", ""])

    for category, count in category_counts.most_common():
        lines.append(f"- {category}: {count}")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            (
                "Static local analysis using fictional demo data only. No live model call, "
                "no real customer data, no production classifier."
            ),
            "",
            (
                "This proof artifact is not clinical validation, not safeguarding validation, "
                "not production-ready, and not integrated into the Meridian runtime yet."
            ),
            "",
        ]
    )

    with output_path.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def format_counter(counter: Counter) -> str:
    """Turn a Counter into a short readable summary."""
    parts = []

    for name, count in counter.most_common():
        parts.append(f"{name} ({count})")

    return ", ".join(parts)


def main() -> None:
    """Run the full local analysis workflow."""
    project_root = Path(__file__).parent
    input_path = project_root / "data" / "enquiries.json"
    json_output_path = project_root / "outputs" / "analysed_enquiries.json"
    markdown_output_path = project_root / "outputs" / "daily_summary.md"

    enquiries = load_enquiries(input_path)
    analyser = MeridianAnalyser(enquiries)
    analysed_enquiries = analyser.process()

    write_json_output(analysed_enquiries, json_output_path)
    write_markdown_summary(analysed_enquiries, markdown_output_path)

    print(f"Analysed {len(analysed_enquiries)} fictional enquiries.")
    print(f"Wrote JSON output to {json_output_path}")
    print(f"Wrote Markdown summary to {markdown_output_path}")
    print("Truth boundary: fictional data, local deterministic analysis, no live AI model.")


if __name__ == "__main__":
    main()
