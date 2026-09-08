### `normalize_survey.py`

Preprocesses the synthetic citizen survey dataset and converts it into the standardized CiviVoice feedback format.

The survey dataset is designed to simulate citizen feedback collected through a Google Form. Since collecting a large number of geographically diverse real-world responses is not practical for development and testing, synthetic responses are used for the initial NLP pipeline.

> **Important:** The survey records are synthetic and must not be represented as real citizen responses.

#### Processing Steps

- Loads the raw synthetic survey responses from CSV
- Generates unique feedback IDs
- Cleans citizen feedback text
- Normalizes timestamps and issue dates
- Standardizes state and district/city fields
- Maps public services to standardized categories
- Preserves survey attributes such as:
  - Experience
  - Urgency
  - Language
  - Action requested
- Adds the `source` field as `Survey`
- Adds `data_type` as `synthetic`
- Removes records with empty feedback text
- Removes duplicate feedback IDs
- Saves the processed dataset as `survey_clean.csv`

#### Execution

```bash
python scripts/normalize_survey.py

# Output
========================================
SURVEY PREPROCESSING COMPLETE
========================================
Output: datasets\processed\survey_clean.csv
Records: 10,000
Columns: 14

Missing text: 0
Unique feedback IDs: 10,000
Category mapped: 10,000
Data Summary
Total records loaded: 10,000
Records removed because of empty text: 0
Duplicate feedback IDs removed: 0


# Top States

Uttar Pradesh                  329
Bihar                          309
Ladakh                         306
Mizoram                        295
Puducherry                     295
Andaman and Nicobar Islands    294
Gujarat                        292
West Bengal                    289
Nagaland                       288
Punjab                         288


# Top Public Services

Sanitation & Waste        1,077
Public Transport          1,043
Education                 1,028
Police & Public Safety    1,027
Roads & Traffic           1,022
Government Documents        980
Water Supply                978
Healthcare                  965
Electricity                 950
Other Public Services       930


# Top Categories

Sanitation & Waste        1,077
Public Transport          1,043
Education                 1,028
Police & Public Safety    1,027
Roads & Traffic           1,022
Government Documents        980
Water Supply                978
Healthcare                  965
Electricity                 950
Other Public Services       930
Data Type
synthetic    10,000
