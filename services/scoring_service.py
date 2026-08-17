class ScoringService:
    """
    Calculates overall Student Career Readiness Score (0-100)
    broken down across 5 foundational employability dimensions.
    """

    @classmethod
    def calculate_readiness_score(cls, student_profile, top_recommendation=None):
        """
        Calculates career readiness score (0-100) and component breakdown.
        """
        skills = student_profile.get("skills", [])
        projects = student_profile.get("projects", [])
        certifications = student_profile.get("certifications", [])
        experience = student_profile.get("experience_level", "Beginner").lower()

        try:
            cgpa = float(student_profile.get("education", {}).get("cgpa", 0))
        except (ValueError, TypeError):
            cgpa = 0.0

        # 1. Technical Skills Pillar (Max 35 points)
        skill_count = len(skills)
        if skill_count >= 8:
            tech_score = 35
        elif skill_count >= 5:
            tech_score = 28
        elif skill_count >= 3:
            tech_score = 20
        elif skill_count >= 1:
            tech_score = 12
        else:
            tech_score = 0

        # 2. Academic Standard (CGPA) Pillar (Max 20 points)
        if cgpa >= 8.5:
            edu_score = 20
        elif cgpa >= 7.5:
            edu_score = 17
        elif cgpa >= 6.5:
            edu_score = 14
        elif cgpa >= 5.5:
            edu_score = 10
        elif cgpa > 0:
            edu_score = 6
        else:
            edu_score = 0

        # 3. Practical Projects Pillar (Max 20 points)
        proj_count = len(projects)
        if proj_count >= 3:
            proj_score = 20
        elif proj_count == 2:
            proj_score = 15
        elif proj_count == 1:
            proj_score = 10
        else:
            proj_score = 3

        # 4. Certifications Pillar (Max 15 points)
        cert_count = len(certifications)
        if cert_count >= 3:
            cert_score = 15
        elif cert_count == 2:
            cert_score = 12
        elif cert_count == 1:
            cert_score = 8
        else:
            cert_score = 2

        # 5. Experience Pillar (Max 10 points)
        if experience == "advanced":
            exp_score = 10
        elif experience == "intermediate":
            exp_score = 7
        else:
            exp_score = 4

        total_readiness = tech_score + edu_score + proj_score + cert_score + exp_score
        total_readiness = min(100, max(0, total_readiness))

        # Generate Actionable Summary Advice
        summary_text = cls._generate_feedback_summary(total_readiness, top_recommendation, skills)

        return {
            "total_score": total_readiness,
            "breakdown": {
                "technical_skills": {"score": tech_score, "max": 35},
                "education": {"score": edu_score, "max": 20},
                "projects": {"score": proj_score, "max": 20},
                "certifications": {"score": cert_score, "max": 15},
                "experience": {"score": exp_score, "max": 10}
            },
            "summary": summary_text
        }

    @classmethod
    def _generate_feedback_summary(cls, total_score, top_recommendation, skills):
        """Generates dynamic feedback commentary based on readiness score and missing skills."""
        if top_recommendation and top_recommendation.get("missing_skills"):
            missing_str = ", ".join(top_recommendation["missing_skills"][:3])
            role_title = top_recommendation["role_title"]
            if total_score >= 80:
                return f"Outstanding profile! You have a high career readiness score of {total_score}/100. To maximize your competitive edge for {role_title} roles, focus on mastering: {missing_str}."
            elif total_score >= 60:
                return f"Your profile is developing well with a readiness score of {total_score}/100. Strengthen your skills in {missing_str} to boost your matching percentage for {role_title}."
            else:
                return f"Your readiness score is currently {total_score}/100. Build foundational projects and learn target skills like {missing_str} to improve your readiness for software roles."
        else:
            if total_score >= 80:
                return f"Excellent profile with a readiness score of {total_score}/100! Keep expanding your practical project portfolio."
            else:
                return f"Your profile readiness is {total_score}/100. Add technical skills, complete hands-on projects, and gain certifications to increase your career score."
