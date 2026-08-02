# 🧬 Procedural Dataset Generation (Python)

## Why This Script Exists
To build a highly realistic HR Analytics Engine without violating actual corporate data governance or exposing Personally Identifiable Information (PII), I needed a robust, relational dataset to stress-test my architecture. 

Instead of manually typing dummy data or downloading a generic Kaggle CSV, I wrote `dataset_generator.py` to procedurally synthesize a complete corporate hiring environment from scratch.

## What the Script Does
This script utilizes `pandas` and `numpy` to generate 1,200 candidates and their corresponding fact tables, ensuring strict relational integrity across a 7-stage hiring pipeline. 

It does not just generate random numbers; it engineers **realistic business logic**:
* **Drop-off Logic:** The script is weighted to force higher rejection rates at the "Technical Assessment" and "Panel Interview" stages to simulate actual industry bottlenecks.
* **SLA Timelines:** Date generation is bound by specific minimum and maximum day intervals to ensure `Time_to_Hire_Days` calculations accurately reflect realistic corporate hiring speeds.
* **Relational Integrity:** Candidate IDs, Job IDs, and Recruiter IDs are strictly mapped to ensure no orphaned records exist when the data is loaded into the xVelocity Power Pivot engine.

## How to Run It
If you wish to generate a fresh dataset with different randomized parameters:
1. Ensure Python 3.x and `pandas` are installed.
2. Run the script via terminal: `python dataset_generator.py`
3. The script will output the updated relational tables as a multi-sheet Excel file (`HR_Recruitment_Data_Architecture.xlsx`) ready for Power Pivot ingestion.
