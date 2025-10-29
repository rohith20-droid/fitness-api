import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.exercise import Exercise

app = create_app()

exercises_data = [
    # Cardio - Beginner
    {"name": "Walking", "category": "cardio", "difficulty": "beginner", "equipment": "none", 
     "description": "Low-impact cardio exercise", "calories_per_minute": 3.5, "target_muscles": "legs, core"},
    {"name": "Jogging", "category": "cardio", "difficulty": "beginner", "equipment": "none", 
     "description": "Moderate-intensity running", "calories_per_minute": 8.0, "target_muscles": "legs, cardiovascular"},
    {"name": "Cycling (Light)", "category": "cardio", "difficulty": "beginner", "equipment": "bicycle", 
     "description": "Low-intensity cycling", "calories_per_minute": 5.0, "target_muscles": "legs, glutes"},
    
    # Cardio - Intermediate
    {"name": "Running", "category": "cardio", "difficulty": "intermediate", "equipment": "none", 
     "description": "High-intensity running", "calories_per_minute": 11.5, "target_muscles": "legs, cardiovascular"},
    {"name": "Jump Rope", "category": "cardio", "difficulty": "intermediate", "equipment": "jump_rope", 
     "description": "High-intensity skipping", "calories_per_minute": 12.0, "target_muscles": "full body, cardiovascular"},
    {"name": "Burpees", "category": "cardio", "difficulty": "intermediate", "equipment": "none", 
     "description": "Full-body explosive exercise", "calories_per_minute": 10.0, "target_muscles": "full body"},
    
    # Strength - Beginner
    {"name": "Push-ups", "category": "strength", "difficulty": "beginner", "equipment": "none", 
     "description": "Upper body strength exercise", "calories_per_minute": 7.0, "target_muscles": "chest, triceps, shoulders"},
    {"name": "Bodyweight Squats", "category": "strength", "difficulty": "beginner", "equipment": "none", 
     "description": "Lower body strength exercise", "calories_per_minute": 5.5, "target_muscles": "quadriceps, glutes, hamstrings"},
    {"name": "Plank", "category": "strength", "difficulty": "beginner", "equipment": "mat", 
     "description": "Core stability exercise", "calories_per_minute": 4.0, "target_muscles": "core, shoulders"},
    {"name": "Lunges", "category": "strength", "difficulty": "beginner", "equipment": "none", 
     "description": "Single-leg strength exercise", "calories_per_minute": 6.0, "target_muscles": "quadriceps, glutes"},
    
    # Strength - Intermediate
    {"name": "Dumbbell Bench Press", "category": "strength", "difficulty": "intermediate", "equipment": "dumbbells", 
     "description": "Chest building exercise", "calories_per_minute": 6.5, "target_muscles": "chest, triceps, shoulders"},
    {"name": "Barbell Squats", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", 
     "description": "Compound leg exercise", "calories_per_minute": 8.0, "target_muscles": "quadriceps, glutes, core"},
    {"name": "Deadlifts", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", 
     "description": "Full-body compound movement", "calories_per_minute": 8.5, "target_muscles": "back, legs, core"},
    {"name": "Pull-ups", "category": "strength", "difficulty": "intermediate", "equipment": "pull_up_bar", 
     "description": "Upper body pulling exercise", "calories_per_minute": 9.0, "target_muscles": "back, biceps"},
    {"name": "Dumbbell Shoulder Press", "category": "strength", "difficulty": "intermediate", "equipment": "dumbbells", 
     "description": "Overhead shoulder exercise", "calories_per_minute": 6.0, "target_muscles": "shoulders, triceps"},
    {"name": "Bent Over Rows", "category": "strength", "difficulty": "intermediate", "equipment": "barbell", 
     "description": "Back strengthening exercise", "calories_per_minute": 7.0, "target_muscles": "back, biceps"},
    
    # Flexibility - Beginner
    {"name": "Yoga (Basic)", "category": "flexibility", "difficulty": "beginner", "equipment": "mat", 
     "description": "Stretching and flexibility", "calories_per_minute": 3.0, "target_muscles": "full body"},
    {"name": "Static Stretching", "category": "flexibility", "difficulty": "beginner", "equipment": "mat", 
     "description": "Basic flexibility exercises", "calories_per_minute": 2.5, "target_muscles": "full body"},
]

if __name__ == '__main__':
    with app.app_context():
        print("=" * 60)
        print("🌱 Seeding exercise data...")
        print("=" * 60)
        
        # DELETE ALL EXISTING EXERCISES FIRST
        print("🗑️  Deleting existing exercises...")
        Exercise.query.delete()
        db.session.commit()
        print("✅ Cleared exercise table!")
        
        # ADD NEW EXERCISES
        print("➕ Adding new exercises...")
        for exercise_data in exercises_data:
            exercise = Exercise(**exercise_data)
            db.session.add(exercise)
        
        db.session.commit()
        
        total = Exercise.query.count()
        print(f"✅ Successfully added {len(exercises_data)} exercises!")
        print(f"📊 Total exercises in database: {total}")
        
        if total > 0:
            print("\n📋 Exercise List:")
            for i, ex in enumerate(Exercise.query.all(), 1):
                print(f"  {i}. {ex.name} ({ex.difficulty} - {ex.category})")
        
        print("=" * 60)
        print("🎉 Database seeding complete!")
        print("=" * 60)
