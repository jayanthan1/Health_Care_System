import os
import fitz
import pandas as pd
import joblib
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, send_file
from sklearn.ensemble import RandomForestClassifier
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import PyPDF2
import re
import numpy as np
from health_recommendations import generate_health_recommendations, calculate_risk_factors, calculate_protein_needs, calculate_carb_needs, calculate_fat_needs, calculate_fiber_needs, track_activity_progress, generate_health_projections, get_recommended_foods, generate_meal_schedule, calculate_health_decline
from database import init_db, add_user, save_pdf_analysis, update_health_data_from_pdf, get_user_by_email
from pdf_analyzer import analyze_pdf
from datetime import datetime
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Add these configurations after creating the Flask app
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Connection
def get_db_connection():
    try:
        conn = sqlite3.connect('health_db.sqlite')  # Use SQLite database file
        conn.row_factory = sqlite3.Row  # Enable row access by name
        print("Database connection successful")  # Debugging
        return conn
    except sqlite3.Error as err:
        print(f"Database Connection Error: {err}")  # Log the error
        return None

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    session.clear()  # Clear session before registering a new user

    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            age = request.form['age']
            gender = request.form['gender']

            if get_user_by_email(email):
                flash('Email already registered. Please use a different email.', 'danger')
                return render_template('register.html')

            # Add user to the database
            user_id = add_user(name, email, password, age, gender)
            if user_id:
                # Save health data
                health_data = {
                    'user_id': user_id,
                    'height': request.form['height'],
                    'weight': request.form['weight'],
                    'blood_pressure': request.form['blood_pressure'],
                    'heart_rate': request.form['heart_rate'],
                    # Other health data...
                }
                save_health_data(user_id, health_data)
                flash('Registration successful!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error registering user. Please try again.', 'danger')
        except Exception as e:
            print(f"Error during registration: {e}")
            flash('An error occurred. Please try again.', 'danger')
    return render_template('register.html')

def analyze_health_data(health_data):
    """
    Analyze health data using machine learning models
    Returns predictions and recommendations
    """
    try:
        # Load the trained models
        disease_model = joblib.load('models/disease_prediction_model.pkl')
        risk_model = joblib.load('models/risk_assessment_model.pkl')

        # Prepare features for prediction
        features = np.array([[
            health_data['age'],
            health_data['bmi'],
            health_data['glucose_level'],
            health_data['cholesterol'],
            health_data['heart_rate'],
            health_data['smoking_status'],
            health_data['alcohol_consumption'],
            health_data['physical_activity'],
            health_data['sleep_hours'],
            health_data['stress_level']
        ]])

        # Get predictions
        disease_risk = disease_model.predict_proba(features)[0]
        overall_risk = risk_model.predict_proba(features)[0]

        # Generate recommendations based on risk factors
        recommendations = generate_health_recommendations(health_data, disease_risk)

        return {
            'prediction_type': 'comprehensive',
            'risk_score': float(overall_risk[1] * 100),
            'recommendations': recommendations,
            'confidence_level': float(np.max(disease_risk) * 100)
        }

    except Exception as e:
        print(f"Error in health analysis: {e}")
        return {
            'prediction_type': 'basic',
            'risk_score': 50,
            'recommendations': "Unable to generate detailed recommendations. Please consult a healthcare provider.",
            'confidence_level': 60
        }

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            user = get_user_by_email(email)

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            print(f"Error during login: {e}")
            flash('An error occurred. Please try again.', 'danger')
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get logged-in user's info
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()

        # Get user's health data
        cursor.execute("""
            SELECT 
                *,
                COALESCE(improvement_percentage, 0) as improvement_percentage,
                COALESCE(last_updated, created_at) as last_updated
            FROM health_data 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (session['user_id'],))
        
        health_data = cursor.fetchone()

        # Get user's analysis history
        cursor.execute("""
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as date,
                   prediction_type as summary,
                   recommendations as findings
            FROM health_predictions 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 5
        """, (session['user_id'],))
        
        analysis_history = cursor.fetchall()

        # Get health history for the past 6 months
        cursor.execute("""
            SELECT 
                DATE_FORMAT(created_at, '%Y-%m-%d') as date,
                improvement_percentage,
                bmi,
                physical_activity_level,
                stress_level,
                sleep_hours
            FROM health_data 
            WHERE user_id = %s 
            AND created_at >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            ORDER BY created_at ASC
        """, (session['user_id'],))
        
        health_history = cursor.fetchall()

        if not health_data:
            flash("Please complete your health profile", "warning")
            return redirect(url_for('complete_profile'))

        # Calculate predictions for this specific user
        decline_predictions = calculate_health_decline(health_data)
        improvement_predictions = [max(75, min(100, x + 15)) for x in decline_predictions]

        # Define the get_action_items function to be used in template
        def get_action_items(health_data):
            action_items = []
            
            # Check BMI
            if health_data.get('bmi', 0) > 25:
                action_items.append({
                    'icon': 'bx-run',
                    'title': 'Increase Physical Activity',
                    'description': 'Aim for 30 minutes of moderate exercise daily'
                })
            
            # Check blood pressure
            bp = health_data.get('blood_pressure', '120/80')
            systolic, diastolic = map(int, bp.split('/'))
            if systolic > 120 or diastolic > 80:
                action_items.append({
                    'icon': 'bx-heart',
                    'title': 'Monitor Blood Pressure',
                    'description': 'Track your blood pressure daily and reduce sodium intake'
                })
            
            # Check sleep
            if health_data.get('sleep_hours', 0) < 7:
                action_items.append({
                    'icon': 'bx-moon',
                    'title': 'Improve Sleep Habits',
                    'description': 'Aim for 7-9 hours of sleep per night'
                })
            
            # Add general wellness recommendations
            action_items.append({
                'icon': 'bx-water',
                'title': 'Stay Hydrated',
                'description': 'Drink at least 8 glasses of water daily'
            })
            
            return action_items

        return render_template('dashboard.html',
                             user=user,
                             health_data=health_data,
                             get_action_items=get_action_items,  # Pass the function to the template
                             analysis_history=analysis_history,
                             health_decline_predictions=decline_predictions,
                             health_predictions=improvement_predictions,
                             health_history=health_history)

    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return redirect(url_for('login'))

    finally:
        cursor.close()
        conn.close()

# Train AI Model for Disease Prediction
def train_model():
    try:
        data = pd.read_csv("medical_data.csv")
        X = data[['age', 'bmi', 'blood_pressure']]
        y = data['disease_risk']
        model = RandomForestClassifier()
        model.fit(X, y)
        joblib.dump(model, "health_model.pkl")
    except Exception as e:
        print(f"Error training model: {e}")

# Predict Risk Function
def predict_risk(user_data):
    try:
        model = joblib.load("health_model.pkl")
        return model.predict([user_data])
    except Exception as e:
        print(f"Prediction Error: {e}")
        return ["Error"]

# Predict Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        bmi = float(request.form['bmi'])
        blood_pressure = float(request.form['bp'])
        result = predict_risk([age, bmi, blood_pressure])
        return {"risk": result.tolist()}
    except Exception as e:
        return {"error": str(e)}

# Extract Text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text("text") for page in doc)
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def analyze_medical_report(file_path):
    """Analyze the uploaded medical report PDF"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Simple analysis (you can make this more sophisticated)
            findings = []
            
            # Look for common medical terms and values
            if re.search(r'blood\s+pressure\s*[:=]?\s*(\d{2,3}/\d{2,3})', text, re.I):
                findings.append("Blood Pressure Information Found")
            
            if re.search(r'glucose\s*[:=]?\s*(\d{2,3})', text, re.I):
                findings.append("Glucose Levels Found")
            
            if re.search(r'cholesterol\s*[:=]?\s*(\d{2,3})', text, re.I):
                findings.append("Cholesterol Information Found")

            return {
                'success': True,
                'analysis_summary': "Medical report analyzed successfully",
                'key_findings': ", ".join(findings) or "No specific medical data identified"
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    try:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extract and analyze PDF content
            text = extract_text(filepath)
            analysis_result = simple_pdf_analysis(text)
            
            if analysis_result['success']:
                # Save to database
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO medical_reports 
                    (user_id, file_name, file_path, analysis_results, key_findings) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    session['user_id'],
                    filename,
                    filepath,
                    json.dumps(analysis_result['metrics']),
                    json.dumps(analysis_result['findings'])
                ))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'filename': filename,
                    'metrics': analysis_result['metrics'],
                    'findings': analysis_result['findings']
                })
            
            return jsonify({'success': False, 'error': 'Could not analyze PDF'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        # Clean up uploaded file after saving to database
        if os.path.exists(filepath):
            os.remove(filepath)

def extract_pdf_text(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text

def simple_pdf_analysis(text):
    """Simple PDF analysis without NLTK"""
    metrics = {}
    findings = []
    
    # Common patterns to look for
    patterns = {
        'blood_pressure': r'(?:BP|blood pressure)[:\s]+(\d{2,3}\/\d{2,3})',
        'heart_rate': r'(?:HR|heart rate|pulse)[:\s]+(\d{2,3})',
        'glucose': r'(?:glucose|blood sugar)[:\s]+(\d{2,3})',
        'cholesterol': r'(?:cholesterol)[:\s]+(\d{2,3})',
        'bmi': r'(?:BMI)[:\s]+(\d{1,2}\.?\d{0,2})',
        'weight': r'(?:weight)[:\s]+(\d{2,3}\.?\d{0,2})',
        'height': r'(?:height)[:\s]+(\d{1,3})'
    }
    
    # Extract metrics
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics[key] = match.group(1)
            findings.append(f"Found {key}: {match.group(1)}")
    
    return {
        'success': True,
        'metrics': metrics,
        'findings': findings
    }

def analyze_medical_report(text):
    # Add your medical report analysis logic here
    # This is a simple example - you should enhance this based on your needs
    analysis = {
        'summary': "Medical report analysis completed successfully.",
        'key_findings': []
    }

    # Example analysis (you should make this more sophisticated)
    if 'blood pressure' in text.lower():
        analysis['key_findings'].append("Blood pressure information found")
    if 'cholesterol' in text.lower():
        analysis['key_findings'].append("Cholesterol levels detected")
    if 'glucose' in text.lower():
        analysis['key_findings'].append("Glucose measurements present")

    analysis['key_findings'] = ", ".join(analysis['key_findings']) if analysis['key_findings'] else "No specific findings detected"
    
    return analysis

@app.route('/get_risk_score')
def get_risk_score():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try:
        # Get user's health data
        health_data = get_user_health_data(session['user_id'])
        
        if not health_data:
            return jsonify({
                'success': False,
                'error': 'No health data found',
                'message': 'Please complete your health profile'
            })

        # Calculate risk assessment
        risk_assessment = calculate_risk_factors(health_data)
        
        # Calculate disease risks
        disease_risks = [
            {'name': 'Cardiovascular Disease', 'risk': calculate_disease_risk(health_data, 'cardiovascular')},
            {'name': 'Diabetes', 'risk': calculate_disease_risk(health_data, 'diabetes')},
            {'name': 'Hypertension', 'risk': calculate_disease_risk(health_data, 'hypertension')}
        ]

        # Generate recommendations
        recommendations = generate_health_recommendations(health_data)

        return jsonify({
            'success': True,
            'risk_score': risk_assessment['score'],
            'status': risk_assessment['status'],
            'risk_factors': risk_assessment['risk_factors'],
            'disease_risks': disease_risks,
            'recommendations': recommendations,
            'trend': 'Stable'  # You can implement trend calculation based on historical data
        })

    except Exception as e:
        print(f"Error in get_risk_score: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error calculating risk score'
        })

def calculate_disease_risk(health_data, disease_type):
    try:
        risk_score = 0
        if disease_type == 'cardiovascular':
            # Calculate cardiovascular risk
            if health_data.get('cholesterol', 0) > 200:
                risk_score += 30
            if health_data.get('blood_pressure'):
                sys, dia = map(int, health_data['blood_pressure'].split('/'))
                if sys > 140 or dia > 90:
                    risk_score += 30
            if health_data.get('smoking_status'):
                risk_score += 20
                
        elif disease_type == 'diabetes':
            # Calculate diabetes risk
            if health_data.get('glucose_level', 0) > 100:
                risk_score += 40
            if health_data.get('bmi', 0) > 25:
                risk_score += 20
                
        elif disease_type == 'hypertension':
            # Calculate hypertension risk
            if health_data.get('blood_pressure'):
                sys, dia = map(int, health_data['blood_pressure'].split('/'))
                if sys > 130 or dia > 80:
                    risk_score += 40
            if health_data.get('stress_level', 0) > 7:
                risk_score += 20

        return min(risk_score, 100)  # Cap at 100%
        
    except Exception as e:
        print(f"Error calculating {disease_type} risk: {str(e)}")
        return 0

def generate_health_recommendations(health_data):
    recommendations = []
    
    try:
        # BMI-based recommendations
        if health_data.get('bmi'):
            bmi = float(health_data['bmi'])
            if bmi >= 25:
                recommendations.append("Maintain a balanced diet and regular exercise routine")
                recommendations.append("Consider consulting with a nutritionist")
            
        # Blood pressure recommendations
        if health_data.get('blood_pressure'):
            sys, dia = map(int, health_data['blood_pressure'].split('/'))
            if sys >= 130 or dia >= 80:
                recommendations.append("Monitor blood pressure regularly")
                recommendations.append("Reduce sodium intake")
                
        # Lifestyle recommendations
        if health_data.get('smoking_status'):
            recommendations.append("Consider smoking cessation programs")
            
        if health_data.get('physical_activity', 0) < 3:
            recommendations.append("Increase physical activity to at least 150 minutes per week")
            
        if health_data.get('sleep_hours', 0) < 7:
            recommendations.append("Improve sleep habits to get 7-9 hours of sleep")
            
        if health_data.get('stress_level', 0) > 7:
            recommendations.append("Practice stress management techniques")
            
        # Add some general recommendations if list is too short
        if len(recommendations) < 3:
            recommendations.extend([
                "Maintain regular health check-ups",
                "Stay hydrated with adequate water intake",
                "Practice mindful eating habits"
            ])
            
        return recommendations[:5]  # Return top 5 recommendations
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return ["Complete your health profile for personalized recommendations"]

@app.route('/complete_profile', methods=['GET', 'POST'])
def complete_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Get the current health data from form
            health_data = {
                'height': float(request.form['height']),
                'weight': float(request.form['weight']),
                'blood_pressure': request.form['blood_pressure'],
                'heart_rate': int(request.form['heart_rate']),
                'glucose_level': float(request.form['glucose_level']),
                'cholesterol': float(request.form['cholesterol']),
                'smoking_status': int(request.form['smoking_status']),
                'alcohol_consumption': int(request.form['alcohol_consumption']),
                'physical_activity': float(request.form['physical_activity']),
                'sleep_hours': float(request.form['sleep_hours']),
                'stress_level': int(request.form['stress_level']),
                'existing_conditions': request.form['existing_conditions'],
                'family_history': request.form['family_history'],
                'medications': request.form['medications']
            }

            # Calculate BMI
            height_m = health_data['height'] / 100  # Convert cm to m
            health_data['bmi'] = round(health_data['weight'] / (height_m * height_m), 2)

            # Get previous health data
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT * FROM health_data 
                WHERE user_id = %s 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (session['user_id'],))
            
            previous_data = cursor.fetchone()

            # Calculate improvement percentage
            improvement_percentage = 0
            
            if previous_data:
                # BMI improvement (if previously overweight/obese)
                if previous_data['bmi'] > 25 and health_data['bmi'] < previous_data['bmi']:
                    improvement_percentage += 20
                
                # Physical activity improvement
                if health_data['physical_activity'] > previous_data['physical_activity_level']:
                    improvement_percentage += 15
                
                # Sleep improvement
                if health_data['sleep_hours'] >= 7 and previous_data['sleep_hours'] < 7:
                    improvement_percentage += 10
                
                # Stress level improvement
                if health_data['stress_level'] < previous_data['stress_level']:
                    improvement_percentage += 10
                
                # Blood pressure improvement
                if previous_data['blood_pressure'] and health_data['blood_pressure']:
                    prev_sys, prev_dia = map(int, previous_data['blood_pressure'].split('/'))
                    curr_sys, curr_dia = map(int, health_data['blood_pressure'].split('/'))
                    if curr_sys < prev_sys and curr_dia < prev_dia:
                        improvement_percentage += 15
                
                # Cholesterol improvement
                if health_data['cholesterol'] < previous_data['cholesterol']:
                    improvement_percentage += 15
                
                # Glucose level improvement
                if health_data['glucose_level'] < previous_data['glucose_level']:
                    improvement_percentage += 15
            else:
                # For first-time entries, set a baseline improvement
                improvement_percentage = 50 if health_data['bmi'] < 25 else 30

            # Insert new health data with improvement percentage
            cursor.execute("""
                INSERT INTO health_data 
                (user_id, height, weight, bmi, blood_pressure, heart_rate, 
                glucose_level, cholesterol, smoking_status, alcohol_consumption,
                physical_activity_level, sleep_hours, stress_level,
                existing_conditions, family_history, medications, improvement_percentage)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                session['user_id'], health_data['height'], health_data['weight'],
                health_data['bmi'], health_data['blood_pressure'],
                health_data['heart_rate'], health_data['glucose_level'],
                health_data['cholesterol'], health_data['smoking_status'],
                health_data['alcohol_consumption'], health_data['physical_activity'],
                health_data['sleep_hours'], health_data['stress_level'],
                health_data['existing_conditions'], health_data['family_history'],
                health_data['medications'], improvement_percentage
            ))

            conn.commit()
            
            return jsonify({
                'success': True,
                'message': 'Health profile updated successfully!',
                'redirect': url_for('dashboard')
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()

    # GET request handling
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT * FROM health_data 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (session['user_id'],))
        
        health_data = cursor.fetchone()
        if not health_data:
            health_data = {
                'height': '',
                'weight': '',
                'blood_pressure': '',
                'heart_rate': '',
                'glucose_level': '',
                'cholesterol': '',
                'smoking_status': 0,
                'alcohol_consumption': 0,
                'physical_activity_level': '',
                'sleep_hours': '',
                'stress_level': 5,
                'existing_conditions': '',
                'family_history': '',
                'medications': ''
            }
        
        return render_template('complete_profile.html', health_data=health_data)
        
    except Exception as e:
        flash(f'Error loading profile: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        cursor.close()
        conn.close()

@app.route('/profile_settings')
def profile_settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Fetch user profile
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        return render_template('profile_settings.html', user=user)
    
    finally:
        cursor.close()
        conn.close()

@app.route('/health_records')
def health_records():
    if 'user_id' not in session:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Fetch user data
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        
        # Fetch medical records
        cursor.execute("""
            SELECT 
                mr.*,
                DATE_ADD(mr.upload_date, INTERVAL 7 DAY) >= CURRENT_TIMESTAMP as is_new
            FROM medical_reports mr
            WHERE mr.user_id = %s
            ORDER BY mr.upload_date DESC
        """, (session['user_id'],))
        records = cursor.fetchall()
        
        return render_template('health_records.html', 
                             user=user, 
                             records=records,
                             active_page='health_records')
    
    except Exception as e:
        flash(f'Error loading health records: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
    
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # First check if the record belongs to the logged-in user
        cursor.execute("""
            SELECT * FROM medical_reports 
            WHERE id = %s AND user_id = %s
        """, (record_id, session['user_id']))
        
        record = cursor.fetchone()
        
        if not record:
            return jsonify({'success': False, 'error': 'Record not found'})

        # Delete the physical file if it exists
        if record['file_path']:
            try:
                os.remove(record['file_path'])
            except OSError:
                # Log the error but continue with database deletion
                print(f"Error deleting file: {record['file_path']}")

        # Delete the record from database
        cursor.execute("""
            DELETE FROM medical_reports 
            WHERE id = %s AND user_id = %s
        """, (record_id, session['user_id']))
        
        conn.commit()
        
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    finally:
        cursor.close()
        conn.close()

@app.route('/download_record/<int:record_id>')
def download_record(record_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Check if the record belongs to the logged-in user
        cursor.execute("""
            SELECT * FROM medical_reports 
            WHERE id = %s AND user_id = %s
        """, (record_id, session['user_id']))
        
        record = cursor.fetchone()
        
        if not record or not record['file_path']:
            flash('Record not found or file missing', 'danger')
            return redirect(url_for('health_records'))

        # Check if file exists
        if not os.path.exists(record['file_path']):
            flash('File not found', 'danger')
            return redirect(url_for('health_records'))

        # Return the file for download
        return send_file(
            record['file_path'],
            as_attachment=True,
            download_name=record['file_name']
        )

    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('health_records'))

    finally:
        cursor.close()
        conn.close()

# Add this function to create/update tables
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anand$2005"
    )
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS health_db")
        cursor.execute("USE health_db")

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                age INT,
                gender VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create health_data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                height FLOAT,
                weight FLOAT,
                bmi FLOAT,
                blood_pressure VARCHAR(20),
                heart_rate INT,
                glucose_level FLOAT,
                cholesterol FLOAT,
                smoking_status INT,
                alcohol_consumption INT,
                physical_activity_level FLOAT,
                sleep_hours FLOAT,
                existing_conditions TEXT,
                family_history TEXT,
                medications TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Check if improvement_percentage column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_NAME = 'health_data' 
            AND COLUMN_NAME = 'improvement_percentage'
        """)
        has_improvement = cursor.fetchone()[0] > 0

        # Add improvement_percentage if it doesn't exist
        if not has_improvement:
            cursor.execute("""
                ALTER TABLE health_data 
                ADD COLUMN improvement_percentage FLOAT DEFAULT 0
            """)

        # Check if last_updated column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_NAME = 'health_data' 
            AND COLUMN_NAME = 'last_updated'
        """)
        has_last_updated = cursor.fetchone()[0] > 0

        # Add last_updated if it doesn't exist
        if not has_last_updated:
            cursor.execute("""
                ALTER TABLE health_data 
                ADD COLUMN last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """)

        # Create analysis_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                summary TEXT,
                findings TEXT,
                is_new BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        # Create medical_reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(255),
                analysis_results JSON,
                key_findings JSON,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        print("Database tables created/updated successfully")
        
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        conn.rollback()
        raise
        
    finally:
        cursor.close()
        conn.close()

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Get current user data for verification
        cursor.execute("SELECT email FROM users WHERE id = %s", (session['user_id'],))
        current_user = cursor.fetchone()

        # Check if email is being changed and if it's already taken
        new_email = request.form['email']
        if new_email != current_user['email']:
            cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", 
                         (new_email, session['user_id']))
            if cursor.fetchone():
                flash('Email address is already in use.', 'danger')
                return redirect(url_for('profile_settings'))

        # Start with basic info update
        update_query = """
            UPDATE users 
            SET name = %s, 
                email = %s,
                last_update = CURRENT_TIMESTAMP
        """
        params = [request.form['name'], new_email]

        # Check if password is being updated
        new_password = request.form.get('new_password')
        if new_password:
            if new_password != request.form.get('confirm_password'):
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('profile_settings'))
            
            # Add password to update query
            update_query += ", password = %s"
            params.append(generate_password_hash(new_password))

        # Complete the query
        update_query += " WHERE id = %s"
        params.append(session['user_id'])

        # Execute the update
        cursor.execute(update_query, tuple(params))
        conn.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile_settings'))

    except Exception as e:
        conn.rollback()
        flash(f'Error updating profile: {str(e)}', 'danger')
        return redirect(url_for('profile_settings'))

    finally:
        cursor.close()
        conn.close()

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        # Verify current password
        cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()

        if not check_password_hash(user['password'], current_password):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            })

        # Update password
        hashed_password = generate_password_hash(new_password)
        cursor.execute("""
            UPDATE users 
            SET password = %s,
                last_update = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (hashed_password, session['user_id']))

        conn.commit()
        return jsonify({
            'success': True,
            'message': 'Password updated successfully!'
        })

    except Exception as e:
        conn.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        })

    finally:
        cursor.close()
        conn.close()

@app.route('/update_profile_picture', methods=['POST'])
def update_profile_picture():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})

    if 'profile_picture' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})

    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    try:
        # Save file
        filename = secure_filename(f"profile_{session['user_id']}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Update database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET profile_picture = %s,
                last_update = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (filepath, session['user_id']))
        conn.commit()

        return jsonify({
            'success': True,
            'message': 'Profile picture updated!',
            'picture_url': url_for('static', filename=f'uploads/{filename}')
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def calculate_risk_score(health_data):
    risk_score = 0
    risk_factors = []
    recommendations = []
    
    try:
        # BMI Risk Assessment (15% of total risk)
        if health_data['bmi'] < 18.5:
            risk_score += 15
            risk_factors.append({
                'factor': "Underweight - BMI below healthy range",
                'severity': 'high',
                'value': f"BMI: {health_data['bmi']:.1f}"
            })
        elif health_data['bmi'] >= 25 and health_data['bmi'] < 30:
            risk_score += 10
            risk_factors.append({
                'factor': "Overweight - Increased health risk",
                'severity': 'moderate',
                'value': f"BMI: {health_data['bmi']:.1f}"
            })
        elif health_data['bmi'] >= 30:
            risk_score += 15
            risk_factors.append({
                'factor': "Obesity - High health risk",
                'severity': 'high',
                'value': f"BMI: {health_data['bmi']:.1f}"
            })

        # Blood Pressure Risk (20% of total risk)
        if health_data['blood_pressure']:
            systolic, diastolic = map(int, health_data['blood_pressure'].split('/'))
            if systolic >= 140 or diastolic >= 90:
                risk_score += 20
                risk_factors.append({
                    'factor': "High Blood Pressure",
                    'severity': 'high',
                    'value': f"{systolic}/{diastolic} mmHg"
                })
            elif systolic >= 130 or diastolic >= 85:
                risk_score += 15
                risk_factors.append({
                    'factor': "Pre-hypertension",
                    'severity': 'moderate',
                    'value': f"{systolic}/{diastolic} mmHg"
                })

        # Glucose Level Risk (20% of total risk)
        glucose = float(health_data['glucose_level'])
        if glucose > 126:
            risk_score += 20
            risk_factors.append({
                'factor': "High Blood Glucose - Diabetes Risk",
                'severity': 'high',
                'value': f"{glucose} mg/dL"
            })
        elif glucose > 100:
            risk_score += 15
            risk_factors.append({
                'factor': "Pre-diabetic Range",
                'severity': 'moderate',
                'value': f"{glucose} mg/dL"
            })

        # Cholesterol Risk (15% of total risk)
        cholesterol = float(health_data['cholesterol'])
        if cholesterol > 240:
            risk_score += 15
            risk_factors.append({
                'factor': "High Cholesterol",
                'severity': 'high',
                'value': f"{cholesterol} mg/dL"
            })
        elif cholesterol > 200:
            risk_score += 10
            risk_factors.append({
                'factor': "Borderline High Cholesterol",
                'severity': 'moderate',
                'value': f"{cholesterol} mg/dL"
            })

        # Lifestyle Risks (30% of total risk)
        lifestyle_score = 0
        
        # Smoking
        if health_data['smoking_status'] == 2:
            lifestyle_score += 10
            risk_factors.append({
                'factor': "Regular Smoker",
                'severity': 'high',
                'value': 'Daily smoker'
            })
        elif health_data['smoking_status'] == 1:
            lifestyle_score += 5
            risk_factors.append({
                'factor': "Occasional Smoker",
                'severity': 'moderate',
                'value': 'Occasional smoker'
            })

        # Physical Activity
        activity = float(health_data['physical_activity_level'])
        if activity < 2:
            lifestyle_score += 10
            risk_factors.append({
                'factor': "Insufficient Physical Activity",
                'severity': 'high',
                'value': f"{activity} hours/week"
            })
        elif activity < 4:
            lifestyle_score += 5
            risk_factors.append({
                'factor': "Low Physical Activity",
                'severity': 'moderate',
                'value': f"{activity} hours/week"
            })

        # Sleep
        sleep = float(health_data['sleep_hours'])
        if sleep < 6:
            lifestyle_score += 5
            risk_factors.append({
                'factor': "Sleep Deprivation",
                'severity': 'high',
                'value': f"{sleep} hours/day"
            })
        elif sleep > 9:
            lifestyle_score += 5
            risk_factors.append({
                'factor': "Excessive Sleep",
                'severity': 'moderate',
                'value': f"{sleep} hours/day"
            })

        # Add lifestyle score to total risk
        risk_score += lifestyle_score

        # Calculate final risk score (0-100)
        risk_score = min(100, risk_score)
        
        # Generate recommendations based on risk factors
        recommendations = generate_recommendations(risk_factors)

        return {
            'success': True,
            'risk_score': risk_score,
            'risk_level': get_risk_level(risk_score),
            'risk_factors': risk_factors,
            'recommendations': recommendations,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f"Error calculating risk score: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'risk_score': 50,
            'risk_level': 'Moderate',
            'risk_factors': [{'factor': 'Error calculating risks', 'severity': 'moderate', 'value': 'N/A'}],
            'recommendations': ['Please complete your health profile for accurate assessment']
        }

@app.route('/get_risk_assessment')
def get_risk_assessment():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'})

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM health_data 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (session['user_id'],))
        
        health_data = cursor.fetchone()
        
        if not health_data:
            return jsonify({
                'error': 'No health data available',
                'message': 'Please complete your health profile'
            })

        risk_assessment = calculate_risk_score(health_data)
        
        return jsonify({
            'success': True,
            'risk_score': risk_assessment['risk_score'],
            'risk_level': risk_assessment['risk_level'],
            'risk_factors': risk_assessment['risk_factors'],
            'recommendations': risk_assessment['recommendations']
        })

    except Exception as e:
        return jsonify({'error': str(e)})
    
    finally:
        cursor.close()
        conn.close()

def get_user_health_data(user_id):
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                height,
                weight,
                bmi,
                blood_pressure,
                heart_rate,
                glucose_level,
                cholesterol,
                smoking_status,
                alcohol_consumption,
                physical_activity_level as physical_activity,
                sleep_hours,
                stress_level,
                existing_conditions,
                family_history,
                medications,
                age
            FROM health_data 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (user_id,))
        
        data = cursor.fetchone()
        if data:
            # Convert numeric strings to float/int
            numeric_fields = {
                'float': ['height', 'weight', 'bmi', 'glucose_level', 'cholesterol', 'physical_activity'],
                'int': ['heart_rate', 'smoking_status', 'alcohol_consumption', 'stress_level', 'age']
            }
            
            for field in numeric_fields['float']:
                if data.get(field):
                    data[field] = float(data[field])
            
            for field in numeric_fields['int']:
                if data.get(field):
                    data[field] = int(data[field])

        return data

    except Exception as e:
        print(f"Error fetching health data: {str(e)}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/get_disease_predictions')
def get_disease_predictions():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'})
    
    try:
        health_data = get_user_health_data(session['user_id'])
        
        if not health_data:
            return jsonify({'success': False, 'error': 'No health data found'})
        
        # Calculate predictions based on health data
        predictions = []
        preventive_measures = []
        
        # BMI-based predictions
        bmi = health_data.get('bmi', 0)
        if bmi > 30:
            predictions.append({
                'condition': 'Type 2 Diabetes',
                'risk_level': 'High',
                'description': 'High BMI increases risk of developing diabetes.'
            })
            preventive_measures.append('Maintain a balanced diet and regular exercise routine')
        
        # Blood pressure based predictions
        bp = health_data.get('blood_pressure', '120/80')
        systolic, diastolic = map(int, bp.split('/'))
        if systolic > 140 or diastolic > 90:
            predictions.append({
                'condition': 'Cardiovascular Disease',
                'risk_level': 'High',
                'description': 'Elevated blood pressure increases risk of heart disease.'
            })
            preventive_measures.append('Monitor blood pressure regularly and reduce sodium intake')
        
        # Lifestyle-based predictions
        if int(health_data.get('smoking_status', 0)) > 0:
            predictions.append({
                'condition': 'Lung Disease',
                'risk_level': 'High',
                'description': 'Smoking significantly increases risk of respiratory issues.'
            })
            preventive_measures.append('Consider smoking cessation programs and avoid second-hand smoke')
        
        if float(health_data.get('physical_activity', 0)) < 2.5:
            predictions.append({
                'condition': 'Obesity',
                'risk_level': 'Moderate',
                'description': 'Low physical activity increases risk of weight gain.'
            })
            preventive_measures.append('Aim for at least 150 minutes of moderate exercise per week')
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'preventive_measures': preventive_measures
        })
        
    except Exception as e:
        print(f"Error generating predictions: {str(e)}")
        return jsonify({'success': False, 'error': 'Error generating predictions'})

@app.route('/health_history')
def health_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get the period from query parameters (default to 'month')
        period = request.args.get('period', 'month')
        period_clause = {
            'week': 'AND created_at >= DATE_SUB(NOW(), INTERVAL 1 WEEK)',
            'month': 'AND created_at >= DATE_SUB(NOW(), INTERVAL 1 MONTH)',
            'year': 'AND created_at >= DATE_SUB(NOW(), INTERVAL 1 YEAR)'
        }.get(period, '')
        
        # Fetch health history data with window functions to get previous values
        cursor.execute(f"""
            SELECT 
                created_at as date,
                bmi,
                blood_pressure,
                heart_rate,
                physical_activity_level,
                sleep_hours,
                stress_level,
                improvement_percentage as health_score,
                LAG(bmi) OVER (ORDER BY created_at) as previous_bmi,
                LAG(physical_activity_level) OVER (ORDER BY created_at) as previous_activity
            FROM health_data 
            WHERE user_id = %s {period_clause}
            ORDER BY created_at DESC
        """, (session['user_id'],))
        
        health_history = cursor.fetchall()
        
        # Prepare arrays for chart data and calculate changes
        dates = []
        health_scores = []
        bmi_data = []
        
        for entry in health_history:
            dates.append(entry['date'].strftime('%Y-%m-%d'))
            health_scores.append(entry['health_score'])
            bmi_data.append(entry['bmi'])
            
            # Calculate BMI change if previous BMI is available
            if entry['previous_bmi'] is not None:
                entry['bmi_change'] = entry['bmi'] - entry['previous_bmi']
            else:
                entry['bmi_change'] = None
        
        # Calculate overall progress based on health score improvement
        if health_history:
            initial_score = health_history[-1]['health_score']
            current_score = health_history[0]['health_score']
            overall_progress = round(((current_score - initial_score) / initial_score) * 100, 1) if initial_score else 0
        else:
            overall_progress = 0
        
        # Prepare additional metrics for comparison (example: BMI comparison)
        metrics_comparison = []
        if health_history and len(health_history) > 1:
            prev_bmi = health_history[-1]['bmi'] or 0
            curr_bmi = health_history[0]['bmi'] or 0
            if prev_bmi:
                bmi_change_percent = round(((curr_bmi - prev_bmi) / prev_bmi) * 100, 1)
            else:
                bmi_change_percent = 0
            metrics_comparison.append({
                'label': 'BMI',
                'current_value': f"{curr_bmi:.1f}",
                'change': bmi_change_percent,
                'improvement': curr_bmi < prev_bmi
            })
        else:
            metrics_comparison.append({
                'label': 'BMI',
                'current_value': 'N/A',
                'change': 0,
                'improvement': False
            })
        
        return render_template('health_history.html',
                               active_page='health_history',
                               health_history=health_history,
                               overall_progress=overall_progress,
                               dates=dates,
                               health_scores=health_scores,
                               bmi_data=bmi_data,
                               metrics_comparison=metrics_comparison)
    
    except Exception as e:
        flash(f'Error loading health history: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))
        
    finally:
        cursor.close()
        conn.close()

# Call this function when the app starts
if __name__ == '__main__':
    init_db()  # This will create the database and tables if they do not exist
    app.run(debug=True)
