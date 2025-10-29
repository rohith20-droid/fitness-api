from app import db
from datetime import datetime

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    equipment = db.Column(db.String(100))
    description = db.Column(db.Text)
    calories_per_minute = db.Column(db.Float)
    target_muscles = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ADD THIS METHOD
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'difficulty': self.difficulty,
            'equipment': self.equipment,
            'description': self.description,
            'calories_per_minute': self.calories_per_minute,
            'target_muscles': self.target_muscles,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Exercise {self.name}>'
