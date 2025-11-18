"""Quick script to create sample data files"""
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

np.random.seed(42)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

# Create sample job postings
roles = ['Data Engineer', 'Data Scientist', 'Software Engineer', 'Data Analyst', 'ML Engineer']
levels = ['Junior', 'Mid', 'Senior']
locations = ['Seattle', 'San Francisco', 'New York', 'Austin', 'Boston', 'Chicago']
comp_types = ['Yearly', 'Hourly']
industries = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Consulting']
remote_types = ['On-site', 'Remote', 'Hybrid']

job_postings = []
skills_data = []
predictions_data = []
employer_offers = []

# Base salaries by role and level
base_salaries = {
    'Data Engineer': {'Junior': 80000, 'Mid': 115000, 'Senior': 155000},
    'Data Scientist': {'Junior': 90000, 'Mid': 130000, 'Senior': 180000},
    'Software Engineer': {'Junior': 75000, 'Mid': 110000, 'Senior': 150000},
    'Data Analyst': {'Junior': 65000, 'Mid': 90000, 'Senior': 120000},
    'ML Engineer': {'Junior': 95000, 'Mid': 140000, 'Senior': 190000}
}

location_multipliers = {
    'San Francisco': 1.25,
    'New York': 1.20,
    'Seattle': 1.15,
    'Boston': 1.10,
    'Chicago': 1.05,
    'Austin': 1.00
}

all_skills = ['Python', 'SQL', 'R', 'Java', 'JavaScript', 'TensorFlow', 'PyTorch', 'AWS', 'Azure', 'GCP', 
              'Spark', 'Kafka', 'Tableau', 'Power BI', 'Excel', 'Machine Learning', 'Deep Learning', 'ETL']

for i in range(1, 101):
    role = np.random.choice(roles)
    level = np.random.choice(levels)
    location = np.random.choice(locations)
    
    base_salary = base_salaries[role][level]
    location_mult = location_multipliers[location]
    salary_mid = int(base_salary * location_mult)
    salary_min = int(salary_mid * 0.85)
    salary_max = int(salary_mid * 1.15)
    
    posted_date = datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))
    
    job_postings.append({
        'PostingID': i,
        'JobTitle': role,
        'RoleLevel': level,
        'Company': f'Company{i}',
        'Location': location,
        'Country': 'USA',
        'Region': 'West' if location in ['Seattle', 'San Francisco'] else 'East',
        'City': location,
        'EmploymentType': 'Full-time',
        'CompensationType': np.random.choice(comp_types, p=[0.95, 0.05]),
        'SalaryMin': salary_min,
        'SalaryMax': salary_max,
        'SalaryMid': salary_mid,
        'PostedDate': posted_date.strftime('%Y-%m-%d'),
        'Source': np.random.choice(['LinkedIn', 'Indeed', 'Glassdoor']),
        'RemoteType': np.random.choice(remote_types),
        'Industry': np.random.choice(industries)
    })
    
    # Add skills (3-7 skills per posting)
    num_skills = np.random.randint(3, 8)
    posting_skills = np.random.choice(all_skills, num_skills, replace=False)
    for skill in posting_skills:
        skills_data.append({
            'PostingID': i,
            'Skills': skill
        })
    
    # Create predictions
    pred_salary = salary_mid + np.random.randint(-10000, 10000)
    predictions_data.append({
        'PostingID': i,
        'PredictedSalary': max(salary_min, pred_salary),
        'PredictedSalaryLower': int(pred_salary * 0.85),
        'PredictedSalaryUpper': int(pred_salary * 1.15),
        'PredictedCompType': 'Yearly',
        'PredictedCompTypeConfidence': round(np.random.uniform(0.8, 1.0), 3),
        'ConfidenceScore': round(np.random.uniform(0.75, 0.95), 3),
        'ModelVersion': 1.0
    })

# Create employer offers
for i, role in enumerate(roles[:4], 1):
    for loc in locations[:5]:
        base = base_salaries[role]['Mid']
        offer = int(base * location_multipliers[loc] * np.random.uniform(0.9, 1.1))
        employer_offers.append({
            'Role': role,
            'Location': loc,
            'SalaryOffer': offer,
            'CompensationType': 'Yearly',
            'PostedDate': (datetime(2024, 1, 1) + timedelta(days=i*10)).strftime('%Y-%m-%d'),
            'Status': 'Active'
        })

# Save to CSV
pd.DataFrame(job_postings).to_csv(os.path.join(data_dir, 'sample_job_postings.csv'), index=False)
pd.DataFrame(skills_data).to_csv(os.path.join(data_dir, 'sample_skills.csv'), index=False)
pd.DataFrame(predictions_data).to_csv(os.path.join(data_dir, 'sample_predictions.csv'), index=False)
pd.DataFrame(employer_offers).to_csv(os.path.join(data_dir, 'sample_employer_offers.csv'), index=False)

print(f"Created sample data files in {data_dir}")
print(f"  - {len(job_postings)} job postings")
print(f"  - {len(skills_data)} skill entries")
print(f"  - {len(predictions_data)} predictions")
print(f"  - {len(employer_offers)} employer offers")



