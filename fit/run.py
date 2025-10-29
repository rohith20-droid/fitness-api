import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.profile import UserProfile
from app.models.exercise import Exercise
from app.models.fitness_plan import FitnessPlan

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'UserProfile': UserProfile,
        'Exercise': Exercise,
        'FitnessPlan': FitnessPlan
    }

if __name__ == '__main__':
    print("🚀 Starting Personalized Fitness Plan Recommendation API...")
    print("📍 Server running at: http://localhost:5000")
    print("📚 API Documentation available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)