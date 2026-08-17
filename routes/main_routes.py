from flask import Blueprint, render_template, jsonify, current_app
from models.student_model import StudentModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Renders home landing page."""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """Renders about and project overview page."""
    return render_template('about.html')

@main_bp.route('/health')
def health_check():
    """
    Healthcheck endpoint returns JSON status of application server and database connectivity.
    """
    student_model = StudentModel(
        mongodb_uri=current_app.config.get('MONGODB_URI'),
        db_name=current_app.config.get('DB_NAME')
    )
    is_db_ok = student_model.is_db_connected()

    return jsonify({
        "status": "healthy",
        "service": "Student Career & Job Recommendation System",
        "database": "connected" if is_db_ok else "fallback_mode",
        "db_connected": is_db_ok
    }), 200
