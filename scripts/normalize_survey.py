import re
from pathlib import Path
import pandas as pd

INPUT_FILE = Path(r"datasets\raw\survey\survey_synthetic_raw.csv")
OUTPUT_FILE = Path(r"datasets\processed\survey_clean.csv")

def clean_text(value):
    if pd.isna(value):
        return ""
    text = str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

SERVICE_TO_CATEGORY = {
    "Roads & Traffic": "Roads & Traffic",
    "Public Transport": "Public Transport",
    "Water Supply": "Water Supply",
    "Electricity": "Electricity",
    "Healthcare": "Healthcare",
    "Sanitation & Waste": "Sanitation & Waste",
    "Education": "Education",
    "Police & Public Safety": "Police & Public Safety",
    "Government Documents": "Government Documents",
    "Other Public Services": "Other Public Services",
}

print("Loading synthetic survey data...")
df = pd.read_csv(INPUT_FILE)
print("Records loaded:", len(df))

processed = pd.DataFrame()
processed["feedback_id"] = [f"SURVEY_{i:06d}" for i in range(1, len(df) + 1)]
processed["source"] = "Survey"
processed["timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
processed["text"] = df["Tell us about your experience"].apply(clean_text)
processed["state"] = df["State"].fillna("").astype(str).str.strip()
processed["district"] = df["City/District"].fillna("").astype(str).str.strip()
processed["service"] = df["Public service"].fillna("").astype(str).str.strip()
processed["category"] = processed["service"].map(SERVICE_TO_CATEGORY)
processed["language"] = df["Language"].fillna("").astype(str).str.strip()
processed["experience"] = df["Experience"].fillna("").astype(str).str.strip()
processed["urgency"] = df["Urgency"].fillna("").astype(str).str.strip()
processed["issue_date"] = pd.to_datetime(df["Issue date"], errors="coerce")
processed["action_requested"] = (
    df["Would you like the concerned authority to take action?"]
    .fillna("").astype(str).str.strip()
)

# These are simulated/demo responses, not real citizen responses.
processed["data_type"] = "synthetic"

before = len(processed)
processed = processed[processed["text"].str.len() > 0].copy()
print("Records removed because of empty text:", before - len(processed))

before = len(processed)
processed = processed.drop_duplicates(subset=["feedback_id"])
print("Duplicate feedback IDs removed:", before - len(processed))

processed = processed[
    [
        "feedback_id", "source", "timestamp", "text", "state", "district",
        "service", "category", "language", "experience", "urgency",
        "issue_date", "action_requested", "data_type"
    ]
]

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
processed.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\n========================================")
print("SURVEY PREPROCESSING COMPLETE")
print("========================================")
print("Output:", OUTPUT_FILE)
print("Records:", len(processed))
print("Columns:", len(processed.columns))
print("Missing text:", (processed["text"].str.len() == 0).sum())
print("Unique feedback IDs:", processed["feedback_id"].nunique())
print("Category mapped:", processed["category"].notna().sum())

print("\nTop states:")
print(processed["state"].value_counts().head(10))

print("\nTop services:")
print(processed["service"].value_counts().head(10))

print("\nTop categories:")
print(processed["category"].value_counts().head(10))

print("\nData type:")
print(processed["data_type"].value_counts())

print("\nDone.")
