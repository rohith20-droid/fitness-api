from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.fitness_plan import WorkoutSession
from datetime import datetime, date

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/', methods=['POST'])
@jwt_required()
def log_workout():
    current_user_id = int(get_jwt_identity())  # Convert to int
    data = request.get_json()
    
    workout_date = datetime.strptime(data.get('date', str(date.today())), '%Y-%m-%d').date()
    
    session = WorkoutSession(
        user_id=current_user_id,
        plan_id=data.get('plan_id'),
        date=workout_date,
        duration=data.get('duration'),
        calories_burned=data.get('calories_burned'),
        completed=data.get('completed', True),
        notes=data.get('notes')
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify({
        'message': 'Workout logged successfully',
        'session_id': session.id,
        'session': session.to_dict()
    }), 201

@progress_bp.route('/', methods=['GET'])
@jwt_required()
def get_workout_history():
    current_user_id = int(get_jwt_identity())  # Convert to int
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = WorkoutSession.query.filter_by(user_id=current_user_id)
    
    if start_date:
        query = query.filter(WorkoutSession.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(WorkoutSession.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    sessions = query.order_by(WorkoutSession.date.desc()).all()
    
    return jsonify({
        'total_sessions': len(sessions),
        'workout_sessions': [s.to_dict() for s in sessions]
    }), 200

@progress_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_statistics():
    current_user_id = int(get_jwt_identity())  # Convert to int
    
    sessions = WorkoutSession.query.filter_by(user_id=current_user_id).all()
    
    if not sessions:
        return jsonify({
            'total_sessions': 0,
            'total_duration': 0,
            'total_calories': 0,
            'avg_duration': 0,
            'avg_calories': 0
        }), 200
    
    total_sessions = len(sessions)
    total_duration = sum(s.duration or 0 for s in sessions)
    total_calories = sum(s.calories_burned or 0 for s in sessions)
    
    return jsonify({
        'total_sessions': total_sessions,
        'total_duration': total_duration,
        'total_calories': round(total_calories, 2),
        'avg_duration': round(total_duration / total_sessions, 2),
        'avg_calories': round(total_calories / total_sessions, 2)
    }), 200

@progress_bp.route('/<int:session_id>', methods=['GET'])
@jwt_required()
def get_workout_session(session_id):
    current_user_id = int(get_jwt_identity())  # Convert to int
    
    session = WorkoutSession.query.filter_by(
        id=session_id, 
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    return jsonify(session.to_dict()), 200

@progress_bp.route('/<int:session_id>', methods=['PUT'])
@jwt_required()
def update_workout_session(session_id):
    current_user_id = int(get_jwt_identity())  # Convert to int
    data = request.get_json()
    
    session = WorkoutSession.query.filter_by(
        id=session_id, 
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    # Update fields
    if 'duration' in data:
        session.duration = data['duration']
    if 'calories_burned' in data:
        session.calories_burned = data['calories_burned']
    if 'completed' in data:
        session.completed = data['completed']
    if 'notes' in data:
        session.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'message': 'Workout session updated successfully',
        'session': session.to_dict()
    }), 200

@progress_bp.route('/<int:session_id>', methods=['DELETE'])
@jwt_required()
def delete_workout_session(session_id):
    current_user_id = int(get_jwt_identity())  # Convert to int
    
    session = WorkoutSession.query.filter_by(
        id=session_id, 
        user_id=current_user_id
    ).first()
    
    if not session:
        return jsonify({'error': 'Workout session not found'}), 404
    
    db.session.delete(session)
    db.session.commit()
    
    return jsonify({'message': 'Workout session deleted successfully'}), 200
