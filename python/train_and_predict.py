"""
Enhanced Salary & Compensation Prediction Model
Trains models and generates predictions for Dashboard
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
import pickle
import os
import json
from datetime import datetime

np.random.seed(42)

def load_and_prepare_data(job_postings_path, skills_path):
    """Load and prepare data for modeling"""
    print("Loading data...")
    df_jobs = pd.read_csv(job_postings_path)
    df_skills = pd.read_csv(skills_path)
    
    # Merge skills into job postings
    skills_grouped = df_skills.groupby('PostingID')['Skills'].apply(
        lambda x: ','.join(x.astype(str))
    ).reset_index()
    skills_grouped.columns = ['PostingID', 'AllSkills']
    
    df = df_jobs.merge(skills_grouped, on='PostingID', how='left')
    
    # Extract individual skills as binary features
    all_skills = set()
    for skills_str in df['AllSkills'].dropna():
        all_skills.update([s.strip() for s in str(skills_str).split(',')])
    
    # Create binary skill features
    for skill in all_skills:
        if skill and len(skill) > 0:
            df[f'Has_{skill}'] = df['AllSkills'].apply(
                lambda x: 1 if pd.notna(x) and skill in str(x) else 0
            )
    
    return df, list(all_skills)

def encode_categorical_features(df):
    """Encode categorical features"""
    df_encoded = df.copy()
    
    encoders = {}
    categorical_cols = ['JobTitle', 'RoleLevel', 'Location', 'Industry', 'RemoteType']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df_encoded[f'{col}_Encoded'] = le.fit_transform(df_encoded[col].astype(str))
        encoders[col] = le
    
    return df_encoded, encoders

def train_salary_model(df, target_col='SalaryMid'):
    """Train salary prediction model"""
    feature_cols = [
        'JobTitle_Encoded', 'RoleLevel_Encoded', 'Location_Encoded',
        'Industry_Encoded', 'RemoteType_Encoded'
    ] + [col for col in df.columns if col.startswith('Has_')]
    
    X = df[feature_cols].fillna(0)
    y = df[target_col]
    
    mask = ~y.isna()
    X = X[mask]
    y = y[mask]
    
    if len(X) == 0:
        raise ValueError("No valid data for training")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    metrics = {
        'train_mae': mean_absolute_error(y_train, y_pred_train),
        'test_mae': mean_absolute_error(y_test, y_pred_test),
        'test_mape': mean_absolute_percentage_error(y_test, y_pred_test) * 100,
        'test_r2': r2_score(y_test, y_pred_test)
    }
    
    feature_importance = dict(zip(feature_cols, model.feature_importances_))
    
    print(f"\nSalary Model Performance:")
    print(f"  Training MAE: ${metrics['train_mae']:,.2f}")
    print(f"  Test MAE: ${metrics['test_mae']:,.2f}")
    print(f"  Test MAPE: {metrics['test_mape']:.2f}%")
    print(f"  Test R2: {metrics['test_r2']:.4f}")
    
    return model, feature_cols, metrics, feature_importance

def train_compensation_type_model(df):
    """Train compensation type prediction model"""
    feature_cols = [
        'JobTitle_Encoded', 'RoleLevel_Encoded', 'Location_Encoded',
        'Industry_Encoded', 'RemoteType_Encoded'
    ] + [col for col in df.columns if col.startswith('Has_')]
    
    X = df[feature_cols].fillna(0)
    y = df['CompensationType']
    
    mask = ~y.isna()
    X = X[mask]
    y = y[mask]
    
    le_comp = LabelEncoder()
    y_encoded = le_comp.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    metrics = {
        'train_accuracy': train_acc * 100,
        'test_accuracy': test_acc * 100
    }
    
    feature_importance = dict(zip(feature_cols, model.feature_importances_))
    
    print(f"\nCompensation Type Model Performance:")
    print(f"  Training Accuracy: {metrics['train_accuracy']:.2f}%")
    print(f"  Test Accuracy: {metrics['test_accuracy']:.2f}%")
    
    return model, feature_cols, le_comp, metrics, feature_importance

def generate_predictions(df, salary_model, comp_model, feature_cols, encoders, comp_encoder):
    """Generate predictions with confidence intervals"""
    predictions = []
    
    for idx, row in df.iterrows():
        # Prepare features
        features = []
        for col in feature_cols:
            if col in df.columns:
                val = row[col] if pd.notna(row[col]) else 0
                features.append(val)
            else:
                features.append(0)
        
        features_array = np.array(features).reshape(1, -1)
        
        # Predict salary
        pred_salary = salary_model.predict(features_array)[0]
        
        # Get prediction intervals
        tree_preds = [tree.predict(features_array)[0] for tree in salary_model.estimators_]
        std_dev = np.std(tree_preds)
        pred_lower = max(0, pred_salary - 1.96 * std_dev)
        pred_upper = pred_salary + 1.96 * std_dev
        
        # Predict compensation type
        comp_proba = comp_model.predict_proba(features_array)[0]
        comp_pred = comp_model.predict(features_array)[0]
        comp_type = comp_encoder.inverse_transform([comp_pred])[0]
        comp_confidence = max(comp_proba)
        
        # Calculate overall confidence
        salary_confidence = max(0.5, min(0.95, 1 - (std_dev / pred_salary) if pred_salary > 0 else 0.5))
        overall_confidence = (salary_confidence + comp_confidence) / 2
        
        predictions.append({
            'PostingID': int(row['PostingID']),
            'PredictedSalary': int(round(pred_salary)),
            'PredictedSalaryLower': int(round(pred_lower)),
            'PredictedSalaryUpper': int(round(pred_upper)),
            'PredictedCompType': comp_type,
            'PredictedCompTypeConfidence': round(comp_confidence, 3),
            'ConfidenceScore': round(overall_confidence, 3),
            'ModelVersion': 1.0
        })
    
    return pd.DataFrame(predictions)

def main():
    """Main execution"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    job_postings_path = os.path.join(base_dir, 'data', 'sample_job_postings.csv')
    skills_path = os.path.join(base_dir, 'data', 'sample_skills.csv')
    predictions_path = os.path.join(base_dir, 'data', 'sample_predictions.csv')
    model_path = os.path.join(base_dir, 'python', 'salary_model.pkl')
    importance_path = os.path.join(base_dir, 'python', 'feature_importance.json')
    
    print("=" * 60)
    print("FutureWorks Salary & Compensation Prediction Model")
    print("=" * 60)
    
    # Load and prepare data
    df, all_skills = load_and_prepare_data(job_postings_path, skills_path)
    print(f"Loaded {len(df)} job postings with {len(all_skills)} unique skills")
    
    # Encode features
    df_encoded, encoders = encode_categorical_features(df)
    print("Features encoded")
    
    # Train models
    salary_model, salary_features, salary_metrics, salary_importance = train_salary_model(df_encoded)
    comp_model, comp_features, comp_encoder, comp_metrics, comp_importance = train_compensation_type_model(df_encoded)
    
    # Generate predictions
    print("\nGenerating predictions...")
    predictions_df = generate_predictions(
        df_encoded, salary_model, comp_model,
        salary_features, encoders, comp_encoder
    )
    
    # Save predictions
    predictions_df.to_csv(predictions_path, index=False)
    print(f"\n[OK] Predictions saved to: {predictions_path}")
    print(f"  Generated {len(predictions_df)} predictions")
    
    # Save models
    model_data = {
        'salary_model': salary_model,
        'comp_model': comp_model,
        'salary_features': salary_features,
        'comp_features': comp_features,
        'encoders': encoders,
        'comp_encoder': comp_encoder,
        'metrics': {
            'salary': salary_metrics,
            'compensation_type': comp_metrics
        },
        'trained_date': datetime.now().isoformat()
    }
    
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    print(f"[OK] Models saved to: {model_path}")
    
    # Save feature importance
    importance_data = {
        'salary_model': {
            'top_features': sorted(
                salary_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:20]
        },
        'compensation_type_model': {
            'top_features': sorted(
                comp_importance.items(),
                key=lambda x: x[1],
                reverse=True
            )[:20]
        }
    }
    
    os.makedirs(os.path.dirname(importance_path), exist_ok=True)
    with open(importance_path, 'w') as f:
        json.dump(importance_data, f, indent=2)
    print(f"[OK] Feature importance saved to: {importance_path}")
    
    print("\n" + "=" * 60)
    print("Model Training Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()



