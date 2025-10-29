from app import db
from datetime import datetime, date

class FitnessPlan(db.Model):
    __tablename__ = 'fitness_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))
    goal = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exercises = db.relationship('PlanExercise', backref='plan', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('WorkoutSession', backref='plan', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'duration_weeks': self.duration_weeks,
            'difficulty': self.difficulty,
            'goal': self.goal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'exercises': [ex.to_dict() for ex in self.exercises]
        }
    
    def __repr__(self):
        return f'<FitnessPlan {self.name}>'


class PlanExercise(db.Model):
    __tablename__ = 'plan_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('fitness_plans.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    day_of_week = db.Column(db.String(20))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_minutes = db.Column(db.Integer)
    order = db.Column(db.Integer)
    
    # FIX: Use different backref name to avoid conflict
    exercise = db.relationship('Exercise', backref='exercise_plans', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'plan_id': self.plan_id,
            'exercise_id': self.exercise_id,
            'exercise': self.exercise.to_dict() if self.exercise else None,
            'day_of_week': self.day_of_week,
            'sets': self.sets,
            'reps': self.reps,
            'duration_minutes': self.duration_minutes,
            'order': self.order
        }
    
    def __repr__(self):
        return f'<PlanExercise {self.id}>'


class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('fitness_plans.id'))
    date = db.Column(db.Date, default=date.today)
    duration = db.Column(db.Integer)  # in minutes
    calories_burned = db.Column(db.Float)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'date': self.date.isoformat() if self.date else None,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'completed': self.completed,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<WorkoutSession {self.id} - {self.date}>'
