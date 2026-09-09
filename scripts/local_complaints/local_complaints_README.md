Yes. Copy **everything inside this block** directly into `scripts/local_complaints/README.md`:

````markdown
# Local Complaints Dataset Processing

This folder contains the preprocessing and normalization script for the Bengaluru local complaints dataset used in the CiviVoice project.

## Dataset

The dataset contains local civic complaints from Bengaluru, including complaint details, complaint text, location information, grievance dates, and urgency levels.

### Raw Dataset

```text
datasets/raw/local_complaints/local_complaints_bengaluru.csv
````

### Raw Dataset Columns

The original dataset contains the following columns:

* `Complaint ID`
* `Category`
* `Sub Category`
* `Grievance Date`
* `Ward Name`
* `Grievance Status`
* `Staff Remarks`
* `Staff Name`
* `Complaint_Text`
* `Urgency_Level`

## Normalization

The raw dataset is processed using:

```text
scripts/local_complaints/normalize_local_complaints.py
```

The script converts the raw Bengaluru complaints dataset into the common CiviVoice feedback schema used for combining multiple citizen-feedback sources.

### Column Mapping

| Raw Column       | Standardized Column |
| ---------------- | ------------------- |
| `Complaint ID`   | `feedback_id`       |
| `Grievance Date` | `timestamp`         |
| `Complaint_Text` | `text`              |
| `Ward Name`      | `loc`               |
| `Urgency_Level`  | `urgency`           |

The following values are assigned during normalization:

| Standardized Column | Value            |
| ------------------- | ---------------- |
| `source`            | `BBMP_Bengaluru` |
| `organization`      | `BBMP`           |

### Excluded Columns

The following raw columns are not included in the standardized dataset:

* `Category`
* `Sub Category`
* `Grievance Status`
* `Staff Remarks`
* `Staff Name`

These fields are excluded because they are not required in the common 7-column CiviVoice master schema.

## Standardized Schema

The processed dataset contains exactly 7 columns:

```text
feedback_id
source
timestamp
text
organization
loc
urgency
```

| Column         | Description                                    |
| -------------- | ---------------------------------------------- |
| `feedback_id`  | Unique complaint identifier                    |
| `source`       | Source of the feedback                         |
| `timestamp`    | Date and time of the complaint                 |
| `text`         | Complaint or feedback text                     |
| `organization` | Organization associated with the complaint     |
| `loc`          | Location or ward associated with the complaint |
| `urgency`      | Urgency level of the complaint                 |

## Processing Steps

1. Loads the raw Bengaluru complaints CSV file.
2. Maps `Complaint ID` to `feedback_id`.
3. Maps `Grievance Date` to `timestamp`.
4. Maps `Complaint_Text` to `text`.
5. Assigns `BBMP_Bengaluru` as the `source`.
6. Assigns `BBMP` as the `organization`.
7. Maps `Ward Name` to `loc`.
8. Maps `Urgency_Level` to `urgency`.
9. Removes columns that are not required in the common schema.
10. Saves the normalized dataset in the processed datasets directory.

## Execution

Run the following command from the project root:

```bash
python scripts/local_complaints/normalize_local_complaints.py
```

## Output

The normalized dataset is saved as:

```text
datasets/processed/local_complaints_bengaluru_clean.csv
```

### Output Summary

* **Records:** 20,000
* **Columns:** 7

## Role in CiviVoice

The normalized Bengaluru complaints dataset is later combined with the other processed citizen-feedback datasets using:

```text
scripts/master_Dataset/merge_feedback.py
```

The dataset contributes **20,000 records** to the final CiviVoice master dataset.

```


```
