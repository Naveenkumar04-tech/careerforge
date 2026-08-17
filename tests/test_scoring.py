import pytest
from services.scoring_service import ScoringService

def test_calculate_readiness_score_high_profile():
    student_profile = {
        "skills": ["Python", "Flask", "SQL", "Git", "MongoDB", "C++", "HTML", "CSS", "JavaScript"],
        "education": {"cgpa": 9.2, "degree": "B.Tech", "branch": "Computer Science"},
        "projects": [
            {"title": "Project 1", "description": "Desc 1"},
            {"title": "Project 2", "description": "Desc 2"},
            {"title": "Project 3", "description": "Desc 3"}
        ],
        "certifications": ["AWS Certified Cloud Practitioner", "Python Essentials"],
        "experience_level": "Intermediate"
    }

    result = ScoringService.calculate_readiness_score(student_profile)
    
    assert "total_score" in result
    assert result["total_score"] >= 80
    assert result["breakdown"]["technical_skills"]["score"] == 35
    assert result["breakdown"]["education"]["score"] == 20
    assert result["breakdown"]["projects"]["score"] == 20
    assert "summary" in result

def test_calculate_readiness_score_beginner_profile():
    student_profile = {
        "skills": ["C++"],
        "education": {"cgpa": 6.2, "degree": "B.Tech", "branch": "Computer Science"},
        "projects": [],
        "certifications": [],
        "experience_level": "Beginner"
    }

    result = ScoringService.calculate_readiness_score(student_profile)
    
    assert "total_score" in result
    assert result["total_score"] < 50
    assert result["breakdown"]["technical_skills"]["score"] == 12
    assert result["breakdown"]["projects"]["score"] == 3
