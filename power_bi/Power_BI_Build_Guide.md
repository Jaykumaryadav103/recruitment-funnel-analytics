# Power BI Build Guide

## 1. Load and clean

Use Get Data → Text/CSV and import `data/raw/candidate_pipeline_raw.csv`. In Power Query, set Candidate ID and category fields to Text, date milestones to Date, and Days to Current Stage to Whole Number. Apply the cleaning steps in `power_bi/Power_Query_Cleaning.m`; the cleaned output should contain one row per Candidate ID.

## 2. Model

For a compact portfolio model, use one fact table named `Candidates`. Add a calendar table for Application Date and relate it one-to-many to Candidates. Keep Application Date as the active relationship. Use the cleaned table, not the intentionally imperfect raw export, for visuals. Sort Current Stage using a numeric stage-order column from 1 to 7.

## 3. Measures

Copy measures from `power_bi/Recruitment_Measures.dax`. Check the counts against `analysis/funnel_summary.csv` before presenting.

## 4. Page layout

### Page 1: Hiring overview

- KPI cards: Applications, Joiners, Application-to-join rate, Median days to join
- Funnel: stage reached, sorted by Stage Order
- Bar chart: applications and joiners by role
- Slicers: application month, role, experience level, source

### Page 2: Source performance

- Matrix: source, applications, joiners, hire rate, median days to join
- Bar chart: application-to-join rate by source with applicant count in tooltip
- Keep Unknown visible as a data-quality category. Do not rank sources without considering sample size and role mix.

### Page 3: Process and quality

- Stage-to-stage conversion table
- Candidate counts by current stage and outcome
- Data quality indicators: duplicate IDs removed, missing source rows, invalid dates removed
- A short note stating the synthetic data notice and snapshot date

## 5. Visual and accessibility choices

Use a restrained navy and teal palette, descriptive titles, consistent date filters and readable labels. Avoid red/green as the only signal. Give every visual alt text and test the report at normal laptop width. Hide Candidate ID from leadership pages and do not publish row-level candidate details.

## 6. Refresh and QA

1. Refresh the query and confirm unique Candidate ID count equals row count.
2. Confirm applications equal 360 and joined equals 48 for the supplied sample.
3. Confirm stage counts match the funnel CSV: 360, 318, 218, 138, 88, 60, 48.
4. Spot-check a few joined records' application and start dates.
5. Verify slicers filter every relevant visual and stage order remains correct.
6. Add a visible refresh date and synthetic-data disclosure before sharing.
