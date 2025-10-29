from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.fitness import fitness_bp
    from app.routes.progress import progress_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(fitness_bp, url_prefix='/api/fitness')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    
    # Create database tables - ADD THIS BACK!
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Personalized Fitness Plan Recommendation API',
            'version': '1.0',
            'endpoints': {
                'auth': '/api/auth',
                'user': '/api/user',
                'fitness': '/api/fitness',
                'progress': '/api/progress'
            }
        })
    
    return app
