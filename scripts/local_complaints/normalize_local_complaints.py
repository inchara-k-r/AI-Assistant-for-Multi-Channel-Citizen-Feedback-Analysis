import pandas as pd
from pathlib import Path


# File paths
INPUT_FILE = Path(
    "datasets/raw/local_complaints/local_complaints_bengaluru.csv"
)

OUTPUT_FILE = Path(
    "datasets/processed/local_complaints_bengaluru_clean.csv"
)


def normalize_dataset():
    # Read raw dataset
    df = pd.read_csv(INPUT_FILE)

    # Create normalized dataset
    clean_df = pd.DataFrame({
        "feedback_id": df["Complaint ID"],
        "source": "BBMP_Bengaluru",
        "timestamp": pd.to_datetime(
            df["Grievance Date"],
            errors="coerce"
        ),
        "text": df["Complaint_Text"],
        "organization": "BBMP",
        "loc": df["Ward Name"],
        "urgency": df["Urgency_Level"],
    })

    # Basic text cleanup
    clean_df["text"] = (
        clean_df["text"]
        .fillna("")
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Clean location
    clean_df["loc"] = (
        clean_df["loc"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Clean urgency
    clean_df["urgency"] = (
        clean_df["urgency"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Create output directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save normalized dataset
    clean_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("Normalization completed successfully!")
    print(f"Input shape:  {df.shape}")
    print(f"Output shape: {clean_df.shape}")
    print(f"\nOutput file: {OUTPUT_FILE}")

    print("\nColumns:")
    print(clean_df.columns.tolist())

    print("\nFirst 5 rows:")
    print(clean_df.head().to_string(index=False))


if __name__ == "__main__":
    normalize_dataset()