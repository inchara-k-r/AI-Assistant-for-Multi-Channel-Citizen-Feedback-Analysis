import pandas as pd
from pathlib import Path


# ============================================================
# Paths
# ============================================================

PROCESSED_DIR = Path("datasets/processed")
MASTER_DIR = Path("datasets/masterd")

OUTPUT_FILE = MASTER_DIR / "master_feedback.csv"
# ============================================================
# Required master schema
# ============================================================

MASTER_COLUMNS = [
    "feedback_id",
    "source",
    "timestamp",
    "text",
    "organization",
    "loc",
    "urgency",
]


# ============================================================
# Helper functions
# ============================================================

def clean_text(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def clean_column(series):
    return (
        series
        .fillna("")
        .astype(str)
        .str.strip()
    )


def normalize_twitter():
    file = PROCESSED_DIR / "twitter_clean.csv"
    df = pd.read_csv(file, dtype=str)

    clean = pd.DataFrame({
        "feedback_id": df["feedback_id"],
        "source": df["source"],
        "timestamp": df["timestamp"],
        "text": df["text"],
        "organization": df["organization"],
        "loc": df["state"],
        "urgency": "",
    })

    return clean


def normalize_cpgrams():
    file = PROCESSED_DIR / "cpgrams_clean.csv"
    df = pd.read_csv(file, dtype=str)

    clean = pd.DataFrame({
        "feedback_id": df["feedback_id"],
        "source": df["source"],
        "timestamp": df["timestamp"],
        "text": df["text"],
        "organization": df["organization"],
        "loc": df["district"],
        "urgency": "",
    })

    return clean


def normalize_email():
    file = PROCESSED_DIR / "email_clean.csv"
    df = pd.read_csv(file, dtype=str)

    clean = df[MASTER_COLUMNS].copy()

    return clean

    


def normalize_survey():
    file = PROCESSED_DIR / "survey_clean.csv"
    df = pd.read_csv(file, dtype=str)

    clean = pd.DataFrame({
        "feedback_id": df["feedback_id"],
        "source": df["source"],
        "timestamp": df["timestamp"],
        "text": df["text"],
        "organization": df["service"],
        "loc": df["district"],
        "urgency": df["urgency"],
    })

    return clean


def normalize_bengaluru():
    file = PROCESSED_DIR / "local_complaints_bengaluru_clean.csv"
    df = pd.read_csv(file, dtype=str)

    clean = df[MASTER_COLUMNS].copy()

    return clean


# ============================================================
# Main merge
# ============================================================

def main():

    print("=" * 60)
    print("CITIZEN FEEDBACK MASTER DATASET CREATION")
    print("=" * 60)

    print("\nLoading and normalizing datasets...")

    twitter = normalize_twitter()
    print(f"Twitter:       {len(twitter):,} rows")

    cpgrams = normalize_cpgrams()
    print(f"CPGRAMS:       {len(cpgrams):,} rows")

    email = normalize_email()
    print(f"Email:         {len(email):,} rows")

    survey = normalize_survey()
    print(f"Survey:        {len(survey):,} rows")

    bengaluru = normalize_bengaluru()
    print(f"Bengaluru:     {len(bengaluru):,} rows")


    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    master = pd.concat(
        [
            twitter,
            cpgrams,
            email,
            survey,
            bengaluru,
        ],
        ignore_index=True
    )


    # --------------------------------------------------------
    # Basic cleaning
    # --------------------------------------------------------

    master["feedback_id"] = clean_column(master["feedback_id"])
    master["source"] = clean_column(master["source"])
    master["text"] = clean_text(master["text"])
    master["organization"] = clean_column(master["organization"])
    master["loc"] = clean_column(master["loc"])
    master["urgency"] = clean_column(master["urgency"])


    # Convert timestamps
    master["timestamp"] = pd.to_datetime(
    master["timestamp"],
    errors="coerce",
    utc=True,
    format="mixed"
)


    # --------------------------------------------------------
    # Remove completely empty feedback text
    # --------------------------------------------------------

    before_empty = len(master)

    master = master[
        master["text"].str.strip() != ""
    ].copy()

    removed_empty = before_empty - len(master)


    # --------------------------------------------------------
    # Check duplicate feedback IDs
    # --------------------------------------------------------

    duplicate_count = master["feedback_id"].duplicated().sum()


    # --------------------------------------------------------
    # Ensure exact column order
    # --------------------------------------------------------

    master = master[MASTER_COLUMNS]


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    MASTER_DIR.mkdir(parents=True, exist_ok=True)

    master.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )


    # ========================================================
    # Report
    # ========================================================

    print("\n" + "=" * 60)
    print("MERGE COMPLETED")
    print("=" * 60)

    print(f"\nMaster dataset: {OUTPUT_FILE}")
    print(f"Final shape:    {master.shape}")

    print(f"\nEmpty-text rows removed: {removed_empty:,}")
    print(f"Duplicate feedback IDs: {duplicate_count:,}")

    print("\nColumns:")
    print(master.columns.tolist())

    print("\nRecords by source:")
    print(master["source"].value_counts().to_string())

    print("\nUrgency distribution:")
    print(
        master["urgency"]
        .replace("", "Not Available")
        .value_counts()
        .to_string()
    )

    print("\nFirst 5 rows:")
    print(master.head().to_string(index=False))

    print("\n" + "=" * 60)
    print("MASTER DATASET READY")
    print("=" * 60)


if __name__ == "__main__":
    main()