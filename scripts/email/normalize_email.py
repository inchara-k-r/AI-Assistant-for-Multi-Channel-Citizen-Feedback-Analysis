import pandas as pd
import os
import re

RAW_FILE = r"datasets\raw\email\email_raw_dataset.csv"
OUTPUT_FILE = r"datasets\processed\email_clean.csv"

EXPECTED_COLUMNS = [
    "feedback_id",
    "source",
    "timestamp",
    "text",
    "organization",
    "loc",
    "urgency"
]


def clean_html(text):
    """Remove HTML tags and normalize whitespace."""
    if pd.isna(text):
        return ""

    text = str(text)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


print("=" * 70)
print("EMAIL DATA NORMALIZATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load raw dataset
# ------------------------------------------------------------

print("\nLoading raw Email dataset...")

df = pd.read_csv(RAW_FILE)

print(f"Raw records: {len(df):,}")
print("Raw columns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. Check required columns
# ------------------------------------------------------------

required_columns = [
    "feedback_id",
    "source",
    "timestamp",
    "subject",
    "email_body",
    "service",
    "city",
    "state"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print("\nERROR: Missing required columns:")
    print(missing_columns)
    raise SystemExit(1)


# ------------------------------------------------------------
# 3. Analyze source values before standardization
# ------------------------------------------------------------

print("\nSource values before standardization:")
print(df["source"].value_counts(dropna=False))


# ------------------------------------------------------------
# 4. Remove exact duplicate rows
# ------------------------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = before_duplicates - len(df)

print(f"\nExact duplicate rows removed: {duplicates_removed:,}")


# ------------------------------------------------------------
# 5. Feedback ID validation
# ------------------------------------------------------------

missing_ids = df["feedback_id"].isna().sum()
duplicate_ids = df["feedback_id"].duplicated().sum()

print(f"Missing feedback IDs: {missing_ids:,}")
print(f"Duplicate feedback IDs: {duplicate_ids:,}")

if missing_ids > 0:
    print("WARNING: Some Email records have missing feedback IDs.")

if duplicate_ids > 0:
    print("WARNING: Duplicate Email feedback IDs detected.")


# ------------------------------------------------------------
# 6. Normalize timestamp
# ------------------------------------------------------------

print("\nProcessing timestamps...")

# Treat obvious placeholder values as missing
df["timestamp"] = df["timestamp"].replace(
    [
        "##############",
        "############",
        "########",
        "",
        "nan",
        "NaN"
    ],
    pd.NA
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

timestamp_missing = df["timestamp"].isna().sum()
timestamp_available = df["timestamp"].notna().sum()

print(f"Valid timestamps: {timestamp_available:,}")
print(f"Missing/invalid timestamps: {timestamp_missing:,}")


# ------------------------------------------------------------
# 7. Clean subject and email body
# ------------------------------------------------------------

df["subject"] = df["subject"].apply(clean_html)
df["email_body"] = df["email_body"].apply(clean_html)


# ------------------------------------------------------------
# 8. Create unified text field
# ------------------------------------------------------------

def combine_text(row):
    subject = str(row["subject"]).strip()
    body = str(row["email_body"]).strip()

    if subject and body:
        return subject + " " + body

    if subject:
        return subject

    return body


df["text"] = df.apply(combine_text, axis=1)


# ------------------------------------------------------------
# 9. Create location
# ------------------------------------------------------------

df["city"] = df["city"].apply(clean_html)
df["state"] = df["state"].apply(clean_html)


def combine_location(row):
    city = str(row["city"]).strip()
    state = str(row["state"]).strip()

    if city and state:
        return f"{city}, {state}"

    if city:
        return city

    if state:
        return state

    return pd.NA


df["loc"] = df.apply(combine_location, axis=1)


# ------------------------------------------------------------
# 10. Standardize source
# ------------------------------------------------------------

# This dataset is the Email source.
# Standardize source labels such as "Eail" to "Email".
df["source"] = "Email"


# ------------------------------------------------------------
# 11. Organization and urgency
# ------------------------------------------------------------

# The current Email dataset does not provide a dedicated
# organization or urgency field in the source schema.

df["organization"] = pd.NA
df["urgency"] = pd.NA


# ------------------------------------------------------------
# 12. Select final master schema
# ------------------------------------------------------------

df = df[
    [
        "feedback_id",
        "source",
        "timestamp",
        "text",
        "organization",
        "loc",
        "urgency"
    ]
]


# ------------------------------------------------------------
# 13. Final validation
# ------------------------------------------------------------

empty_text = (df["text"].str.strip() == "").sum()
duplicate_rows_final = df.duplicated().sum()
duplicate_ids_final = df["feedback_id"].duplicated().sum()

print("\n" + "=" * 70)
print("EMAIL NORMALIZATION COMPLETED")
print("=" * 70)

print(f"Final records:             {len(df):,}")
print(f"Exact duplicate rows:      {duplicate_rows_final:,}")
print(f"Duplicate feedback IDs:    {duplicate_ids_final:,}")
print(f"Empty text records:        {empty_text:,}")
print(f"Valid timestamps:          {df['timestamp'].notna().sum():,}")
print(f"Missing timestamps:        {df['timestamp'].isna().sum():,}")
print(f"Available locations:       {df['loc'].notna().sum():,}")
print(f"Missing locations:         {df['loc'].isna().sum():,}")

print("\nFinal columns:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 14. Save
# ------------------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nOutput file:")
print(OUTPUT_FILE)

print("\n" + "=" * 70)
print("EMAIL CLEAN DATASET READY")
print("=" * 70)