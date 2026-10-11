// Import the raw CSV, then apply these transformations in Power Query.
let
    Source = Csv.Document(File.Contents("candidate_pipeline_raw.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Types = Table.TransformColumnTypes(Headers, {{"Candidate ID", type text}, {"Application Date", type date}, {"Role", type text}, {"Department", type text}, {"Experience Level", type text}, {"Source", type text}, {"Recruiter", type text}, {"Current Stage", type text}, {"Outcome", type text}, {"Applied Date", type date}, {"ScreenedDate", type date}, {"RecruiterInterviewDate", type date}, {"HiringManagerInterviewDate", type date}, {"FinalInterviewDate", type date}, {"OfferDate", type date}, {"JoinedDate", type date}, {"Days to Current Stage", Int64.Type}}),
    UniqueCandidates = Table.Distinct(Types, {"Candidate ID"}),
    SourceFilled = Table.ReplaceValue(UniqueCandidates, null, "Unknown", Replacer.ReplaceValue, {"Source"}),
    FixMilestone = (inputTable as table, columnName as text) as table =>
        let
            Added = Table.AddColumn(inputTable, columnName & "_clean", (row) =>
                let value = Record.Field(row, columnName), applied = Record.Field(row, "Application Date")
                in if value <> null and value < applied then null else value, type nullable date),
            Removed = Table.RemoveColumns(Added, {columnName}),
            Renamed = Table.RenameColumns(Removed, {{columnName & "_clean", columnName}})
        in Renamed,
    FixedMilestones = List.Accumulate({"ScreenedDate", "RecruiterInterviewDate", "HiringManagerInterviewDate", "FinalInterviewDate", "OfferDate", "JoinedDate"}, SourceFilled, FixMilestone),
    AddedStageOrder = Table.AddColumn(FixedMilestones, "Stage Order", each if [Current Stage] = "Applied" then 1 else if [Current Stage] = "Screened" then 2 else if [Current Stage] = "Recruiter Interview" then 3 else if [Current Stage] = "Hiring Manager Interview" then 4 else if [Current Stage] = "Final Interview" then 5 else if [Current Stage] = "Offer" then 6 else if [Current Stage] = "Joined" then 7 else null, Int64.Type),
    Output = AddedStageOrder
in
    Output
