-- Example SQL Server staging and summary. Update the file location for your environment.
CREATE TABLE #CandidatesRaw (
    CandidateID varchar(12), ApplicationDate date, RoleName varchar(100), Department varchar(60),
    ExperienceLevel varchar(30), SourceName varchar(50), Recruiter varchar(30), CurrentStage varchar(40),
    Outcome varchar(30), AppliedDate date, ScreenedDate date NULL, RecruiterInterviewDate date NULL,
    HiringManagerInterviewDate date NULL, FinalInterviewDate date NULL, OfferDate date NULL,
    JoinedDate date NULL, DaysToCurrentStage int, WithdrawalReason varchar(80) NULL
);
-- Load candidate_pipeline_raw.csv into #CandidatesRaw using the SQL Server import wizard.

WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CandidateID ORDER BY ApplicationDate, CandidateID) AS rn
    FROM #CandidatesRaw
), cleaned AS (
    SELECT CandidateID, ApplicationDate, RoleName, Department, ExperienceLevel,
           COALESCE(NULLIF(SourceName, ''), 'Unknown') AS SourceName,
           Recruiter, CurrentStage, Outcome, AppliedDate,
           CASE WHEN ScreenedDate < ApplicationDate THEN NULL ELSE ScreenedDate END AS ScreenedDate,
           CASE WHEN RecruiterInterviewDate < ApplicationDate THEN NULL ELSE RecruiterInterviewDate END AS RecruiterInterviewDate,
           CASE WHEN HiringManagerInterviewDate < ApplicationDate THEN NULL ELSE HiringManagerInterviewDate END AS HiringManagerInterviewDate,
           CASE WHEN FinalInterviewDate < ApplicationDate THEN NULL ELSE FinalInterviewDate END AS FinalInterviewDate,
           CASE WHEN OfferDate < ApplicationDate THEN NULL ELSE OfferDate END AS OfferDate,
           CASE WHEN JoinedDate < ApplicationDate THEN NULL ELSE JoinedDate END AS JoinedDate,
           DaysToCurrentStage, WithdrawalReason
    FROM ranked WHERE rn = 1
)
SELECT CurrentStage, COUNT(*) AS CandidateCount
FROM cleaned
GROUP BY CurrentStage
ORDER BY CASE CurrentStage WHEN 'Applied' THEN 1 WHEN 'Screened' THEN 2 WHEN 'Recruiter Interview' THEN 3
 WHEN 'Hiring Manager Interview' THEN 4 WHEN 'Final Interview' THEN 5 WHEN 'Offer' THEN 6 WHEN 'Joined' THEN 7 END;
