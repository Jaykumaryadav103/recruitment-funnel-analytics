# Interview Walkthrough

## 90-second project explanation

“I built a fictional recruitment funnel analysis for a growing quantum and AI company. I started with a candidate-level export, documented its grain and created a cleaning log. After removing duplicate IDs, filling missing sources as Unknown and clearing milestone dates that occurred before application, I had 360 unique applications. I defined stage conversion and time-to-join explicitly, then built an Excel summary and a Power BI specification with an overview, channel and data-quality view. In this sample, 48 people joined, median time to join was 33 days, and the largest loss was between screening and recruiter interview. I would investigate the handoff and disposition reasons before proposing a process change. Source results are descriptive because the sample is synthetic and channel groups are small. I also prepared a leadership readout and made the data limitations visible.”

## Likely questions

**Why did you choose this project?** It maps directly to recruitment reporting, data cleaning, dashboard work and explaining a business question to stakeholders.

**How did you define conversion?** A candidate counts as reaching a stage when their furthest completed stage is that stage or later. The denominator is candidates who reached the previous stage.

**What is the main insight?** The biggest count loss is from Screened (318) to Recruiter Interview (218), a gap of 100 candidates. That shows where I would investigate; it does not tell us why the candidates left.

**Would you stop using agencies?** No. The observed sample has only 42 agency applicants and 2 joiners. I would compare the same roles and experience bands, include cost and time, then make a decision with the recruiter team.

**How did you use AI?** I would use it to draft a DAX pattern or summarize verified aggregate results, then check the formula against the source rows. I would never submit identifiable candidate data to an unapproved service.

**What would you improve with real data?** Add stage entry and exit timestamps, offer accepted/declined status, standardized disposition reasons and a role requisition key. Then separate open-candidate aging from completed time-to-hire.

## Demo flow

1. Show the question and synthetic-data notice.
2. Open the workbook KPI and quality tabs.
3. Walk through the funnel and explain the denominator.
4. Show the source comparison with applicant counts.
5. Close with one concrete investigation question and the data you would request next.
