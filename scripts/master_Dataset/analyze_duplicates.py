import pandas as pd
import os

# ============================================================
# DUPLICATE ANALYSIS FOR MASTER DATASET
# ============================================================

MASTER_FILE = r"datasets\masterd\master_feedback.csv"

print("=" * 70)
print("MASTER DATASET - DUPLICATE ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Load dataset
# ------------------------------------------------------------

df = pd.read_csv(
    MASTER_FILE,
    low_memory=False,
    dtype={"feedback_id": str}
)

print(f"\nTotal records: {len(df):,}")

# ------------------------------------------------------------
# 2. Exact duplicate rows by source
# ------------------------------------------------------------

print("\n1. EXACT DUPLICATE ROWS BY SOURCE")
print("-" * 70)

exact_dup_mask = df.duplicated(keep=False)

exact_dups = df[exact_dup_mask]

print(f"Total records involved in exact duplicates: {len(exact_dups):,}")

if len(exact_dups) > 0:
    print("\nExact duplicate records by source:")
    print(
        exact_dups["source"]
        .value_counts()
        .to_string()
    )

# ------------------------------------------------------------
# 3. Duplicate feedback IDs by source
# ------------------------------------------------------------

print("\n2. DUPLICATE FEEDBACK IDs BY SOURCE")
print("-" * 70)

duplicate_id_mask = df["feedback_id"].duplicated(keep=False)

duplicate_ids = df[duplicate_id_mask]

print(f"Records involved in duplicate IDs: {len(duplicate_ids):,}")
print(
    f"Unique duplicate feedback IDs: "
    f"{duplicate_ids['feedback_id'].nunique():,}"
)

print("\nDuplicate ID records by source:")
print(
    duplicate_ids["source"]
    .value_counts()
    .to_string()
)

# ------------------------------------------------------------
# 4. Duplicate IDs within each source
# ------------------------------------------------------------

print("\n3. DUPLICATE IDs WITHIN EACH SOURCE")
print("-" * 70)

for source in df["source"].dropna().unique():

    source_df = df[df["source"] == source]

    duplicate_count = source_df["feedback_id"].duplicated(
        keep=False
    ).sum()

    unique_duplicate_ids = source_df.loc[
        source_df["feedback_id"].duplicated(keep=False),
        "feedback_id"
    ].nunique()

    print(
        f"{source:<20} "
        f"records: {duplicate_count:>8,} | "
        f"unique IDs: {unique_duplicate_ids:>6,}"
    )

# ------------------------------------------------------------
# 5. Cross-source duplicate IDs
# ------------------------------------------------------------

print("\n4. CROSS-SOURCE DUPLICATE IDs")
print("-" * 70)

id_source_counts = (
    df.groupby("feedback_id")["source"]
    .nunique()
)

cross_source_ids = id_source_counts[
    id_source_counts > 1
]

print(
    f"Feedback IDs appearing in multiple sources: "
    f"{len(cross_source_ids):,}"
)

if len(cross_source_ids) > 0:

    print("\nExamples of cross-source duplicate IDs:")

    example_ids = cross_source_ids.head(10).index

    print(
        df[df["feedback_id"].isin(example_ids)][
            ["feedback_id", "source", "text"]
        ].to_string(index=False)
    )

# ------------------------------------------------------------
# 6. Examples of exact duplicates
# ------------------------------------------------------------

print("\n5. EXAMPLES OF EXACT DUPLICATE ROWS")
print("-" * 70)

if len(exact_dups) > 0:

    duplicate_groups = (
        exact_dups
        .groupby(list(df.columns))
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    print(
        duplicate_groups.head(10).to_string(index=False)
    )

# ------------------------------------------------------------
# 7. Timestamp availability by source
# ------------------------------------------------------------

print("\n6. TIMESTAMP AVAILABILITY BY SOURCE")
print("-" * 70)

timestamp = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

timestamp_summary = pd.DataFrame({
    "Total": df.groupby("source").size(),
    "Missing": timestamp.isna().groupby(df["source"]).sum()
})

timestamp_summary["Available"] = (
    timestamp_summary["Total"] -
    timestamp_summary["Missing"]
)

timestamp_summary["Missing %"] = (
    timestamp_summary["Missing"] /
    timestamp_summary["Total"] * 100
).round(2)

print(timestamp_summary.to_string())

# ------------------------------------------------------------
# 8. Location availability by source
# ------------------------------------------------------------

print("\n7. LOCATION AVAILABILITY BY SOURCE")
print("-" * 70)

location_missing = (
    df["loc"]
    .isna()
    .groupby(df["source"])
    .sum()
)

location_total = df.groupby("source").size()

location_summary = pd.DataFrame({
    "Total": location_total,
    "Missing": location_missing
})

location_summary["Available"] = (
    location_summary["Total"] -
    location_summary["Missing"]
)

location_summary["Missing %"] = (
    location_summary["Missing"] /
    location_summary["Total"] * 100
).round(2)

print(location_summary.to_string())

# ------------------------------------------------------------
# 9. Urgency availability by source
# ------------------------------------------------------------

print("\n8. URGENCY AVAILABILITY BY SOURCE")
print("-" * 70)

urgency_missing = (
    df["urgency"]
    .isna()
    .groupby(df["source"])
    .sum()
)

urgency_total = df.groupby("source").size()

urgency_summary = pd.DataFrame({
    "Total": urgency_total,
    "Missing": urgency_missing
})

urgency_summary["Available"] = (
    urgency_summary["Total"] -
    urgency_summary["Missing"]
)

urgency_summary["Missing %"] = (
    urgency_summary["Missing"] /
    urgency_summary["Total"] * 100
).round(2)

print(urgency_summary.to_string())

# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DUPLICATE ANALYSIS COMPLETED")
print("=" * 70)

print("\nNo changes were made to master_feedback.csv.")