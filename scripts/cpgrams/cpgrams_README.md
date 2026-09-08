### `normalize_cpgrams.py`

Preprocesses the raw CPGRAMS grievance dataset and converts it into the standardized CiviVoice format.

#### Processing Steps

- Loads the CPGRAMS category mapping from `CategoryCode_Mapping.xlsx`
- Loads the raw CPGRAMS grievance data from JSON
- Cleans grievance text by removing HTML tags and unnecessary whitespace
- Removes records with empty grievance text
- Removes duplicate feedback IDs
- Normalizes dates, states, districts, category codes, and organization fields
- Maps `CategoryV7` values to their corresponding category descriptions
- Adds standardized fields such as `feedback_id`, `source`, `timestamp`, `language`, and `data_type`
- Saves the processed dataset as `cpgrams_clean.csv`

#### Execution

```bash
python scripts/normalize_cpgrams.py


### Output

CPGRAMS PREPROCESSING COMPLETE
========================================
Output: datasets/processed/cpgrams_clean.csv
Records: 175,782
Columns: 12

Missing text: 0
Unique feedback IDs: 175,782
Category mapped: 63,622
Category not mapped: 112,160


# Data Summary
Total records loaded: 175,784
Records removed because of empty text: 2
Duplicate feedback IDs removed: 0

Top states:
UP    39,333
BH    16,295
MH    15,206
DH    12,380
GJ     9,891
WB     9,305
MP     8,386
RJ     7,735
TN     6,735
HY     6,612


# Category Mapping Diagnostics

Total records: 175,782
Mapped: 63,622
Empty category codes: 112,160
Non-empty but unmapped: 0



# Top Mapped Categories


Others                                                      6,847
stoppage of installments after issue of few installments    4,417
Others (EPFO)                                               2,864
Refund matter, Wrong Demand                                 2,672
Central Government related                                  1,536
Others/Misc.                                                1,470
Miscellaneous/Others                                        1,426
Miscellaneous                                               1,278
Other                                                       1,115
Other/Misc/Suggestions                                        805