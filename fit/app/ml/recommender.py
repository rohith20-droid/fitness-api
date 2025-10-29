import numpy as np
from app.models.exercise import Exercise

class FitnessRecommender:
    def __init__(self):
        pass
    
    def recommend_exercises(self, profile, difficulty='beginner', limit=10):
        all_exercises = Exercise.query.all()
        
        if not all_exercises:
            return []
        
        filtered_exercises = [
            ex for ex in all_exercises 
            if ex.difficulty == difficulty
        ]
        
        recommendations = []
        
        for exercise in filtered_exercises:
            score = self._calculate_exercise_score(profile, exercise)
            recommendations.append({
                'exercise': exercise,
                'score': score
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:limit]
    
    def _calculate_exercise_score(self, profile, exercise):
        score = 1.0
        
        if profile.fitness_goal == 'weight_loss':
            if exercise.category == 'cardio':
                score += 0.5
        elif profile.fitness_goal == 'muscle_gain':
            if exercise.category == 'strength':
                score += 0.5
        elif profile.fitness_goal == 'endurance':
            if exercise.category in ['cardio', 'flexibility']:
                score += 0.3
        
        bmi = profile.calculate_bmi()
        if bmi and bmi > 30:
            if exercise.equipment in ['none', 'mat', 'resistance_band']:
                score += 0.2
        
        return score
