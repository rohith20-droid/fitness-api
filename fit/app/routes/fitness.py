from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.profile import UserProfile
from app.models.fitness_plan import FitnessPlan
from app.services.recommendation_service import RecommendationService

fitness_bp = Blueprint('fitness', __name__)

@fitness_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    current_user_id = int(get_jwt_identity())  # Convert to int
    data = request.get_json()
    
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    
    if not profile or not profile.fitness_goal:
        return jsonify({
            'error': 'Please complete your profile first'
        }), 400
    
    rec_service = RecommendationService()
    recommendations = rec_service.get_recommendations(
        profile=profile,
        duration_weeks=data.get('duration_weeks', 4),
        difficulty=data.get('difficulty', 'beginner')
    )
    
    return jsonify(recommendations), 200

@fitness_bp.route('/plans', methods=['GET'])
@jwt_required()
def get_plans():
    current_user_id = int(get_jwt_identity())  # Convert to int
    plans = FitnessPlan.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'plans': [plan.to_dict() for plan in plans]
    }), 200

@fitness_bp.route('/plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_plan(plan_id):
    current_user_id = int(get_jwt_identity())  # Convert to int
    plan = FitnessPlan.query.filter_by(
        id=plan_id, 
        user_id=current_user_id
    ).first()
    
    if not plan:
        return jsonify({'error': 'Plan not found'}), 404
    
    return jsonify(plan.to_dict()), 200

@fitness_bp.route('/plans', methods=['POST'])
@jwt_required()
def save_plan():
    current_user_id = int(get_jwt_identity())  # Convert to int
    data = request.get_json()
    
    rec_service = RecommendationService()
    plan = rec_service.save_plan(current_user_id, data)
    
    return jsonify({
        'message': 'Plan saved successfully',
        'plan': plan.to_dict()
    }), 201

@fitness_bp.route('/calculate/bmi', methods=['POST'])
def calculate_bmi():
    data = request.get_json()
    
    if not all(k in data for k in ('weight', 'height')):
        return jsonify({'error': 'Missing weight or height'}), 400
    
    weight = float(data['weight'])
    height = float(data['height']) / 100
    bmi = round(weight / (height ** 2), 2)
    
    if bmi < 18.5:
        category = 'Underweight'
    elif bmi < 25:
        category = 'Normal'
    elif bmi < 30:
        category = 'Overweight'
    else:
        category = 'Obese'
    
    return jsonify({
        'bmi': bmi,
        'category': category
    }), 200

@fitness_bp.route('/calculate/bmr', methods=['POST'])
def calculate_bmr():
    data = request.get_json()
    
    required = ['weight', 'height', 'age', 'gender']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    gender = data['gender'].lower()
    
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    return jsonify({'bmr': round(bmr, 2)}), 200

@fitness_bp.route('/calculate/calories', methods=['POST'])
def calculate_calories():
    data = request.get_json()
    
    required = ['weight', 'height', 'age', 'gender', 'activity_level', 'fitness_goal']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Calculate BMR
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    gender = data['gender'].lower()
    
    if gender == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = activity_multipliers.get(data['activity_level'].lower(), 1.2)
    daily_calories = bmr * multiplier
    
    # Adjust for fitness goal
    fitness_goal = data['fitness_goal'].lower()
    if fitness_goal == 'weight_loss':
        daily_calories -= 500
    elif fitness_goal == 'muscle_gain':
        daily_calories += 300
    
    # Calculate macros (rough estimate)
    protein = round((daily_calories * 0.30) / 4, 2)  # 30% from protein (4 cal/g)
    carbs = round((daily_calories * 0.40) / 4, 2)    # 40% from carbs (4 cal/g)
    fats = round((daily_calories * 0.30) / 9, 2)     # 30% from fats (9 cal/g)
    
    return jsonify({
        'daily_calories': round(daily_calories, 2),
        'bmr': round(bmr, 2),
        'macros': {
            'protein_grams': protein,
            'carbs_grams': carbs,
            'fats_grams': fats
        }
    }), 200
