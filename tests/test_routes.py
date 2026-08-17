import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Find Your Best Career Path" in response.data

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert "database" in json_data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"System Architecture" in response.data

def test_profile_page(client):
    response = client.get('/profile')
    assert response.status_code == 200
    assert b"Student Profile Assessment" in response.data

def test_analyze_and_dashboard_flow(client):
    payload = {
        "name": "Test Student",
        "email": "test@student.com",
        "degree": "B.Tech",
        "branch": "CSE",
        "cgpa": "8.5",
        "graduation_year": "2026",
        "skills": "Python, Flask, SQL, Git, HTML, CSS",
        "certifications": "Python Certified",
        "interests": ["Web Development", "Backend Development"],
        "experience_level": "Intermediate",
        "preferred_career": "Backend Developer",
        "project_title": ["Portfolio API"],
        "project_desc": ["Built using Flask and SQL"]
    }

    # Submit profile analysis form
    response = client.post('/analyze', data=payload, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, Test Student!" in response.data
    assert b"Career Readiness Score" in response.data

def test_invalid_cgpa_validation(client):
    payload = {
        "name": "Invalid Student",
        "email": "invalid@student.com",
        "degree": "B.Tech",
        "branch": "CSE",
        "cgpa": "15.0",  # Invalid CGPA > 10.0
        "skills": "Python",
        "experience_level": "Beginner"
    }

    response = client.post('/analyze', data=payload)
    assert response.status_code == 200
    assert b"CGPA must be a value between 0.0 and 10.0" in response.data
