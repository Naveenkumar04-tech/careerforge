import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from models.student_model import StudentModel
from services.recommendation_service import RecommendationService
from services.scoring_service import ScoringService
from services.roadmap_service import RoadmapService

student_bp = Blueprint('student', __name__)

def get_student_model():
    """Instantiates StudentModel using active application configuration."""
    return StudentModel(
        mongodb_uri=current_app.config.get('MONGODB_URI'),
        db_name=current_app.config.get('DB_NAME')
    )

@student_bp.route('/profile', methods=['GET'])
def profile_form():
    """Renders student profile form (Create or Edit mode if student_id parameter is passed)."""
    student_id = request.args.get('id')
    student_data = None
    if student_id:
        model = get_student_model()
        student_data = model.get_student(student_id)
    return render_template('profile.html', student=student_data)

@student_bp.route('/analyze', methods=['POST'])
def analyze_profile():
    """
    Parses submitted profile form data, validates fields, calculates career recommendations,
    readiness score, and roadmap, saves data to database, and redirects to student dashboard.
    """
    try:
        # Form Data Parsing
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        degree = request.form.get('degree', '').strip()
        branch = request.form.get('branch', '').strip()
        cgpa_raw = request.form.get('cgpa', '').strip()
        grad_year_raw = request.form.get('graduation_year', '').strip()

        raw_skills = request.form.get('skills', '').strip()
        raw_certs = request.form.get('certifications', '').strip()
        raw_interests = request.form.getlist('interests')
        experience_level = request.form.get('experience_level', 'Beginner').strip()
        preferred_career = request.form.get('preferred_career', '').strip()

        project_titles = request.form.getlist('project_title')
        project_descs = request.form.getlist('project_desc')

        # Validation Checks
        errors = []

        if not name:
            errors.append("Student Name is required.")
        
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("A valid Email address is required.")

        try:
            cgpa = float(cgpa_raw)
            if cgpa < 0.0 or cgpa > 10.0:
                errors.append("CGPA must be a value between 0.0 and 10.0.")
        except ValueError:
            errors.append("CGPA must be a valid numeric number (e.g. 8.5).")

        try:
            grad_year = int(grad_year_raw) if grad_year_raw else 2026
        except ValueError:
            grad_year = 2026

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('profile.html', form_data=request.form)

        # Parse skills and certifications into list
        skills = [s.strip() for s in re.split(r'[,;\n]+', raw_skills) if s.strip()]
        certifications = [c.strip() for c in re.split(r'[,;\n]+', raw_certs) if c.strip()]
        
        # Build projects list
        projects = []
        for title, desc in zip(project_titles, project_descs):
            if title.strip():
                projects.append({
                    "title": title.strip(),
                    "description": desc.strip()
                })

        student_profile = {
            "name": name,
            "email": email,
            "education": {
                "degree": degree,
                "branch": branch,
                "cgpa": cgpa,
                "graduation_year": grad_year
            },
            "skills": skills,
            "certifications": certifications,
            "interests": raw_interests,
            "experience_level": experience_level,
            "projects": projects,
            "preferred_career": preferred_career
        }

        # Perform Scoring & Recommendations
        recommendations = RecommendationService.evaluate_profile(student_profile)
        top_match = recommendations[0] if recommendations else None
        readiness = ScoringService.calculate_readiness_score(student_profile, top_match)
        roadmap = RoadmapService.generate_roadmap(top_match, skills)

        # Attach computed analysis to profile
        student_profile["analysis"] = {
            "recommendations": recommendations,
            "readiness": readiness,
            "roadmap": roadmap
        }

        # Save or Update Database
        model = get_student_model()
        existing_id = request.form.get('student_id')
        
        if existing_id:
            updated = model.update_student(existing_id, student_profile)
            student_id = existing_id if updated else model.save_student(student_profile)
        else:
            student_id = model.save_student(student_profile)

        flash("Profile analyzed and saved successfully!", "success")
        return redirect(url_for('student.dashboard', student_id=student_id))

    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "danger")
        return redirect(url_for('student.profile_form'))

@student_bp.route('/dashboard/<student_id>')
def dashboard(student_id):
    """Displays dashboard overview for a specific student."""
    model = get_student_model()
    student = model.get_student(student_id)

    if not student:
        flash("Student profile not found.", "warning")
        return redirect(url_for('student.profile_form'))

    analysis = student.get('analysis', {})
    recommendations = analysis.get('recommendations', [])
    readiness = analysis.get('readiness', {})
    top_3_matches = recommendations[:3] if recommendations else []
    top_match = recommendations[0] if recommendations else {}

    return render_template(
        'dashboard.html',
        student=student,
        student_id=student_id,
        readiness=readiness,
        top_matches=top_3_matches,
        top_match=top_match
    )

@student_bp.route('/results/<student_id>')
def results(student_id):
    """Displays full detailed career recommendation results for a student."""
    model = get_student_model()
    student = model.get_student(student_id)

    if not student:
        flash("Student profile not found.", "warning")
        return redirect(url_for('student.profile_form'))

    analysis = student.get('analysis', {})
    recommendations = analysis.get('recommendations', [])
    readiness = analysis.get('readiness', {})

    return render_template(
        'results.html',
        student=student,
        student_id=student_id,
        recommendations=recommendations,
        readiness=readiness
    )

@student_bp.route('/roadmap/<student_id>')
def roadmap(student_id):
    """Displays personalized 6-month career roadmap view."""
    model = get_student_model()
    student = model.get_student(student_id)

    if not student:
        flash("Student profile not found.", "warning")
        return redirect(url_for('student.profile_form'))

    analysis = student.get('analysis', {})
    roadmap_data = analysis.get('roadmap', {})
    recommendations = analysis.get('recommendations', [])
    top_match = recommendations[0] if recommendations else {}

    return render_template(
        'roadmap.html',
        student=student,
        student_id=student_id,
        roadmap=roadmap_data,
        top_match=top_match
    )

# REST API Endpoints
@student_bp.route('/api/student/<student_id>', methods=['GET'])
def api_get_student(student_id):
    """API endpoint returning student profile JSON data."""
    model = get_student_model()
    student = model.get_student(student_id)
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    return jsonify(student), 200
