import joblib

def calculate_risk_factors(health_data):
    if not health_data:
        return {
            'score': 50,
            'status': 'Moderate Risk',
            'risk_factors': ['Health profile incomplete']
        }
        
    risk_factors = []
    total_risk = 0
    
    try:
        # BMI Risk (25% weight in total risk)
        if health_data.get('bmi'):
            bmi = float(health_data['bmi'])
            if bmi < 18.5:
                risk_factors.append("Underweight (BMI: {:.1f})".format(bmi))
                total_risk += 20
            elif bmi >= 30:
                risk_factors.append("Obesity (BMI: {:.1f})".format(bmi))
                total_risk += 25
            elif bmi >= 25:
                risk_factors.append("Overweight (BMI: {:.1f})".format(bmi))
                total_risk += 15

        # Blood Pressure Risk (25% weight)
        if health_data.get('blood_pressure'):
            try:
                systolic, diastolic = map(int, str(health_data['blood_pressure']).split('/'))
                if systolic >= 140 or diastolic >= 90:
                    risk_factors.append(f"High Blood Pressure ({systolic}/{diastolic})")
                    total_risk += 25
                elif systolic >= 130 or diastolic >= 80:
                    risk_factors.append(f"Elevated Blood Pressure ({systolic}/{diastolic})")
                    total_risk += 15
            except:
                pass

        # Physical Activity Risk (20% weight)
        activity_level = float(health_data.get('physical_activity_level', 0))
        if activity_level < 2:
            risk_factors.append("Insufficient Physical Activity")
            total_risk += 20
        elif activity_level < 4:
            risk_factors.append("Moderate Physical Activity")
            total_risk += 10

        # Sleep Risk (15% weight)
        sleep_hours = float(health_data.get('sleep_hours', 7))
        if sleep_hours < 6:
            risk_factors.append("Severe Sleep Deficiency")
            total_risk += 15
        elif sleep_hours < 7:
            risk_factors.append("Mild Sleep Deficiency")
            total_risk += 10

        # Stress Level Risk (15% weight)
        stress_level = int(health_data.get('stress_level', 5))
        if stress_level >= 8:
            risk_factors.append("High Stress Level")
            total_risk += 15
        elif stress_level >= 6:
            risk_factors.append("Moderate Stress Level")
            total_risk += 10

        # Calculate final risk score (0-100)
        final_risk_score = min(100, total_risk)
        
        # Determine status based on risk score
        if final_risk_score < 30:
            status = "Low Risk"
        elif final_risk_score < 60:
            status = "Moderate Risk"
        else:
            status = "High Risk"

        return {
            'score': final_risk_score,
            'status': status,
            'risk_factors': risk_factors if risk_factors else ['No significant health risks detected'],
            'recommendations': generate_health_recommendations(health_data, {'risk_factors': risk_factors})
        }
        
    except Exception as e:
        print(f"Error calculating risk factors: {str(e)}")
        return {
            'score': 50,
            'status': 'Moderate Risk',
            'risk_factors': ['Error calculating health risks']
        }

def generate_health_recommendations(health_data, risk_assessment):
    recommendations = []
    
    for factor in risk_assessment['risk_factors']:
        factor_lower = factor.lower()
        
        if "bmi" in factor_lower:
            if "overweight" in factor_lower or "obesity" in factor_lower:
                recommendations.extend([
                    "• Create a calorie deficit through balanced diet and exercise",
                    "• Aim for 150-300 minutes of moderate exercise weekly",
                    "• Consider consulting a registered dietitian",
                    "• Monitor portion sizes and keep a food diary"
                ])
            elif "underweight" in factor_lower:
                recommendations.extend([
                    "• Increase caloric intake with nutrient-dense foods",
                    "• Add strength training to your exercise routine",
                    "• Consider protein supplementation",
                    "• Consult a nutritionist for a personalized meal plan"
                ])

        if "hypertension" in factor_lower or "blood pressure" in factor_lower:
            recommendations.extend([
                "• Monitor blood pressure daily",
                "• Reduce sodium intake to less than 2,300mg daily",
                "• Practice stress management techniques",
                "• Consider the DASH diet approach"
            ])

        if "heart rate" in factor_lower:
            recommendations.extend([
                "• Schedule a cardiac evaluation",
                "• Monitor heart rate regularly",
                "• Avoid excessive caffeine and stimulants",
                "• Practice relaxation techniques"
            ])

        if "blood sugar" in factor_lower or "diabetic" in factor_lower:
            recommendations.extend([
                "• Monitor blood glucose levels regularly",
                "• Follow a low-glycemic diet",
                "• Exercise regularly to improve insulin sensitivity",
                "• Consider consulting an endocrinologist"
            ])

        if "physical activity" in factor_lower:
            recommendations.extend([
                "• Start with short walks and gradually increase activity",
                "• Find physical activities you enjoy",
                "• Join group exercise classes for motivation",
                "• Set realistic fitness goals"
            ])

    # Remove duplicates while preserving order
    recommendations = list(dict.fromkeys(recommendations))

    # Add general recommendations if few specific ones exist
    if len(recommendations) < 3:
        recommendations.extend([
            "• Schedule regular check-ups with your healthcare provider",
            "• Maintain a balanced diet rich in fruits and vegetables",
            "• Aim for 7-9 hours of quality sleep each night",
            "• Stay hydrated with 8 glasses of water daily",
            "• Practice stress management techniques regularly"
        ])

    return recommendations[:8]  # Limit to top 8 recommendations

def generate_nutrition_plan(health_data, risk_assessment):
    nutrition_plan = {
        'daily_nutrients': {
            'protein': calculate_protein_needs(health_data),
            'carbs': calculate_carb_needs(health_data),
            'fats': calculate_fat_needs(health_data),
            'fiber': calculate_fiber_needs(health_data)
        },
        'recommended_foods': get_recommended_foods(health_data, risk_assessment),
        'meal_timing': generate_meal_schedule(health_data)
    }
    return nutrition_plan

def track_activity_progress(user_id):
    # Implement activity tracking logic
    activity_data = {
        'weekly_minutes': get_weekly_activity(user_id),
        'steps': get_daily_steps(user_id),
        'progress': calculate_activity_progress(user_id)
    }
    return activity_data

def generate_health_projections(health_data, following_recommendations=True):
    # Load projection model
    projection_model = joblib.load('models/health_projection_model.pkl')
    
    # Generate timeline projections
    projections = {
        'with_recommendations': calculate_projection(health_data, True),
        'without_changes': calculate_projection(health_data, False)
    }
    return projections

def calculate_projection(health_data, following_recommendations):
    # Define time points (in months)
    time_points = [0, 1, 3, 6, 12]
    projections = []
    
    for month in time_points:
        # Base projection on current health metrics
        projected_score = 100 - (month * 2)  # Initial health score decreases over time
        
        if following_recommendations:
            # Improve projection if following recommendations
            projected_score += month * 5  # Health improves with recommendations
        else:
            # Decrease more if not following recommendations
            projected_score -= month * 3  # Health declines faster without changes
        
        # Ensure score stays within 0-100 range
        projected_score = max(0, min(100, projected_score))
        projections.append(projected_score)
    
    return projections

def calculate_protein_needs(health_data):
    # Base protein: 0.8g per kg of body weight
    weight = float(health_data.get('weight', 70))
    return round(weight * 0.8, 1)

def calculate_carb_needs(health_data):
    # Carbs: 45-65% of total calories
    weight = float(health_data.get('weight', 70))
    activity_level = float(health_data.get('physical_activity', 1))
    daily_calories = weight * 30 * activity_level
    return round((daily_calories * 0.5) / 4)  # 4 calories per gram of carbs

def calculate_fat_needs(health_data):
    # Fats: 20-35% of total calories
    weight = float(health_data.get('weight', 70))
    daily_calories = weight * 30
    return round((daily_calories * 0.25) / 9)  # 9 calories per gram of fat

def calculate_fiber_needs(health_data):
    # General recommendation: 14g per 1000 calories
    weight = float(health_data.get('weight', 70))
    daily_calories = weight * 30
    return round((daily_calories / 1000) * 14)

def get_recommended_foods(health_data, risk_assessment):
    # Basic food recommendations based on health needs
    return [
        {'name': 'Lean Proteins', 'nutrients': 'Protein, Iron, B12'},
        {'name': 'Leafy Greens', 'nutrients': 'Fiber, Vitamins A, C, K'},
        {'name': 'Whole Grains', 'nutrients': 'Fiber, B Vitamins'},
        {'name': 'Fatty Fish', 'nutrients': 'Omega-3, Protein'},
        {'name': 'Berries', 'nutrients': 'Antioxidants, Fiber'}
    ]

def get_weekly_activity(user_id):
    # Placeholder: Replace with actual database query
    return [30, 45, 60, 30, 45, 60, 45]  # Minutes per day

def get_daily_steps(user_id):
    # Placeholder: Replace with actual step tracking data
    return 8000  # Example daily steps

def calculate_activity_progress(user_id):
    weekly_minutes = sum(get_weekly_activity(user_id))
    target_minutes = 150  # WHO recommends 150 minutes per week
    return min(100, int((weekly_minutes / target_minutes) * 100))

def generate_meal_schedule(health_data):
    # Basic meal timing recommendations
    return {
        'breakfast': '7:00 - 8:00 AM',
        'morning_snack': '10:00 - 10:30 AM',
        'lunch': '12:30 - 1:30 PM',
        'afternoon_snack': '3:30 - 4:00 PM',
        'dinner': '6:30 - 7:30 PM',
        'notes': 'Eat every 3-4 hours to maintain stable blood sugar levels'
    }

def calculate_health_decline(health_data):
    try:
        # Calculate base decline rate from risk factors
        base_decline = 0
        
        # Age factor
        age = int(health_data.get('age', 30))
        base_decline += (age / 100) * 5  # Higher decline rate with age
        
        # BMI factor
        if health_data.get('bmi'):
            bmi = float(health_data['bmi'])
            if bmi >= 30 or bmi < 18.5:
                base_decline += 8
            elif bmi >= 25:
                base_decline += 5
        
        # Blood pressure factor
        if health_data.get('blood_pressure'):
            try:
                systolic, diastolic = map(int, health_data['blood_pressure'].split('/'))
                if systolic >= 140 or diastolic >= 90:
                    base_decline += 10
                elif systolic >= 130 or diastolic >= 80:
                    base_decline += 7
            except:
                pass
        
        # Lifestyle factors
        if health_data.get('smoking_status'):
            base_decline += 12
        if health_data.get('alcohol_consumption', 0) > 2:
            base_decline += 8
        if health_data.get('physical_activity_level', 0) < 2:
            base_decline += 6
        
        # Calculate decline timeline
        timeline = []
        months = [0, 3, 6, 12, 24]  # Timeline points
        current_health = 100 - base_decline
        
        for month in months:
            # Progressive decline based on time and risk factors
            decline = base_decline * (1 + (month / 12) * 0.2)
            health_score = max(0, min(100, current_health - decline))
            timeline.append(round(health_score, 1))
        
        return timeline
        
    except Exception as e:
        print(f"Error calculating health decline: {str(e)}")
        return [100, 95, 90, 85, 80]  # Default decline pattern

def calculate_improvement_trajectory(health_data):
    """
    Calculate potential health improvement trajectory based on following recommendations
    Returns a list of predicted health scores over time
    """
    try:
        # Get the decline timeline as baseline
        decline_timeline = calculate_health_decline(health_data)
        
        # Calculate improvement factors
        improvement_potential = calculate_improvement_potential(health_data)
        
        # Generate improvement timeline
        improvement_timeline = []
        current_score = decline_timeline[0]  # Start from current health score
        
        for i, baseline_score in enumerate(decline_timeline):
            # Calculate improvement percentage based on time
            if i == 0:
                improvement_timeline.append(current_score)  # Current score stays the same
            else:
                # Progressive improvement calculation
                time_factor = min(1.0, i * 0.2)  # Max improvement factor of 1.0
                improvement = baseline_score + (improvement_potential * time_factor)
                
                # Ensure the score doesn't exceed 100
                improved_score = min(100, improvement)
                
                # Ensure the improvement is always better than decline
                improved_score = max(improved_score, baseline_score + 5)
                
                improvement_timeline.append(round(improved_score, 1))
        
        return improvement_timeline

    except Exception as e:
        print(f"Error calculating improvement trajectory: {str(e)}")
        return [70, 75, 80, 85, 90]  # Default improvement pattern

def calculate_improvement_potential(health_data):
    """
    Calculate the maximum potential improvement based on current health factors
    """
    base_improvement = 15  # Base improvement potential
    
    try:
        # BMI improvement potential
        if health_data.get('bmi'):
            bmi = float(health_data['bmi'])
            if bmi >= 30 or bmi < 18.5:
                base_improvement += 10
            elif bmi >= 25:
                base_improvement += 5

        # Blood pressure improvement potential
        if health_data.get('blood_pressure'):
            try:
                systolic, diastolic = map(int, health_data['blood_pressure'].split('/'))
                if systolic >= 140 or diastolic >= 90:
                    base_improvement += 8
                elif systolic >= 130 or diastolic >= 85:
                    base_improvement += 5
            except:
                pass

        # Lifestyle improvement potential
        if health_data.get('smoking_status'):
            base_improvement += 12
        if float(health_data.get('alcohol_consumption', 0)) > 2:
            base_improvement += 8
        if float(health_data.get('physical_activity_level', 0)) < 2:
            base_improvement += 10
        if float(health_data.get('sleep_hours', 7)) < 6:
            base_improvement += 5
        if float(health_data.get('stress_level', 5)) > 7:
            base_improvement += 5

        return base_improvement

    except Exception as e:
        print(f"Error calculating improvement potential: {str(e)}")
        return 15  # Default improvement potential