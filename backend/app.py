"""
Flask API Backend for FutureWorks Salary & Compensation Dashboard
Provides endpoints for data, predictions, and analytics
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import json

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

# Load data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Global data storage
job_postings = None
skills = None
predictions = None
employer_offers = None
model_data = None

def load_data():
    """Load all data files"""
    global job_postings, skills, predictions, employer_offers, model_data
    
    try:
        job_postings = pd.read_csv(os.path.join(DATA_DIR, 'sample_job_postings.csv'))
        skills = pd.read_csv(os.path.join(DATA_DIR, 'sample_skills.csv'))
        predictions = pd.read_csv(os.path.join(DATA_DIR, 'sample_predictions.csv'))
        employer_offers = pd.read_csv(os.path.join(DATA_DIR, 'sample_employer_offers.csv'))
        
        # Load model if available
        model_path = os.path.join(BASE_DIR, 'python', 'salary_model.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
        
        print("Data loaded successfully")
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

# Load data on startup
load_data()

# ============================================
# API ENDPOINTS
# ============================================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_loaded': job_postings is not None,
        'model_loaded': model_data is not None
    })

@app.route('/api/job-postings', methods=['GET'])
def get_job_postings():
    """Get all job postings with optional filters"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    if date_from:
        df = df[pd.to_datetime(df['PostedDate']) >= pd.to_datetime(date_from)]
    if date_to:
        df = df[pd.to_datetime(df['PostedDate']) <= pd.to_datetime(date_to)]
    
    return jsonify(df.to_dict('records'))

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    """Get predictions with optional filters"""
    if predictions is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = predictions.copy()
    
    # Merge with job postings for filtering
    if job_postings is not None:
        merged = df.merge(job_postings[['PostingID', 'JobTitle', 'Location']], on='PostingID', how='left')
        
        role = request.args.get('role')
        location = request.args.get('location')
        
        if role:
            merged = merged[merged['JobTitle'] == role]
        if location:
            merged = merged[merged['Location'] == location]
        
        df = merged[df.columns]
    
    return jsonify(df.to_dict('records'))

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get skills data"""
    if skills is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    posting_id = request.args.get('posting_id')
    if posting_id:
        filtered = skills[skills['PostingID'] == int(posting_id)]
        return jsonify(filtered.to_dict('records'))
    
    return jsonify(skills.to_dict('records'))

@app.route('/api/employer-offers', methods=['GET'])
def get_employer_offers():
    """Get employer offers"""
    if employer_offers is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    return jsonify(employer_offers.to_dict('records'))

@app.route('/api/analytics/overview-kpis', methods=['GET'])
def get_overview_kpis():
    """Get overview KPIs: total jobs, total companies, average salary, average experience level"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    # Total Jobs (distinct count of job IDs)
    total_jobs = int(df['PostingID'].nunique()) if 'PostingID' in df.columns else int(len(df))
    
    # Highest Paying Role (role with highest average salary)
    highest_paying_role = None
    highest_paying_salary = 0
    if 'JobTitle' in df.columns and 'SalaryMid' in df.columns:
        role_salaries = df.groupby('JobTitle')['SalaryMid'].mean().sort_values(ascending=False)
        if len(role_salaries) > 0:
            highest_paying_role = role_salaries.index[0]
            highest_paying_salary = float(role_salaries.iloc[0])
    
    # Average Salary (only YEARLY jobs, reasonable range)
    yearly_df = df[df['CompensationType'] == 'Yearly'].copy() if 'CompensationType' in df.columns else df.copy()
    if 'SalaryMid' in yearly_df.columns:
        # Filter reasonable range (20k to 500k)
        yearly_df = yearly_df[(yearly_df['SalaryMid'] >= 20000) & (yearly_df['SalaryMid'] <= 500000)]
        average_salary = float(yearly_df['SalaryMid'].mean()) if len(yearly_df) > 0 else 0
    else:
        average_salary = 0
    
    # Average Experience Level (map to 1-5 scale)
    exp_mapping = {'Entry': 1, 'Junior': 1, 'Mid': 3, 'Senior': 4, 'Executive': 5, 'Lead': 4, 'Principal': 5}
    if 'RoleLevel' in df.columns:
        df['exp_numeric'] = df['RoleLevel'].map(exp_mapping).fillna(3)
        average_experience_level = float(df['exp_numeric'].mean()) if len(df) > 0 else 0
    else:
        average_experience_level = 0
    
    return jsonify({
        'total_jobs': total_jobs,
        'highest_paying_role': highest_paying_role or 'N/A',
        'highest_paying_salary': highest_paying_salary,
        'average_salary': average_salary,
        'average_experience_level': average_experience_level
    })

@app.route('/api/analytics/salary-summary', methods=['GET'])
def get_salary_summary():
    """Get salary summary statistics"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    
    return jsonify({
        'median': float(df['SalaryMid'].median()),
        'average': float(df['SalaryMid'].mean()),
        'min': float(df['SalaryMin'].min()),
        'max': float(df['SalaryMax'].max()),
        'percentile_25': float(df['SalaryMid'].quantile(0.25)),
        'percentile_75': float(df['SalaryMid'].quantile(0.75)),
        'count': int(len(df))
    })

@app.route('/api/analytics/prediction-accuracy', methods=['GET'])
def get_prediction_accuracy():
    """Get prediction accuracy metrics"""
    if predictions is None or job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    # Filter job postings first
    df = job_postings.copy()
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    # Get filtered posting IDs
    filtered_posting_ids = df['PostingID'].unique() if 'PostingID' in df.columns else []
    
    # Filter predictions to only those matching filtered postings
    if len(filtered_posting_ids) > 0:
        filtered_predictions = predictions[predictions['PostingID'].isin(filtered_posting_ids)]
    else:
        filtered_predictions = predictions
    
    # Merge with filtered job postings
    merged = filtered_predictions.merge(
        df[['PostingID', 'SalaryMid']],
        on='PostingID',
        how='inner'
    )
    
    if len(merged) == 0:
        return jsonify({
            'mae': 0,
            'mape': 0,
            'r2': 0,
            'count': 0
        })
    
    merged['Error'] = abs(merged['PredictedSalary'] - merged['SalaryMid'])
    merged['ErrorPct'] = (merged['Error'] / merged['SalaryMid']) * 100
    
    mae = float(merged['Error'].mean())
    mape = float(merged['ErrorPct'].mean())
    
    # Calculate R²
    ss_res = ((merged['SalaryMid'] - merged['PredictedSalary']) ** 2).sum()
    ss_tot = ((merged['SalaryMid'] - merged['SalaryMid'].mean()) ** 2).sum()
    r2 = float(1 - (ss_res / ss_tot)) if ss_tot > 0 else 0
    
    return jsonify({
        'mae': mae,
        'mape': mape,
        'r2': r2,
        'count': int(len(merged))
    })

@app.route('/api/analytics/compensation-distribution', methods=['GET'])
def get_compensation_distribution():
    """Get compensation type distribution"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    distribution = df['CompensationType'].value_counts().to_dict()
    total = len(df)
    
    result = {
        'distribution': {k: int(v) for k, v in distribution.items()},
        'percentages': {k: float((v / total) * 100) for k, v in distribution.items()},
        'total': int(total)
    }
    
    return jsonify(result)

@app.route('/api/analytics/salary-by-role', methods=['GET'])
def get_salary_by_role():
    """Get salary statistics by role"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    result = df.groupby('JobTitle')['SalaryMid'].agg([
        ('median', 'median'),
        ('average', 'mean'),
        ('min', 'min'),
        ('max', 'max'),
        ('count', 'count')
    ]).reset_index()
    
    result = result.sort_values('average', ascending=False)
    
    return jsonify(result.to_dict('records'))

@app.route('/api/analytics/salary-by-location', methods=['GET'])
def get_salary_by_location():
    """Get salary statistics by location"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    result = df.groupby('Location')['SalaryMid'].agg([
        ('median', 'median'),
        ('average', 'mean'),
        ('count', 'count')
    ]).reset_index()
    
    result = result.sort_values('average', ascending=False)
    
    return jsonify(result.to_dict('records'))

@app.route('/api/analytics/salary-trends', methods=['GET'])
def get_salary_trends():
    """Get salary trends over time"""
    if job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    df['PostedDate'] = pd.to_datetime(df['PostedDate'])
    df['YearMonth'] = df['PostedDate'].dt.to_period('M').astype(str)
    
    trends = df.groupby('YearMonth')['SalaryMid'].agg([
        ('median', 'median'),
        ('average', 'mean'),
        ('count', 'count')
    ]).reset_index()
    
    return jsonify(trends.to_dict('records'))

@app.route('/api/analytics/prediction-gaps', methods=['GET'])
def get_prediction_gaps():
    """Get prediction gaps (overpaying/underpaying analysis)"""
    if predictions is None or job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    # Filter job postings first
    df = job_postings.copy()
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    # Get filtered posting IDs
    filtered_posting_ids = df['PostingID'].unique() if 'PostingID' in df.columns else []
    
    # Filter predictions to only those matching filtered postings
    if len(filtered_posting_ids) > 0:
        filtered_predictions = predictions[predictions['PostingID'].isin(filtered_posting_ids)]
    else:
        filtered_predictions = predictions
    
    # Merge with filtered job postings
    merged = filtered_predictions.merge(
        df[['PostingID', 'JobTitle', 'Location', 'SalaryMid']],
        on='PostingID',
        how='inner'
    )
    
    if len(merged) == 0:
        return jsonify([])
    
    merged['Gap'] = merged['SalaryMid'] - merged['PredictedSalary']
    merged['GapPct'] = (merged['Gap'] / merged['PredictedSalary']) * 100
    
    # Categorize
    merged['Category'] = merged['GapPct'].apply(
        lambda x: 'Overpaying' if x > 10 else ('Underpaying' if x < -10 else 'Competitive')
    )
    
    return jsonify(merged.to_dict('records'))

@app.route('/api/analytics/benchmarking', methods=['GET'])
def get_benchmarking():
    """Get benchmarking data (employer vs market)"""
    if employer_offers is None or job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get market data by role and location
    market_data = job_postings.groupby(['JobTitle', 'Location'])['SalaryMid'].agg([
        ('market_median', 'median'),
        ('market_avg', 'mean'),
        ('market_p25', lambda x: x.quantile(0.25)),
        ('market_p75', lambda x: x.quantile(0.75)),
        ('count', 'count')
    ]).reset_index()
    
    # Merge with employer offers
    benchmarking = employer_offers.merge(
        market_data,
        left_on=['Role', 'Location'],
        right_on=['JobTitle', 'Location'],
        how='left'
    )
    
    benchmarking['Gap'] = benchmarking['SalaryOffer'] - benchmarking['market_median']
    benchmarking['GapPct'] = (benchmarking['Gap'] / benchmarking['market_median']) * 100
    
    # Calculate percentile
    def calc_percentile(row):
        if pd.isna(row['market_median']):
            return None
        market_salaries = job_postings[
            (job_postings['JobTitle'] == row['Role']) &
            (job_postings['Location'] == row['Location'])
        ]['SalaryMid']
        if len(market_salaries) == 0:
            return None
        percentile = (market_salaries <= row['SalaryOffer']).sum() / len(market_salaries) * 100
        return float(percentile)
    
    benchmarking['MarketPercentile'] = benchmarking.apply(calc_percentile, axis=1)
    
    return jsonify(benchmarking.to_dict('records'))

@app.route('/api/analytics/top-skills', methods=['GET'])
def get_top_skills():
    """Get top skills by frequency and salary impact"""
    if skills is None or job_postings is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    df = job_postings.copy()
    
    # Apply filters
    role = request.args.get('role')
    location = request.args.get('location')
    compensation_type = request.args.get('compensation_type')
    
    if role:
        df = df[df['JobTitle'] == role]
    if location:
        df = df[df['Location'] == location]
    if compensation_type:
        df = df[df['CompensationType'] == compensation_type]
    
    # Get posting IDs that match filters
    filtered_posting_ids = df['PostingID'].unique() if 'PostingID' in df.columns else []
    
    # Filter skills to only those in filtered postings
    if len(filtered_posting_ids) > 0:
        filtered_skills = skills[skills['PostingID'].isin(filtered_posting_ids)]
    else:
        filtered_skills = skills
    
    # Skill frequency
    skill_counts = filtered_skills['Skills'].value_counts().head(20) if 'Skills' in filtered_skills.columns else pd.Series()
    
    # Calculate average salary per skill
    skill_salaries = []
    for skill in skill_counts.index:
        skill_postings = filtered_skills[filtered_skills['Skills'] == skill]['PostingID'].unique()
        avg_salary = job_postings[job_postings['PostingID'].isin(skill_postings)]['SalaryMid'].mean()
        skill_salaries.append({
            'skill': skill,
            'frequency': int(skill_counts[skill]),
            'average_salary': float(avg_salary) if not pd.isna(avg_salary) else 0
        })
    
    return jsonify(skill_salaries)

@app.route('/api/predict', methods=['POST'])
def predict_salary():
    """Predict salary for a new job posting"""
    if model_data is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    data = request.json
    
    try:
        # Prepare features (simplified - would need full feature engineering)
        # For now, return a prediction based on similar postings
        job_title = data.get('job_title')
        location = data.get('location')
        role_level = data.get('role_level')
        
        # Find similar postings
        similar = job_postings[
            (job_postings['JobTitle'] == job_title) &
            (job_postings['Location'] == location) &
            (job_postings['RoleLevel'] == role_level)
        ]
        
        if len(similar) > 0:
            pred_salary = float(similar['SalaryMid'].median())
            pred_lower = float(pred_salary * 0.85)
            pred_upper = float(pred_salary * 1.15)
        else:
            # Fallback to overall median
            pred_salary = float(job_postings['SalaryMid'].median())
            pred_lower = float(pred_salary * 0.85)
            pred_upper = float(pred_salary * 1.15)
        
        return jsonify({
            'predicted_salary': pred_salary,
            'predicted_lower': pred_lower,
            'predicted_upper': pred_upper,
            'predicted_comp_type': 'Yearly',
            'confidence': 0.85
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/filters/roles', methods=['GET'])
def get_roles():
    """Get list of unique roles"""
    if job_postings is None:
        return jsonify([])
    roles = job_postings['JobTitle'].unique().tolist()
    return jsonify(sorted(roles))

@app.route('/api/filters/locations', methods=['GET'])
def get_locations():
    """Get list of unique locations"""
    if job_postings is None:
        return jsonify([])
    locations = job_postings['Location'].unique().tolist()
    return jsonify(sorted(locations))

@app.route('/api/filters/compensation-types', methods=['GET'])
def get_compensation_types():
    """Get list of compensation types"""
    if job_postings is None:
        return jsonify([])
    types = job_postings['CompensationType'].unique().tolist()
    return jsonify(sorted(types))

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    print("Starting FutureWorks Dashboard API...")
    print(f"Data directory: {DATA_DIR}")
    app.run(debug=True, port=5000, host='0.0.0.0')

