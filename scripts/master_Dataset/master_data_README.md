### `merge_feedback.py`

Combines the cleaned datasets from multiple citizen-feedback channels into a single standardized master dataset for downstream NLP analysis.

### Input Datasets

The script combines the following processed datasets:

- `twitter_clean.csv`
- `cpgrams_clean.csv`
- `email_clean.csv`
- `survey_clean.csv`
- `local_complaints_bengaluru_clean.csv`

All datasets are mapped to a common CiviVoice feedback schema before merging.

### Standardized Master Schema

The final master dataset contains the following 7 columns:

| Column | Description |
|---|---|
| `feedback_id` | Unique feedback or complaint identifier |
| `source` | Feedback channel, such as Twitter, CPGRAMS, Survey, Email, or BBMP |
| `timestamp` | Date and time associated with the feedback |
| `text` | Citizen complaint or feedback text |
| `organization` | Organization or service associated with the feedback |
| `loc` | Location associated with the feedback |
| `urgency` | Urgency level when available |

### Processing Steps

1. Loads all cleaned datasets from `datasets/processed/`
2. Maps dataset-specific columns to the common CiviVoice schema
3. Standardizes text, location, organization, and urgency fields
4. Converts timestamps to a consistent datetime format
5. Removes records with empty feedback text
6. Checks for duplicate feedback IDs
7. Combines all datasets into a single master DataFrame
8. Preserves the original cleaned datasets
9. Saves the final master dataset as `master_feedback.csv`

### Execution


Run the following command from the project root:

bash
python scripts/master_Dataset/merge_feedback.py


### Output

The merged master dataset is saved at:

datasets/masterd/master_feedback.csv

