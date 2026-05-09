"""Run deterministic V2 proof evals using the Python standard library only."""

from __future__ import annotations

from pathlib import Path
import json
import sys


EVAL_DIR = Path(__file__).resolve().parent
BASE_DIR = EVAL_DIR.parent
REPORT_PATH = EVAL_DIR / "eval_report.md"
sys.path.insert(0, str(BASE_DIR))

from v2_analyser import KeywordGuidanceRetriever, analyse_enquiry  # noqa: E402


def percent(passed: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{(passed / total) * 100:.1f}%"


def run_cases() -> tuple[list[dict[str, object]], dict[str, object]]:
    cases = json.loads((EVAL_DIR / "eval_cases.json").read_text(encoding="utf-8"))
    retriever = KeywordGuidanceRetriever()
    rows: list[dict[str, object]] = []

    category_pass = 0
    human_review_pass = 0
    retrieval_review_pass = 0

    for case in cases:
        actual = analyse_enquiry(case["enquiry"], retriever=retriever)
        actual_review = actual["retrieval_review"]

        category_ok = actual["service_category"] == case["expected_service_category"]
        human_review_ok = actual["human_review_required"] == case["expected_human_review_required"]
        retrieval_ok = (
            actual_review["guidance_found"] == case["expected_guidance_found"]
            and actual_review["retrieval_confidence"] == case["expected_retrieval_confidence"]
        )

        category_pass += int(category_ok)
        human_review_pass += int(human_review_ok)
        retrieval_review_pass += int(retrieval_ok)

        rows.append(
            {
                "case_id": case["case_id"],
                "expected_category": case["expected_service_category"],
                "actual_category": actual["service_category"],
                "expected_human_review": case["expected_human_review_required"],
                "actual_human_review": actual["human_review_required"],
                "expected_retrieval": f"{case['expected_guidance_found']} / {case['expected_retrieval_confidence']}",
                "actual_retrieval": f"{actual_review['guidance_found']} / {actual_review['retrieval_confidence']}",
                "passed": category_ok and human_review_ok and retrieval_ok,
            }
        )

    metrics = {
        "total_cases": len(cases),
        "category_pass": category_pass,
        "human_review_pass": human_review_pass,
        "retrieval_review_pass": retrieval_review_pass,
        "all_passed": all(row["passed"] for row in rows),
    }
    return rows, metrics


def write_report(rows: list[dict[str, object]], metrics: dict[str, object]) -> None:
    total = int(metrics["total_cases"])
    lines = [
        "# Meridian Enquiry Analyser V2 Eval Report",
        "",
        "Deterministic proof evals using fictional cases only.",
        "",
        "## Results",
        "",
        f"- Total cases: {total}",
        f"- Category accuracy: {metrics['category_pass']}/{total} ({percent(int(metrics['category_pass']), total)})",
        f"- Human-review trigger accuracy: {metrics['human_review_pass']}/{total} ({percent(int(metrics['human_review_pass']), total)})",
        f"- Retrieval-review accuracy: {metrics['retrieval_review_pass']}/{total} ({percent(int(metrics['retrieval_review_pass']), total)})",
        "",
        "## Expected vs Actual",
        "",
        "| Case | Expected category | Actual category | Expected human review | Actual human review | Expected retrieval | Actual retrieval | Pass |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for row in rows:
        lines.append(
            "| {case_id} | {expected_category} | {actual_category} | {expected_human_review} | "
            "{actual_human_review} | {expected_retrieval} | {actual_retrieval} | {passed} |".format(**row)
        )

    lines.extend(
        [
            "",
            "## Known Limitations",
            "",
            "- Keyword overlap can miss paraphrases and can over-rank chunks that share surface words.",
            "- The confidence labels are deterministic proof labels, not calibrated probabilities.",
            "- The eval cases are small and fictional; they demonstrate intended boundaries rather than broad coverage.",
            "- Human-review routing is deliberately conservative for clinic and treatment contexts.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows, metrics = run_cases()
    write_report(rows, metrics)
    total = int(metrics["total_cases"])
    print(f"Ran {total} eval cases.")
    print(f"Category accuracy: {metrics['category_pass']}/{total} ({percent(int(metrics['category_pass']), total)})")
    print(
        "Human-review trigger accuracy: "
        f"{metrics['human_review_pass']}/{total} ({percent(int(metrics['human_review_pass']), total)})"
    )
    print(
        "Retrieval-review accuracy: "
        f"{metrics['retrieval_review_pass']}/{total} ({percent(int(metrics['retrieval_review_pass']), total)})"
    )
    print(f"Wrote {REPORT_PATH}")
    if not metrics["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
