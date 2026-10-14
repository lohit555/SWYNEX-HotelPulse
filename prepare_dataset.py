from pathlib import Path

import pandas as pd

DATA_DIR = Path("data")
INPUT_FILE = DATA_DIR / "Hotel_Reviews.csv"
OUTPUT_FILE = DATA_DIR / "hotel_reviews_sample.csv"

SAMPLES_PER_CLASS = 1000


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT_FILE.resolve()}"
        )

    print("Loading hotel reviews dataset...")

    required_columns = [
        "Positive_Review",
        "Negative_Review",
        "Reviewer_Score",
    ]

    df = pd.read_csv(INPUT_FILE, usecols=required_columns)

    samples = []

    for column, sentiment in [
        ("Positive_Review", "Positive"),
        ("Negative_Review", "Negative"),
    ]:
        reviews = df[[column, "Reviewer_Score"]].copy()
        reviews.rename(columns={column: "review_text"}, inplace=True)

        reviews["review_text"] = (
            reviews["review_text"].fillna("").str.strip()
        )

        # Remove blank reviews and dataset placeholder text.
        placeholders = {
            "positive": {"no positive"},
            "negative": {"no negative"},
        }

        reviews = reviews[
            (reviews["review_text"] != "")
            & ~reviews["review_text"].str.lower().isin(
                placeholders[sentiment.lower()]
            )
        ].copy()

        reviews["source_sentiment"] = sentiment

        sample_size = min(SAMPLES_PER_CLASS, len(reviews))

        reviews = reviews.sample(
            n=sample_size,
            random_state=42,
        )

        samples.append(reviews)

        print(f"{sentiment} reviews selected: {sample_size}")

    result = pd.concat(samples, ignore_index=True)
    result = result.sample(frac=1, random_state=42).reset_index(drop=True)

    result.insert(0, "review_id", range(1, len(result) + 1))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print("\nDataset preparation complete!")
    print(f"Total sample reviews: {len(result)}")
    print(f"Saved to: {OUTPUT_FILE.resolve()}")
    print("\nReview counts:")
    print(result["source_sentiment"].value_counts())
    print("\nFirst five rows:")
    print(result.head().to_string(index=False))


if __name__ == "__main__":
    main()
