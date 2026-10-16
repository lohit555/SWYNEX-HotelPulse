import json
import time
from pathlib import Path

import pandas as pd

from analyzer import analyze_complaint


BASE_DIR = Path(__file__).resolve().parent
EXAMPLES_FILE = BASE_DIR / "evaluation_examples.json"
RESULTS_FILE = BASE_DIR / "evaluation_results.csv"


def load_examples():
    """Load manually labelled evaluation examples."""
    if not EXAMPLES_FILE.exists():
        raise FileNotFoundError(
            f"Evaluation file not found: {EXAMPLES_FILE}"
        )

    with EXAMPLES_FILE.open("r", encoding="utf-8") as file:
        examples = json.load(file)

    if not isinstance(examples, list) or not examples:
        raise ValueError(
            "The evaluation file must contain a non-empty JSON list."
        )

    required_fields = {
        "id",
        "text",
        "expected_category",
        "expected_is_complaint",
        "expected_severity",
    }

    for example in examples:
        missing = required_fields - example.keys()

        if missing:
            raise ValueError(
                f"Example {example.get('id', '?')} is missing: "
                f"{', '.join(sorted(missing))}"
            )

    return examples


def calculate_accuracy(results, expected_field, predicted_field):
    """Calculate accuracy for examples with valid predictions."""
    valid = [
        row
        for row in results
        if row.get(predicted_field) is not None
    ]

    if not valid:
        return None

    correct = sum(
        row[expected_field] == row[predicted_field]
        for row in valid
    )

    return correct / len(valid) * 100


def main():
    examples = load_examples()

    print("=" * 65)
    print("HOTELPULSE MODEL EVALUATION")
    print("=" * 65)
    print(f"Examples to evaluate: {len(examples)}")
    print("Model calls may take time and use API quota.")
    print()

    results = []
    api_failures = 0

    for index, example in enumerate(examples, start=1):
        print(
            f"[{index}/{len(examples)}] "
            f"Evaluating example {example['id']}..."
        )

        row = {
            "id": example["id"],
            "text": example["text"],
            "expected_category": example["expected_category"],
            "expected_is_complaint": example[
                "expected_is_complaint"
            ],
            "expected_severity": example["expected_severity"],
            "predicted_category": None,
            "predicted_is_complaint": None,
            "predicted_severity": None,
            "category_correct": None,
            "complaint_detection_correct": None,
            "severity_correct": None,
            "error": None,
        }

        try:
            prediction = analyze_complaint(example["text"])

            row["predicted_category"] = prediction["category"]
            row["predicted_is_complaint"] = prediction[
                "is_complaint"
            ]
            row["predicted_severity"] = prediction["severity"]

            row["category_correct"] = (
                row["expected_category"]
                == row["predicted_category"]
            )

            row["complaint_detection_correct"] = (
                row["expected_is_complaint"]
                == row["predicted_is_complaint"]
            )

            row["severity_correct"] = (
                row["expected_severity"]
                == row["predicted_severity"]
            )

            if not (
                row["category_correct"]
                and row["complaint_detection_correct"]
                and row["severity_correct"]
            ):
                print(
                    "  MISMATCH | "
                    f"Expected: {row['expected_category']}, "
                    f"Predicted: {row['predicted_category']}"
                )
            else:
                print("  PASS")

        except Exception as error:
            api_failures += 1
            row["error"] = f"{type(error).__name__}: {error}"
            print(f"  ERROR: {row['error']}")

        results.append(row)

        # Avoid sending requests too quickly.
        if index < len(examples):
            time.sleep(1)

    dataframe = pd.DataFrame(results)
    dataframe.to_csv(RESULTS_FILE, index=False, encoding="utf-8")

    valid_results = [
        row for row in results
        if row["error"] is None
    ]

    print()
    print("=" * 65)
    print("EVALUATION SUMMARY")
    print("=" * 65)

    print(f"Total examples: {len(examples)}")
    print(f"Successful predictions: {len(valid_results)}")
    print(f"Failed predictions: {api_failures}")

    if not valid_results:
        print(
            "\nNo successful predictions were available. "
            "Check the API key, model availability, connection, "
            "and quota before trying again."
        )
        print(f"Detailed output: {RESULTS_FILE}")
        return

    metrics = [
        (
            "Category accuracy",
            "expected_category",
            "predicted_category",
        ),
        (
            "Complaint detection accuracy",
            "expected_is_complaint",
            "predicted_is_complaint",
        ),
        (
            "Severity accuracy",
            "expected_severity",
            "predicted_severity",
        ),
    ]

    for label, expected_field, predicted_field in metrics:
        accuracy = calculate_accuracy(
            valid_results,
            expected_field,
            predicted_field,
        )

        print(f"{label}: {accuracy:.2f}%")

    category_mismatches = [
        row for row in valid_results
        if not row["category_correct"]
    ]

    complaint_mismatches = [
        row for row in valid_results
        if not row["complaint_detection_correct"]
    ]

    severity_mismatches = [
        row for row in valid_results
        if not row["severity_correct"]
    ]

    print()
    print("Incorrect category predictions:")
    if category_mismatches:
        for row in category_mismatches:
            print(
                f"  ID {row['id']}: "
                f"expected {row['expected_category']}, "
                f"predicted {row['predicted_category']}"
            )
    else:
        print("  None")

    print()
    print("Incorrect complaint-detection predictions:")
    if complaint_mismatches:
        for row in complaint_mismatches:
            print(
                f"  ID {row['id']}: "
                f"expected {row['expected_is_complaint']}, "
                f"predicted {row['predicted_is_complaint']}"
            )
    else:
        print("  None")

    print()
    print("Incorrect severity predictions:")
    if severity_mismatches:
        for row in severity_mismatches:
            print(
                f"  ID {row['id']}: "
                f"expected {row['expected_severity']}, "
                f"predicted {row['predicted_severity']}"
            )
    else:
        print("  None")

    print()
    print(f"Detailed results saved to: {RESULTS_FILE}")
    print(
        "Review incorrect predictions before drawing conclusions "
        "or changing the model."
    )


if __name__ == "__main__":
    main()