from app.models.exercise import Exercise
from app.models.profile import UserProfile
from app.models.fitness_plan import FitnessPlan, PlanExercise
from app.ml.recommender import FitnessRecommender
from app import db

class RecommendationService:
    def __init__(self):
        self.recommender = FitnessRecommender()
    
    def get_recommendations(self, profile, duration_weeks=4, difficulty='beginner'):
        # Get exercise recommendations from ML model
        recommendations = self.recommender.recommend_exercises(
            profile=profile,
            difficulty=difficulty,
            limit=10
        )
        
        if not recommendations:
            return {'error': 'No exercises found for your profile'}
        
        # Convert exercises to dictionaries
        recommended_exercises = []
        for rec in recommendations:
            recommended_exercises.append({
                'exercise': rec['exercise'].to_dict(),  # Convert to dict!
                'match_score': rec['score']
            })
        
        # Create workout plan structure
        workout_plan = self._create_workout_plan(
            recommended_exercises,
            duration_weeks,
            difficulty,
            profile.fitness_goal
        )
        
        return {
            'recommended_exercises': recommended_exercises,
            'workout_plan': workout_plan
        }
    
    def _create_workout_plan(self, exercises, duration_weeks, difficulty, fitness_goal):
        # Create a weekly workout schedule
        weekly_schedule = []
        
        # Split exercises by category
        cardio = [ex for ex in exercises if ex['exercise']['category'] == 'cardio']
        strength = [ex for ex in exercises if ex['exercise']['category'] == 'strength']
        flexibility = [ex for ex in exercises if ex['exercise']['category'] == 'flexibility']
        
        # Create 5-day workout split
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for day in days:
            day_exercises = []
            
            if day in ['Monday', 'Wednesday', 'Friday']:
                # Strength training days
                day_exercises.extend(strength[:3] if strength else [])
                day_exercises.extend(flexibility[:1] if flexibility else [])
            else:
                # Cardio days
                day_exercises.extend(cardio[:2] if cardio else [])
                day_exercises.extend(flexibility[:1] if flexibility else [])
            
            weekly_schedule.append({
                'day': day,
                'exercises': day_exercises,
                'total_exercises': len(day_exercises),
                'estimated_duration_minutes': 45
            })
        
        # Rest days
        weekly_schedule.append({
            'day': 'Saturday',
            'exercises': flexibility[:2] if flexibility else [],
            'total_exercises': len(flexibility[:2]) if flexibility else 0,
            'estimated_duration_minutes': 30,
            'type': 'Active Recovery'
        })
        
        weekly_schedule.append({
            'day': 'Sunday',
            'exercises': [],
            'total_exercises': 0,
            'estimated_duration_minutes': 0,
            'type': 'Rest Day'
        })
        
        return {
            'duration_weeks': duration_weeks,
            'difficulty': difficulty,
            'goal': fitness_goal,
            'weekly_schedule': weekly_schedule,
            'total_workouts_per_week': 6
        }
    
    def save_plan(self, user_id, plan_data):
        # Create and save fitness plan to database
        plan = FitnessPlan(
            user_id=user_id,
            name=plan_data.get('name', 'My Fitness Plan'),
            description=plan_data.get('description'),
            duration_weeks=plan_data.get('duration_weeks', 4),
            difficulty=plan_data.get('difficulty', 'beginner'),
            goal=plan_data.get('goal')
        )
        
        db.session.add(plan)
        db.session.commit()
        
        # Add exercises to plan
        for exercise_data in plan_data.get('exercises', []):
            plan_exercise = PlanExercise(
                plan_id=plan.id,
                exercise_id=exercise_data['exercise_id'],
                day_of_week=exercise_data.get('day_of_week'),
                sets=exercise_data.get('sets', 3),
                reps=exercise_data.get('reps', 10),
                duration_minutes=exercise_data.get('duration_minutes', 5)
            )
            db.session.add(plan_exercise)
        
        db.session.commit()
        return plan
