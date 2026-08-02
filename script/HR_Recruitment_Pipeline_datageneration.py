import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducible, mathematically consistent data
np.random.seed(42)

print("Initializing HR Recruitment Pipeline Data Generation...")

# 1. Dim_Jobs: 50 Open Requisitions across 6 Departments
departments = ['Engineering', 'Data & BI', 'Product', 'Sales', 'Marketing', 'HR & Operations']
levels = ['L1 - Junior', 'L2 - Mid', 'L3 - Senior', 'L4 - Lead', 'L5 - Manager']
hiring_managers = ['Sarah Jenkins', 'David Chen', 'Elena Rostova', 'Marcus Brody', 'Priya Patel', 'James Wilson']

jobs_data = []
base_date = datetime(2025, 1, 1)
for i in range(1, 51):
    dept = np.random.choice(departments, p=[0.30, 0.25, 0.15, 0.15, 0.10, 0.05])
    lvl = np.random.choice(levels, p=[0.20, 0.35, 0.25, 0.15, 0.05])
    hm = np.random.choice(hiring_managers)
    open_date = base_date + timedelta(days=int(np.random.randint(0, 150)))
    target_days = np.random.choice([30, 45, 60, 90], p=[0.20, 0.40, 0.30, 0.10])
    budget = max(55000, (int(np.random.normal(95000, 25000)) // 5000) * 5000)
    
    jobs_data.append({
        'JobID': f"REQ-{202500 + i}",
        'Department': dept,
        'Job_Title': f"{dept} Specialist ({lvl.split(' - ')[1]})",
        'Level': lvl,
        'Hiring_Manager': hm,
        'Date_Opened': open_date.strftime('%Y-%m-%d'),
        'Target_SLA_Days': target_days,
        'Budgeted_Salary': budget
    })
df_jobs = pd.DataFrame(jobs_data)

# 2. Dim_Recruiters: 8 Specialized Recruiters
recruiters_data = [
    {'RecruiterID': 'REC-01', 'Recruiter_Name': 'Alex Mercer', 'Specialization': 'Engineering', 'Seniority': 'Senior'},
    {'RecruiterID': 'REC-02', 'Recruiter_Name': 'Jordan Vance', 'Specialization': 'Data & BI', 'Seniority': 'Senior'},
    {'RecruiterID': 'REC-03', 'Recruiter_Name': 'Taylor Swift', 'Specialization': 'Sales', 'Seniority': 'Mid'},
    {'RecruiterID': 'REC-04', 'Recruiter_Name': 'Morgan Sterling', 'Specialization': 'Product', 'Seniority': 'Lead'},
    {'RecruiterID': 'REC-05', 'Recruiter_Name': 'Casey Ryans', 'Specialization': 'Marketing', 'Seniority': 'Junior'},
    {'RecruiterID': 'REC-06', 'Recruiter_Name': 'Riley Thorne', 'Specialization': 'HR & Operations', 'Seniority': 'Mid'},
    {'RecruiterID': 'REC-07', 'Recruiter_Name': 'Jamie Lee', 'Specialization': 'Engineering', 'Seniority': 'Junior'},
    {'RecruiterID': 'REC-08', 'Recruiter_Name': 'Quinn Fabray', 'Specialization': 'Data & BI', 'Seniority': 'Mid'}
]
df_recruiters = pd.DataFrame(recruiters_data)

# 3. Dim_Stages: 7 Standard Recruitment Stages with SLA Targets
stages_data = [
    {'StageID': 1, 'Stage_Name': '1-Application Applied', 'Standard_SLA_Days': 2},
    {'StageID': 2, 'Stage_Name': '2-Recruiter Screen', 'Standard_SLA_Days': 5},
    {'StageID': 3, 'Stage_Name': '3-Technical Assessment', 'Standard_SLA_Days': 7},
    {'StageID': 4, 'Stage_Name': '4-Panel Interview', 'Standard_SLA_Days': 10},
    {'StageID': 5, 'Stage_Name': '5-HR Fit & Negotiation', 'Standard_SLA_Days': 5},
    {'StageID': 6, 'Stage_Name': '6-Offer Extended', 'Standard_SLA_Days': 3},
    {'StageID': 7, 'Stage_Name': '7-Hired / Finalized', 'Standard_SLA_Days': 0}
]
df_stages = pd.DataFrame(stages_data)

# 4. Dim_Candidates & Fact Tables: Simulate 1,200 Applications
sources = ['LinkedIn', 'Employee Referral', 'Company Career Site', 'Agency', 'Direct Sourcing']
first_names = ['Liam', 'Noah', 'Oliver', 'Emma', 'Charlotte', 'Amelia', 'Sophia', 'Mateo', 'Lucas', 'Maya', 'Aarav', 'Zanya', 'Kai', 'Elena', 'Hiro']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Patel', 'Kim', 'Nakamura', 'Gupta', 'Silva']

candidates_data, apps_data, stage_movements = [], [], []
app_id_counter = 1001

for i in range(1, 1201):
    cand_id = f"CND-{10000 + i}"
    name = f"{np.random.choice(first_names)} {np.random.choice(last_names)}"
    edu = np.random.choice(['Bachelors', 'Masters', 'PhD', 'Bootcamp / Diploma'], p=[0.55, 0.30, 0.05, 0.10])
    exp = int(np.random.randint(1, 15))
    source = np.random.choice(sources, p=[0.40, 0.20, 0.25, 0.10, 0.05])
    
    candidates_data.append({
        'CandidateID': cand_id, 'Candidate_Name': name,
        'Education_Level': edu, 'Experience_Years': exp, 'Sourcing_Channel': source
    })
    
    job = df_jobs.sample(1).iloc[0]
    job_id = job['JobID']
    
    # Assign recruiter based on department specialization
    matching_recs = df_recruiters[df_recruiters['Specialization'] == job['Department']]
    rec_id = matching_recs.sample(1).iloc[0]['RecruiterID'] if len(matching_recs) > 0 else df_recruiters.sample(1).iloc[0]['RecruiterID']
        
    app_date = datetime.strptime(job['Date_Opened'], '%Y-%m-%d') + timedelta(days=int(np.random.randint(1, 40)))
    current_date = app_date
    max_stage = 1
    final_status = "Rejected"
    rej_reason = "Resume Screen Failure"
    tech_score, interview_score, time_to_hire = np.nan, np.nan, np.nan
    
    # Log Stage 1: Application
    stage_movements.append({
        'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
        'StageID': 1, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
    })
    
    # Simulate Funnel Progression
    if np.random.rand() < 0.75: # Pass to Stage 2: Recruiter Screen
        max_stage = 2
        current_date += timedelta(days=int(np.random.randint(1, 5)))
        stage_movements.append({
            'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
            'StageID': 2, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
        })
        
        if np.random.rand() < 0.60: # Pass to Stage 3: Technical Assessment
            max_stage = 3
            current_date += timedelta(days=int(np.random.randint(3, 8)))
            tech_score = min(100, max(30, int(np.random.normal(72, 12))))
            stage_movements.append({
                'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
                'StageID': 3, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
            })
            
            if tech_score >= 68 and np.random.rand() < 0.70: # Pass to Stage 4: Panel Interview
                max_stage = 4
                current_date += timedelta(days=int(np.random.randint(5, 12)))
                interview_score = min(100, max(50, int(np.random.normal(80, 8))))
                stage_movements.append({
                    'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
                    'StageID': 4, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
                })
                
                if interview_score >= 75 and np.random.rand() < 0.65: # Pass to Stage 5: HR Fit
                    max_stage = 5
                    current_date += timedelta(days=int(np.random.randint(2, 6)))
                    stage_movements.append({
                        'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
                        'StageID': 5, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
                    })
                    
                    if np.random.rand() < 0.80: # Pass to Stage 6: Offer Extended
                        max_stage = 6
                        current_date += timedelta(days=int(np.random.randint(1, 4)))
                        stage_movements.append({
                            'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
                            'StageID': 6, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Completed'
                        })
                        
                        if np.random.rand() < 0.85: # Stage 7: Hired!
                            max_stage = 7
                            final_status = "Hired"
                            rej_reason = "None - Hired"
                            current_date += timedelta(days=int(np.random.randint(1, 5)))
                            time_to_hire = (current_date - app_date).days
                            stage_movements.append({
                                'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
                                'StageID': 7, 'Stage_Enter_Date': current_date.strftime('%Y-%m-%d'), 'Stage_Status': 'Hired'
                            })
                        else:
                            final_status = "Offer Declined"
                            rej_reason = "Salary Expectation Mismatch"
                            
    if final_status == "Rejected":
        if max_stage in [1, 2]: rej_reason = np.random.choice(['Technical Skills Gap', 'Position Closed', 'Candidate Withdrew'])
        elif max_stage == 3: rej_reason = 'Failed Assessment'
        elif max_stage in [4, 5]: rej_reason = np.random.choice(['Culture Fit / Soft Skills', 'Better Candidate Selected'])

    apps_data.append({
        'ApplicationID': f"APP-{app_id_counter}", 'CandidateID': cand_id, 'JobID': job_id,
        'RecruiterID': rec_id, 'Application_Date': app_date.strftime('%Y-%m-%d'),
        'Current_StageID': max_stage, 'Final_Status': final_status,
        'Assessment_Score': tech_score, 'Interview_Score': interview_score,
        'Time_to_Hire_Days': time_to_hire, 'Rejection_Reason': rej_reason
    })
    app_id_counter += 1

df_candidates = pd.DataFrame(candidates_data)
df_apps = pd.DataFrame(apps_data)
df_movements = pd.DataFrame(stage_movements)

# Export to a structured multi-tab Excel Workbook
output_filename = "HR_Recruitment_Data_Architecture.xlsx"
with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
    df_jobs.to_excel(writer, sheet_name='Dim_Jobs', index=False)
    df_recruiters.to_excel(writer, sheet_name='Dim_Recruiters', index=False)
    df_stages.to_excel(writer, sheet_name='Dim_Stages', index=False)
    df_candidates.to_excel(writer, sheet_name='Dim_Candidates', index=False)
    df_apps.to_excel(writer, sheet_name='Fact_Applications', index=False)
    df_movements.to_excel(writer, sheet_name='Fact_Stage_Movements', index=False)

print(f"Success! Generated '{output_filename}' containing 6 structured tables.")