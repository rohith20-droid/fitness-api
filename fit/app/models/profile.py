from app import db
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                       nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    fitness_goal = db.Column(db.String(50))
    activity_level = db.Column(db.String(20))
    health_conditions = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                         onupdate=datetime.utcnow)
    
    def calculate_bmi(self):
        if self.weight and self.height:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 2)
        return None
    
    def calculate_bmr(self):
        if not all([self.weight, self.height, self.age, self.gender]):
            return None
        
        # Mifflin-St Jeor Equation
        if self.gender.lower() == 'male':
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            bmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        
        return round(bmr, 2)
    
    def calculate_daily_calories(self):
        bmr = self.calculate_bmr()
        if not bmr or not self.activity_level:
            return None
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        daily_calories = bmr * multiplier
        
        # Adjust based on fitness goal
        if self.fitness_goal == 'weight_loss':
            daily_calories -= 500
        elif self.fitness_goal == 'muscle_gain':
            daily_calories += 300
        
        return round(daily_calories, 2)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'age': self.age,
            'gender': self.gender,
            'weight': self.weight,
            'height': self.height,
            'fitness_goal': self.fitness_goal,
            'activity_level': self.activity_level,
            'health_conditions': self.health_conditions,
            'bmi': self.calculate_bmi(),
            'bmr': self.calculate_bmr(),
            'daily_calories': self.calculate_daily_calories(),
            'updated_at': self.updated_at.isoformat()
        }
