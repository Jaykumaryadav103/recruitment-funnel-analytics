# Project Methodology

## Business question

A growing technical company needs to understand whether its hiring funnel is moving candidates efficiently and where recruiters should investigate process friction. The analysis focuses on recruitment because it is measurable with a well-defined candidate-level grain and maps directly to the advertised HR analytics role.

## Scope and assumptions

The analysis covers applications dated 1 January through 30 June 2026, observed through 30 September 2026. Each row represents one application. The sample contains 360 unique fictional applications after cleaning. Candidate stage is the furthest completed stage at the snapshot. Milestone date fields remain blank where a candidate did not reach that stage.

This is a synthetic exercise. The sample does not estimate any real company's performance, and the data-generation process is not a statistical model of hiring.

## Data preparation

The raw export includes 366 rows. Cleaning applies these explicit rules:

1. Deduplicate by Candidate ID and retain the first occurrence. Six duplicated rows are removed.
2. Replace five blank recruitment sources with `Unknown`; retain the application rather than guessing its source.
3. Remove two milestone dates that precede the application date. Keep the candidate row and other valid information.
4. Preserve valid milestone blanks as blanks. A blank means the stage was not reached or its date is unavailable; it is not converted to zero.
5. Keep stage and outcome distinct. `Current Stage` indicates progress; `Outcome` indicates disposition.

The quality log records each action and count. No demographic or protected-class fields are present.

## KPI definitions

- **Applications:** distinct Candidate ID count in the selected application cohort.
- **Stage reached:** candidates whose Current Stage is at or beyond the named stage in the agreed sequence.
- **Stage conversion:** candidates reaching the next stage divided by candidates reaching the previous stage.
- **Application-to-join rate:** joined candidates divided by applications.
- **Time to join:** calendar days from Application Date to JoinedDate for joined candidates. Report the median to limit the influence of long waits.
- **Offer acceptance rate:** joined candidates divided by candidates reaching Offer. In this sample, no accepted offer can be distinguished from joined; this is a simplifying assumption and real systems should track offer accepted separately.
- **Source hire rate:** joiners divided by applications attributed to that source. It is descriptive and does not control for role mix, seniority, location, or recruiter assignment.

## Findings and interpretation

The biggest absolute loss occurs between Screened and Recruiter Interview (100 of 318 candidates do not appear in the next stage). The next-largest loss is between Recruiter Interview and Hiring Manager Interview (80 of 218). These stages are sensible places to review screen criteria, scheduling waits and disposition completeness. The dataset does not identify why candidates leave, so these are investigation questions rather than confirmed causes.

The Careers Page shows a 16.9% application-to-join rate (13 of 77); Recruiter Agency shows 4.8% (2 of 42). These small descriptive samples do not support a channel ranking on their own. Compare like roles and experience levels, then review cost and recruiter effort before changing spend.

Median time to join is 33 days among 48 joiners. This excludes candidates still in progress and should be read as a completed-hire metric, not a forecast for open candidates.

## Recommended next actions

- Measure days spent in each stage and add a clear disposition reason for every closed application.
- Review the screen-to-recruiter and recruiter-to-manager handoffs with recruiters and hiring managers.
- Compare source conversion within the same role family and experience band before reallocating channel effort.
- Track offer accepted, declined and start date as separate statuses in a real ATS.
- Publish a monthly snapshot with definitions, refresh date, unique application count and a data-quality section.

## Responsible use

Use aggregated views for leadership. Limit row-level access to authorized recruiters, remove candidate identifiers before sharing, and never feed sensitive candidate information into public AI services. AI can draft formulas or summaries, but the analyst must check calculations against source rows and confirm that wording reflects the evidence.
