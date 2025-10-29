from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.profile import UserProfile

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = int(get_jwt_identity())  # Convert to int
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    
    return jsonify({
        'user': user.to_dict(),
        'profile': profile.to_dict() if profile else None
    }), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = int(get_jwt_identity())  # Convert to int
    data = request.get_json()
    
    profile = UserProfile.query.filter_by(user_id=current_user_id).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user_id)
        db.session.add(profile)
    
    # Update fields
    if 'age' in data:
        profile.age = data['age']
    if 'gender' in data:
        profile.gender = data['gender']
    if 'weight' in data:
        profile.weight = data['weight']
    if 'height' in data:
        profile.height = data['height']
    if 'fitness_goal' in data:
        profile.fitness_goal = data['fitness_goal']
    if 'activity_level' in data:
        profile.activity_level = data['activity_level']
    if 'health_conditions' in data:
        profile.health_conditions = data['health_conditions']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'profile': profile.to_dict()
    }), 200

@user_bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    current_user_id = int(get_jwt_identity())  # Convert to int
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Account deleted successfully'}), 200
