import json
import re
from pathlib import Path
import csv
import pandas as pd


# ============================================================
# PATHS
# ============================================================

INPUT_JSON = Path(r"C:\Users\tejas\Downloads\no_pii_grievance.json")

MAPPING_FILE = Path(
    r"C:\Users\tejas\OneDrive\learning\civic_voice\AI-Assistant-for-Multi-Channel-Citizen-Feedback-Analysis-1"
    r"\datasets\raw\cpgrams\CategoryCode_Mapping.xlsx"
)

OUTPUT_FILE = Path(
    r"C:\Users\tejas\OneDrive\learning\civic_voice\AI-Assistant-for-Multi-Channel-Citizen-Feedback-Analysis-1"
    r"\datasets\processed\cpgrams_clean.csv"
)


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    """Clean citizen grievance text without changing its meaning."""

    if value is None:
        return ""

    text = str(value)

    # Replace HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace newlines/tabs/multiple spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text

def normalize_category_code(value):
    """Normalize category codes so numeric formats like 11578.0 become 11578."""

    if pd.isna(value):
        return ""

    value = str(value).strip()

    if not value:
        return ""

    # Convert values like 11578.0 -> 11578
    if re.fullmatch(r"\d+\.0+", value):
        return value.split(".")[0]

    return value


# ============================================================
# LOAD CATEGORY MAPPING
# ============================================================

print("Loading category mapping...")

mapping = pd.read_excel(
    MAPPING_FILE,
    sheet_name="Complaint Category"
)

print("Mapping rows:", len(mapping))
print("Mapping columns:", list(mapping.columns))


# Convert codes to strings so they can be matched reliably
mapping["Code"] = mapping["Code"].apply(
    normalize_category_code
)

# Keep only useful mapping columns
mapping = mapping[
    ["Code", "Description", "OrgCode", "Parent", "Stage", "MonitoringCode"]
].copy()

mapping = mapping.rename(
    columns={
        "Code": "category_code",
        "Description": "category",
        "OrgCode": "organization"
    }
)

# Remove duplicate category codes if any
mapping = mapping.drop_duplicates(
    subset=["category_code"]
)


# ============================================================
# LOAD CPGRAMS JSON
# ============================================================

print("\nLoading CPGRAMS grievance data...")
print("This may take some time...")

with open(INPUT_JSON, "r", encoding="utf-8") as file:
    data = json.load(file)

print("Total records loaded:", len(data))


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(data)

print("\nOriginal columns:")
print(list(df.columns))


# ============================================================
# SELECT / RENAME FIELDS
# ============================================================

processed = pd.DataFrame()

processed["feedback_id"] = (
    df["registration_no"]
    .astype(str)
    .str.strip()
)

processed["source"] = "CPGRAMS"

# Prefer received date because it represents when the grievance
# entered the system.
processed["timestamp"] = pd.to_datetime(
    df["recvd_date"].apply(
        lambda x: x.get("$date") if isinstance(x, dict) else x
    ),
    errors="coerce",
    utc=True,
    format="mixed"
)

processed["text"] = df["subject_content_text"].apply(clean_text)

processed["state"] = (
    df["state"]
    .fillna("")
    .astype(str)
    .str.strip()
)

processed["district"] = (
    df["dist_name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

processed["category_code"] = (
    df["CategoryV7"]
    .apply(normalize_category_code)
)

processed["organization"] = (
    df["org_code"]
    .fillna("")
    .astype(str)
    .str.strip()
)

processed["v7_target"] = (
    df["v7_target"]
    .fillna("")
    .astype(str)
    .str.strip()
)

processed["data_type"] = "real"


# ============================================================
# REMOVE RECORDS WITHOUT TEXT
# ============================================================

before = len(processed)

processed = processed[
    processed["text"].str.len() > 0
].copy()

after = len(processed)

print("\nRecords removed because of empty text:", before - after)


# ============================================================
# REMOVE DUPLICATE FEEDBACK IDs
# ============================================================

before = len(processed)

processed = processed.drop_duplicates(
    subset=["feedback_id"]
)

after = len(processed)

print("Duplicate feedback IDs removed:", before - after)


# ============================================================
# MAP CATEGORY INFORMATION
# ============================================================

print("\nMapping CategoryV7 values...")

processed = processed.merge(
    mapping[
        [
            "category_code",
            "category",
            "organization"
        ]
    ],
    on="category_code",
    how="left",
    suffixes=("", "_mapped")
)


# Use mapped organization when available
processed["organization"] = processed[
    "organization_mapped"
].fillna(
    processed["organization"]
)

processed = processed.drop(
    columns=["organization_mapped"]
)

# ============================================================
# CATEGORY MAPPING DIAGNOSTICS
# ============================================================

print("\n========================================")
print("CATEGORY MAPPING DIAGNOSTICS")
print("========================================")

empty_category_codes = (
    processed["category_code"].eq("").sum()
)

unmapped_nonempty = (
    processed["category"].isna()
    & processed["category_code"].ne("")
).sum()

mapped = processed["category"].notna().sum()

print("Total records:", len(processed))
print("Mapped:", mapped)
print("Empty category codes:", empty_category_codes)
print("Non-empty but unmapped:", unmapped_nonempty)

print("\nTop unmapped category codes:")

print(
    processed.loc[
        processed["category"].isna()
        & processed["category_code"].ne(""),
        "category_code"
    ]
    .value_counts()
    .head(30)
)


# ============================================================
# LANGUAGE
# ============================================================

# We are not guessing language yet.
# This will be detected later by the NLP pipeline.

processed["language"] = ""


# ============================================================
# REORDER COLUMNS
# ============================================================

processed = processed[
    [
        "feedback_id",
        "source",
        "timestamp",
        "text",
        "state",
        "district",
        "category_code",
        "category",
        "organization",
        "language",
        "data_type",
        "v7_target"
    ]
]


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

processed.to_csv(
    OUTPUT_FILE,
    index=False,
    
    quoting=csv.QUOTE_MINIMAL,
    escapechar="\\"
)


# ============================================================
# SUMMARY
# ============================================================

print("\n========================================")
print("CPGRAMS PREPROCESSING COMPLETE")
print("========================================")

print("Output:", OUTPUT_FILE)
print("Records:", len(processed))
print("Columns:", len(processed.columns))

print("\nMissing text:",
      (processed["text"].str.len() == 0).sum())

print("Unique feedback IDs:",
      processed["feedback_id"].nunique())

print("Category mapped:",
      processed["category"].notna().sum())

print("Category not mapped:",
      processed["category"].isna().sum())

print("\nTop states:")
print(
    processed["state"]
    .value_counts()
    .head(10)
)

print("\nTop categories:")
print(
    processed["category"]
    .value_counts()
    .head(10)
)

print("\nDone.")

print("\nMapping CategoryV7 values...")

print("\nSample CPGRAMS category codes:")
print(processed["category_code"].head(20).to_list())

print("\nSample mapping category codes:")
print(mapping["category_code"].head(20).to_list())

print("\nCPGRAMS category_code dtype:")
print(processed["category_code"].dtype)

print("\nMapping category_code dtype:")
print(mapping["category_code"].dtype)

processed = processed.merge(
    mapping[
        [
            "category_code",
            "category",
            "organization"
        ]
    ],
    on="category_code",
    how="left",
    suffixes=("", "_mapped")
)