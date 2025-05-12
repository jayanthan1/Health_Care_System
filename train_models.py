import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os
from PIL import Image, ImageDraw, ImageFont

def create_sample_dataset():
    # Create sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'bmi': np.random.normal(25, 5, n_samples),
        'glucose_level': np.random.normal(100, 20, n_samples),
        'cholesterol': np.random.normal(200, 30, n_samples),
        'heart_rate': np.random.normal(75, 10, n_samples),
        'smoking_status': np.random.randint(0, 2, n_samples),
        'alcohol_consumption': np.random.randint(0, 4, n_samples),
        'physical_activity': np.random.normal(30, 10, n_samples),
        'sleep_hours': np.random.normal(7, 1, n_samples),
        'stress_level': np.random.randint(1, 11, n_samples),
        'disease_risk': np.random.randint(0, 2, n_samples),
        'overall_health_risk': np.random.randint(0, 101, n_samples)
    })
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save the dataset
    data.to_csv('data/health_dataset.csv', index=False)
    return data

def train_health_models():
    try:
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Create sample data
        n_samples = 1000
        data = pd.DataFrame({
            'age': np.random.randint(18, 80, n_samples),
            'bmi': np.random.normal(25, 5, n_samples),
            'glucose_level': np.random.normal(100, 20, n_samples),
            'cholesterol': np.random.normal(200, 30, n_samples),
            'heart_rate': np.random.normal(75, 10, n_samples),
            'smoking_status': np.random.randint(0, 2, n_samples),
            'alcohol_consumption': np.random.randint(0, 4, n_samples),
            'physical_activity': np.random.normal(30, 10, n_samples),
            'sleep_hours': np.random.normal(7, 1, n_samples),
            'stress_level': np.random.randint(1, 11, n_samples),
            'target': np.random.randint(0, 101, n_samples)  # Health score
        })
        
        # Prepare features
        features = data.drop('target', axis=1)
        
        # Train projection model (this is what was failing before)
        projection_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Create proper projection training data
        projection_data = pd.DataFrame()
        for follows in [0, 1]:  # For both following and not following recommendations
            temp_data = features.copy()
            temp_data['follows_recommendations'] = follows
            projection_data = pd.concat([projection_data, temp_data])
        
        # Create corresponding targets with better outcomes for following recommendations
        projection_targets = np.concatenate([
            data['target'].values,  # Original targets
            data['target'].values * 1.2  # 20% better outcomes for following recommendations
        ])
        
        # Train the projection model
        projection_model.fit(projection_data, projection_targets)
        
        # Save all models
        joblib.dump(projection_model, 'models/health_projection_model.pkl')
        
        # Also train and save other models
        disease_model = RandomForestClassifier(n_estimators=100, random_state=42)
        disease_model.fit(features, data['target'] > 50)
        
        risk_model = RandomForestRegressor(n_estimators=100, random_state=42)
        risk_model.fit(features, data['target'])
        
        joblib.dump(disease_model, 'models/disease_prediction_model.pkl')
        joblib.dump(risk_model, 'models/risk_assessment_model.pkl')
        
        print("Models trained and saved successfully!")
        
    except Exception as e:
        print(f"Error training models: {str(e)}")
        raise  # Re-raise the exception to see the full error trace

def create_placeholder_logo():
    if not os.path.exists('static/images/logo.png'):
        # Create directory if it doesn't exist
        os.makedirs('static/images', exist_ok=True)
        
        # Create a simple logo
        img = Image.new('RGB', (200, 200), color='white')
        d = ImageDraw.Draw(img)
        d.ellipse([40, 40, 160, 160], fill='#2575fc')
        d.text((85, 85), "HP", fill='white', font=ImageFont.load_default())
        
        # Save the logo
        img.save('static/images/logo.png')

if __name__ == "__main__":
    train_health_models()
    create_placeholder_logo()