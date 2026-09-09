import pandas as pd
import os

RAW_FILE = r"datasets\raw\local_complaints\local_complaints_bengaluru.csv"

print("=" * 70)
print("RAW BENGALURU DATASET - DUPLICATE ANALYSIS")
print("=" * 70)

df = pd.read_csv(
    RAW_FILE,
    low_memory=False
)

print(f"\nTotal records: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# ------------------------------------------------------------
# 1. Exact duplicate rows
# ------------------------------------------------------------

print("\n1. EXACT DUPLICATE ROWS")
print("-" * 70)

exact_duplicates = df.duplicated().sum()

print(f"Exact duplicate rows: {exact_duplicates:,}")

# ------------------------------------------------------------
# 2. Duplicate Complaint IDs
# ------------------------------------------------------------

print("\n2. DUPLICATE COMPLAINT IDs")
print("-" * 70)

duplicate_id_mask = df["Complaint ID"].duplicated(keep=False)

duplicate_ids = df[duplicate_id_mask]

print(f"Records involved in duplicate IDs: {len(duplicate_ids):,}")

print(
    f"Unique duplicate Complaint IDs: "
    f"{duplicate_ids['Complaint ID'].nunique():,}"
)

# ------------------------------------------------------------
# 3. Most repeated Complaint IDs
# ------------------------------------------------------------

print("\n3. MOST REPEATED COMPLAINT IDs")
print("-" * 70)

id_counts = (
    df["Complaint ID"]
    .value_counts()
)

repeated_ids = id_counts[id_counts > 1]

print(f"Complaint IDs appearing more than once: {len(repeated_ids):,}")

print("\nTop 10 repeated Complaint IDs:")

print(
    repeated_ids.head(10).to_string()
)

# ------------------------------------------------------------
# 4. Duplicate IDs with different records
# ------------------------------------------------------------

print("\n4. DUPLICATE IDs WITH DIFFERENT RECORD CONTENT")
print("-" * 70)

duplicate_id_groups = (
    df[df["Complaint ID"].isin(repeated_ids.index)]
    .groupby("Complaint ID")
)

different_record_ids = []

for complaint_id, group in duplicate_id_groups:
    if len(group.drop_duplicates()) > 1:
        different_record_ids.append(complaint_id)

print(
    f"Duplicate IDs with different record content: "
    f"{len(different_record_ids):,}"
)

# ------------------------------------------------------------
# 5. Sample duplicate records
# ------------------------------------------------------------

print("\n5. SAMPLE DUPLICATE RECORDS")
print("-" * 70)

if len(repeated_ids) > 0:

    sample_ids = repeated_ids.head(5).index

    sample = df[
        df["Complaint ID"].isin(sample_ids)
    ]

    print(
        sample[
            [
                "Complaint ID",
                "Grievance Date",
                "Ward Name",
                "Complaint_Text",
                "Urgency_Level"
            ]
        ].to_string(index=False)
    )

# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("RAW DUPLICATE ANALYSIS COMPLETED")
print("=" * 70)

print("\nNo changes were made to the raw dataset.")