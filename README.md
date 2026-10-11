# Recruitment Funnel Analytics

A complete, portfolio-ready HR analytics case study for a fictional quantum computing and AI company. The project follows candidate applications from first contact through joining and gives a hiring leader a practical view of funnel loss, hiring speed and source mix.

**Data notice:** Every record, person label, company context and result in this package is synthetic and created for demonstration. It must not be presented as evidence about a real employer. No direct personal information is included.

## Start here

1. Read `documentation/Executive_Readout.pdf` for the decision summary.
2. Open `workbook/Recruitment_Funnel_Analysis.xlsx` for the raw data, clean data, KPI definitions and formula-backed summary.
3. Use `power_bi/Power_BI_Build_Guide.md` to recreate the interactive report in Power BI Desktop. DAX and Power Query files are included; the `.pbix` file is not.
4. Present the findings with `presentation/Recruitment_Funnel_Leadership_Readout.pptx`.
5. Review `documentation/Project_Methodology.md` and `documentation/Interview_Walkthrough.md` to explain how the work was done.

## Case question

Where does the fictional hiring pipeline lose candidates, how long does it take to convert an application into a joiner, and which channel deserves a closer review?

## Project period and grain

- Application cohort: 1 January�30 June 2026
- Snapshot date: 30 September 2026
- Grain: one row per candidate application
- Clean candidate rows: 360
- Raw source rows: 366 (includes deliberate data quality issues)

## Key sample findings

- 360 applications resulted in 48 joiners (13.3% overall application-to-join rate).
- Median time to join was 33 days for joined candidates.
- The largest stage loss was 100 records between Screened and Recruiter Interview.
- Careers Page had the highest observed source hire rate (16.9%, n=77); Recruiter Agency was lowest (4.8%, n=42). Treat this as a prompt to investigate, not proof of channel quality.
- 48 of 60 offers were accepted in this sample (80%).

These are findings about a constructed dataset only. Small channel counts, role mix and the artificial data-generation process prevent causal claims.

## Folder guide

- `data/raw`: intentionally imperfect source export
- `data/cleaned`: deduplicated and standardized analysis table
- `analysis`: reproducible summary tables and quality log
- `workbook`: Excel workbook with readable formulas and supporting tabs
- `power_bi`: measures, model setup, visual specification and Power Query steps
- `sql`: SQL Server staging/quality/summary query
- `scripts`: reproducible data generation and cleaning script
- `documentation`: executive readout, methodology, dictionary, interview and AI-use notes
- `presentation`: editable leadership presentation

## Refreshing the analysis

The source is intentionally reproducible. Run `scripts/build_sample_data.py` with Python 3.10+ to regenerate the fictional source and clean outputs. The script uses only the standard library. Then refresh the workbook or follow the Power BI guide. The workbook and Power BI build assets are not connected to any employer system.
