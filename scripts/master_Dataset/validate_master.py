import pandas as pd
import os

# ============================================================
# MASTER DATASET VALIDATION
# ============================================================

MASTER_FILE = r"datasets\masterd\master_feedback.csv"

print("=" * 60)
print("MASTER DATASET VALIDATION")
print("=" * 60)

# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

if not os.path.exists(MASTER_FILE):
    print(f"\nERROR: File not found: {MASTER_FILE}")
    exit()

df = pd.read_csv(MASTER_FILE, low_memory=False)

print("\n1. DATASET OVERVIEW")
print("-" * 60)
print(f"Shape: {df.shape}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# ------------------------------------------------------------
# 2. Check columns
# ------------------------------------------------------------

expected_columns = [
    "feedback_id",
    "source",
    "timestamp",
    "text",
    "organization",
    "loc",
    "urgency"
]

print("\n2. COLUMN VALIDATION")
print("-" * 60)
print("Expected columns:")
print(expected_columns)

print("\nActual columns:")
print(df.columns.tolist())

if df.columns.tolist() == expected_columns:
    print("\n✓ Column schema is correct.")
else:
    print("\n✗ Column schema does not match expected schema.")

# ------------------------------------------------------------
# 3. Missing values
# ------------------------------------------------------------

print("\n3. MISSING VALUES")
print("-" * 60)

missing = df.isnull().sum()

for column, count in missing.items():
    percentage = (count / len(df)) * 100
    print(f"{column}: {count:,} ({percentage:.2f}%)")

# ------------------------------------------------------------
# 4. Empty text values
# ------------------------------------------------------------

print("\n4. TEXT VALIDATION")
print("-" * 60)

empty_text = df["text"].fillna("").astype(str).str.strip().eq("").sum()

print(f"Empty text records: {empty_text:,}")

# Very short text
short_text = df["text"].fillna("").astype(str).str.strip().str.len().lt(5).sum()

print(f"Very short text (<5 characters): {short_text:,}")

# ------------------------------------------------------------
# 5. Duplicate feedback IDs
# ------------------------------------------------------------

print("\n5. DUPLICATE FEEDBACK IDs")
print("-" * 60)

duplicate_id_count = df["feedback_id"].duplicated(keep=False).sum()
duplicate_unique_ids = df.loc[
    df["feedback_id"].duplicated(keep=False),
    "feedback_id"
].nunique()

print(f"Records involved in duplicate IDs: {duplicate_id_count:,}")
print(f"Unique duplicate IDs: {duplicate_unique_ids:,}")

# ------------------------------------------------------------
# 6. Exact duplicate rows
# ------------------------------------------------------------

print("\n6. EXACT DUPLICATE ROWS")
print("-" * 60)

exact_duplicates = df.duplicated().sum()

print(f"Exact duplicate rows: {exact_duplicates:,}")

# ------------------------------------------------------------
# 7. Source distribution
# ------------------------------------------------------------

print("\n7. SOURCE DISTRIBUTION")
print("-" * 60)

source_counts = df["source"].value_counts(dropna=False)

print(source_counts.to_string())

# ------------------------------------------------------------
# 8. Urgency distribution
# ------------------------------------------------------------

print("\n8. URGENCY DISTRIBUTION")
print("-" * 60)

urgency_counts = df["urgency"].value_counts(dropna=False)

print(urgency_counts.to_string())

# ------------------------------------------------------------
# 9. Timestamp validation
# ------------------------------------------------------------

print("\n9. TIMESTAMP VALIDATION")
print("-" * 60)

timestamps = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True,
    format="mixed"
)

invalid_timestamps = timestamps.isna().sum()

print(f"Invalid/missing timestamps: {invalid_timestamps:,}")

if timestamps.notna().any():
    print(f"Earliest timestamp: {timestamps.min()}")
    print(f"Latest timestamp:   {timestamps.max()}")
else:
    print("No valid timestamps found.")

# ------------------------------------------------------------
# 10. Organization distribution
# ------------------------------------------------------------

print("\n10. ORGANIZATION DISTRIBUTION")
print("-" * 60)

print(
    df["organization"]
    .value_counts(dropna=False)
    .head(20)
    .to_string()
)

# ------------------------------------------------------------
# 11. Location coverage
# ------------------------------------------------------------

print("\n11. LOCATION COVERAGE")
print("-" * 60)

missing_location = df["loc"].isna().sum()

print(f"Missing locations: {missing_location:,}")
print(f"Unique locations: {df['loc'].nunique(dropna=True):,}")

# ------------------------------------------------------------
# 12. Feedback ID validation
# ------------------------------------------------------------

print("\n12. FEEDBACK ID VALIDATION")
print("-" * 60)

missing_ids = df["feedback_id"].isna().sum()
empty_ids = (
    df["feedback_id"]
    .fillna("")
    .astype(str)
    .str.strip()
    .eq("")
    .sum()
)

print(f"Missing feedback IDs: {missing_ids:,}")
print(f"Empty feedback IDs: {empty_ids:,}")

# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(f"Total records:              {len(df):,}")
print(f"Total columns:              {len(df.columns)}")
print(f"Empty text records:         {empty_text:,}")
print(f"Very short text records:    {short_text:,}")
print(f"Duplicate ID records:       {duplicate_id_count:,}")
print(f"Unique duplicate IDs:       {duplicate_unique_ids:,}")
print(f"Exact duplicate rows:       {exact_duplicates:,}")
print(f"Invalid timestamps:         {invalid_timestamps:,}")
print(f"Missing feedback IDs:       {missing_ids:,}")
print(f"Empty feedback IDs:         {empty_ids:,}")

print("\n" + "=" * 60)
print("VALIDATION COMPLETED")
print("=" * 60)