import pytest
from services.recommendation_service import RecommendationService
from services.roadmap_service import RoadmapService

def test_evaluate_profile_backend_developer():
    student_profile = {
        "skills": ["Python", "Flask", "SQL", "MongoDB", "REST API", "Git"],
        "education": {"cgpa": 8.0, "degree": "B.Tech", "branch": "Computer Science"},
        "certifications": ["Python Certificate"],
        "interests": ["Backend Development"],
        "experience_level": "Intermediate",
        "projects": [
            {"title": "API Build", "description": "Flask REST API"},
            {"title": "Database App", "description": "PostgreSQL backend"}
        ],
        "preferred_career": "Backend Developer"
    }

    results = RecommendationService.evaluate_profile(student_profile)

    assert len(results) == 12
    top_match = results[0]
    assert top_match["role_title"] == "Backend Developer"
    assert top_match["match_percentage"] >= 70.0
    assert "Python" in top_match["matched_skills"]

def test_generate_roadmap():
    top_recommendation = {
        "role_title": "Backend Developer",
        "missing_skills": ["Docker", "Redis", "Microservices"]
    }
    
    roadmap = RoadmapService.generate_roadmap(top_recommendation)

    assert roadmap["target_role"] == "Backend Developer"
    assert roadmap["total_months"] == 6
    assert len(roadmap["milestones"]) == 6
    assert "Docker" in roadmap["milestones"][0]["title"] or "Docker" in roadmap["milestones"][1]["title"] or "Docker" in roadmap["milestones"][2]["title"]
