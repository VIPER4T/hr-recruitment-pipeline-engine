# 🛠️ Technical Usage & Architecture Guide

## 1. Relational Data Modeling (Hybrid Star Schema)
This application abandons traditional, flat-file spreadsheet architecture in favor of a **Hybrid Star Schema** loaded into Excel's xVelocity memory engine. This structure ensures high-speed query performance and prevents calculation errors caused by duplicated data.

### Table Categorization
The raw dataset is structurally divided into Dimension (Lookup) and Fact (Data) tables:
* **Dimension Tables:** `Dim_Jobs`, `Dim_Candidates`, `Dim_Stages`, `Dim_Recruiters`. These tables contain unique, non-repeating records that dictate the filter context.
* **Fact Tables:** `Fact_Applications`, `Fact_Stage_Movements`. These tables contain the transactional history and raw quantitative metrics.

### Relationship Mapping
* **1-to-Many Cardinality:** Relationships flow unidirectionally from the Dimension tables downward into the Fact tables. 
* **Dependency Management:** Ambiguous paths and inactive relationships were explicitly mapped to prevent circular dependency loops when cross-filtering between recruiter performance and specific candidate applications.

---

## 2. The Analytical Engine: Advanced DAX
Standard PivotTable summarization is insufficient for calculating relational ratios (like stage drop-offs) or retrieving specific targets across disconnected tables. The engine relies on explicit DAX measures to control filter context.

### Context Overrides (`ALL`)
To calculate the true **Stage Funnel Conversion Rate**, the engine must look at the total volume of applications in *Stage 1*, regardless of which stage row it is currently evaluating.
* By wrapping the denominator in the `ALL()` function, the DAX measure forces the engine to ignore the native row filter and retrieve the absolute starting pipeline volume, ensuring accurate percentage drop-offs step-by-step.

### Row-by-Row Iteration (`AVERAGEX` & `RELATED`)
Calculating **SLA Variance** required pulling the target SLA days from the `Dim_Jobs` table and comparing it against the actual time-to-hire in the `Fact_Applications` table.
* Using `AVERAGEX` forces the xVelocity engine to step through the data row by row. 
* Inside that iterator, `RELATED` is used to travel up the established relationship line to grab the specific SLA target for that distinct job, subtract the actual days, and then average the result. This prevents the engine from defaulting to a global maximum SLA.

---

## 3. Interface Engineering & UI Protection
The front-end user interface is highly insulated from the backend data model to prevent accidental breakage by end-users.

### Shadow Anchor Architecture
The macro KPI cards (Total Requisitions, Conversion Rates, Average SLA) do not pull directly from the raw tables. Instead, they are anchored to a hidden `Staging_Pivots` worksheet. This decoupled structure ensures that when a user aggressively slices the data on the front end, the underlying shapes and references do not collapse or throw `#REF!` errors.

### Dynamic Array Lookups
The **Live Requisition Lookup** utilizes a nested array stack to bypass the need for slow, manual filtering.
* **The Formula:** `=IFERROR(SORT(FILTER(CHOOSECOLS(Applications, 1, 2, 6, 8, 9), (Applications[JobID]=Selected_Req)*(Applications[Final_Status]<>"Rejected")), 4, -1), "No Active Pipeline")`
* **The Mechanics:** `CHOOSECOLS` extracts only the necessary dossier columns. `FILTER` enforces the active pipeline Boolean logic. `SORT` ranks the output by Technical Score (Column 4) in descending order. `IFERROR` catches empty pipelines and cleanly returns a custom text string instead of a `#CALC!` error.

---

## 4. Procedural Dataset Generation
To ensure testing integrity without compromising real-world data governance, the foundational data was programmatically synthesized.
* A custom Python script (`pandas`, `numpy`) generated the 1,200-row relational database.
* The script utilized randomized distribution logic to simulate realistic business conditions, intentionally weighting drop-off rates at the Technical Assessment and Panel Interview stages to mirror enterprise hiring friction.
