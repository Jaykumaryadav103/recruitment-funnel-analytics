import csv, json, random, math, statistics, os, textwrap
from pathlib import Path
from datetime import date, timedelta
from collections import Counter, defaultdict
BASE=Path(__file__).resolve().parents[1]
for d in ['data/raw','data/cleaned','analysis','power_bi','documentation','presentation','sql','scripts']:(BASE/d).mkdir(parents=True,exist_ok=True)
rng=random.Random(20261011)
roles=['Quantum Software Engineer','AI Research Associate','ML Engineer','Solutions Engineer','People Operations Analyst','Product Manager']
sources=['Employee Referral','LinkedIn','Careers Page','Campus','Recruiter Agency']
stages=['Applied','Screened','Recruiter Interview','Hiring Manager Interview','Final Interview','Offer','Joined']
# Planned cohort counts by furthest completed stage, totaling 360.
cohort=['Joined']*48+['Offer']*12+['Final Interview']*28+['Hiring Manager Interview']*50+['Recruiter Interview']*80+['Screened']*100+['Applied']*42
rng.shuffle(cohort)
base=date(2026,1,1)
rows=[]
source_weights={'Employee Referral':.24,'LinkedIn':.26,'Careers Page':.22,'Campus':.16,'Recruiter Agency':.12}
for i,furthest in enumerate(cohort,1):
    source=rng.choices(list(source_weights),weights=list(source_weights.values()))[0]
    role=rng.choice(roles)
    app=base+timedelta(days=rng.randrange(181))
    level=rng.choice(['Entry','Early Career','Experienced'])
    # elapsed durations by milestone, with a modest source-dependent wait component
    ds=[0,rng.randint(1,5),rng.randint(3,8),rng.randint(4,10),rng.randint(3,8),rng.randint(2,7),rng.randint(3,12)]
    dates=[app]
    for j in range(1,len(ds)): dates.append(dates[-1]+timedelta(days=ds[j]))
    furthest_idx=stages.index(furthest)
    # only dates up to furthest stage are visible; later milestones stay blank
    record={'Candidate ID':f'C{i:04d}','Application Date':app.isoformat(),'Role':role,'Department':'People & Culture' if 'People' in role else ('AI' if 'AI' in role or 'ML' in role else ('Quantum' if 'Quantum' in role else 'Business')),'Experience Level':level,'Source':source,'Recruiter':rng.choice(['Recruiter A','Recruiter B','Recruiter C']),'Current Stage':furthest,'Outcome':'Joined' if furthest=='Joined' else ('Offer Declined' if furthest=='Offer' and rng.random()<.25 else ('In Progress' if rng.random()<.48 else 'Not Selected')),'Applied Date':dates[0].isoformat()}
    for j,stage in enumerate(stages[1:],1):
        key=stage.replace(' ','')+'Date'
        record[key]=dates[j].isoformat() if j<=furthest_idx else ''
    record['Days to Current Stage']=(dates[furthest_idx]-app).days
    record['Withdrawal Reason']='' if record['Outcome'] not in ['Offer Declined','Not Selected'] else rng.choice(['Compensation','Accepted another offer','Role fit','Availability','Assessment outcome'])
    rows.append(record)
# create 5 raw source gaps, 2 impossible milestone dates, and 6 duplicated records (data QA exercise)
for idx in [9,77,121,211,298]: rows[idx]['Source']=''
for idx in [i for i,row in enumerate(rows) if stages.index(row['Current Stage'])>=2][:2]:
    j=stages.index(rows[idx]['Current Stage'])
    rows[idx][stages[j].replace(' ','')+'Date']=(date.fromisoformat(rows[idx]['Applied Date'])-timedelta(days=2)).isoformat()
raw=rows+[dict(rows[k]) for k in [12,55,101,177,246,319]]
headers=list(rows[0].keys())
def save_csv(path, data):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(data)
save_csv(BASE/'data/raw/candidate_pipeline_raw.csv',raw)
# clean: deduplicate by ID, source gaps to explicit unknown, impossible dated milestone removed (preserves core record and logs issue)
clean=[]; dq=[]
seen=set()
for row in raw:
    if row['Candidate ID'] in seen:
        dq.append({'Issue':'Duplicate candidate record','Count':1,'Treatment':'Kept first record by Candidate ID; later duplicate removed.'}); continue
    seen.add(row['Candidate ID'])
    r=dict(row)
    if not r['Source']:
        r['Source']='Unknown'
        dq.append({'Issue':'Missing recruitment source','Count':1,'Treatment':'Mapped blank to Unknown; retained record.'})
    for j,stage in enumerate(stages[1:],1):
        key=stage.replace(' ','')+'Date'
        if r[key] and date.fromisoformat(r[key])<date.fromisoformat(r['Applied Date']):
            r[key]=''
            dq.append({'Issue':'Milestone date before application','Count':1,'Treatment':f'Removed invalid {stage} date; retained candidate row.'})
    clean.append(r)
save_csv(BASE/'data/cleaned/candidate_pipeline_clean.csv',clean)
with open(BASE/'analysis/data_quality_log.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['Issue','Count','Treatment']); w.writeheader()
    for issue,count in sorted(Counter(x['Issue'] for x in dq).items()):
        treatment=next(x['Treatment'] for x in dq if x['Issue']==issue);w.writerow({'Issue':issue,'Count':count,'Treatment':treatment})
# analysis
n=len(clean); current=Counter(r['Current Stage'] for r in clean)
reached={s:sum(1 for r in clean if stages.index(r['Current Stage'])>=stages.index(s)) for s in stages}
conv=[]
for i,s in enumerate(stages):
    conv.append({'Stage':s,'Candidates Reached':reached[s],'Conversion from Previous':None if i==0 else reached[s]/reached[stages[i-1]],'Drop from Previous':None if i==0 else reached[stages[i-1]]-reached[s]})
joined=[r for r in clean if r['Outcome']=='Joined']
hire_days=[(date.fromisoformat(r['JoinedDate'])-date.fromisoformat(r['Applied Date'])).days for r in joined if r['JoinedDate']]
source_summary=[]
for s in ['Employee Referral','LinkedIn','Careers Page','Campus','Recruiter Agency','Unknown']:
    rs=[r for r in clean if r['Source']==s]
    if rs: source_summary.append({'Source':s,'Applicants':len(rs),'Joined':sum(r['Outcome']=='Joined' for r in rs),'Hire Rate':sum(r['Outcome']=='Joined' for r in rs)/len(rs),'Median Days to Join':statistics.median([(date.fromisoformat(r['JoinedDate'])-date.fromisoformat(r['Applied Date'])).days for r in rs if r['JoinedDate']]) if any(r['JoinedDate'] for r in rs) else None})
role_summary=[]
for role in roles:
    rs=[r for r in clean if r['Role']==role]
    role_summary.append({'Role':role,'Applicants':len(rs),'Joined':sum(r['Outcome']=='Joined' for r in rs),'Hire Rate':sum(r['Outcome']=='Joined' for r in rs)/len(rs) if rs else 0})
metrics={'applicants':n,'joined':len(joined),'overall_join_rate':len(joined)/n,'median_days_to_join':statistics.median(hire_days),'mean_days_to_join':statistics.mean(hire_days),'cleaned_rows':n,'raw_rows':len(raw),'duplicate_records':len(raw)-len(clean),'recruiter_to_hm_drop':reached['Recruiter Interview']-reached['Hiring Manager Interview'],'recruiter_to_hm_rate':reached['Hiring Manager Interview']/reached['Recruiter Interview'],'stage_counts':reached,'source_summary':source_summary,'role_summary':role_summary}
(BASE/'analysis/metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
with open(BASE/'analysis/funnel_summary.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=conv[0].keys());w.writeheader();w.writerows(conv)
with open(BASE/'analysis/source_summary.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=source_summary[0].keys());w.writeheader();w.writerows(source_summary)
with open(BASE/'analysis/role_summary.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=role_summary[0].keys());w.writeheader();w.writerows(role_summary)
# data dictionary
with open(BASE/'documentation/data_dictionary.csv','w',newline='',encoding='utf-8-sig') as f:
 fields=['Field','Definition','Type','Example / allowed values','Handling note'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 defs=[('Candidate ID','Synthetic unique row key','Text','C0001','No real personal identifier'),('Application Date','Date candidate applied','Date','2026-02-14','ISO 8601'),('Role','Role applied to','Category','ML Engineer','Synthetic role'),('Department','Mapped hiring department','Category','AI','Synthetic grouping'),('Experience Level','Broad experience band','Category','Early Career','No age or protected class'),('Source','Recruitment source','Category','LinkedIn, Unknown','Missing values mapped to Unknown'),('Recruiter','Synthetic recruiter label','Category','Recruiter A','Not a real person'),('Current Stage','Furthest completed stage','Category','Interview, Joined','Stage ordering in KPI definitions'),('Outcome','Current disposition','Category','Joined, In Progress','Offer declined separate'),('Applied Date','Application milestone date','Date','2026-02-14','Same as Application Date'),('ScreenedDate','Screen milestone date','Date or blank','2026-02-18','Blank means stage not reached'),('RecruiterInterviewDate','Recruiter interview date','Date or blank','2026-02-24','Blank means stage not reached'),('HiringManagerInterviewDate','Hiring manager interview date','Date or blank','2026-03-01','Blank means stage not reached'),('FinalInterviewDate','Final interview date','Date or blank','2026-03-08','Blank means stage not reached'),('OfferDate','Offer date','Date or blank','2026-03-11','Blank means stage not reached'),('JoinedDate','Start date','Date or blank','2026-03-20','Blank means not joined'),('Days to Current Stage','Days from application to latest stage','Integer','18','For joined, equals time to join'),('Withdrawal Reason','Disposition reason','Category or blank','Accepted another offer','Synthetic, incomplete by design')]
 for r in defs:w.writerow(dict(zip(fields,r)))
