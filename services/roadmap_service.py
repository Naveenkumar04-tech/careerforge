class RoadmapService:
    """
    Generates a personalized, dynamic 6-month career learning roadmap
    tailored specifically to bridge the student's identified missing skills.
    """

    @classmethod
    def generate_roadmap(cls, top_recommendation, user_skills=None):
        """
        Builds a custom 6-month step-by-step roadmap array.
        """
        role_title = top_recommendation.get("role_title", "Software Developer") if top_recommendation else "Software Developer"
        missing_skills = top_recommendation.get("missing_skills", []) if top_recommendation else []
        
        # Priority queue of target skills to learn
        target_skills = [s for s in missing_skills]
        
        # General tech fallback topics if missing skills list is short
        fallback_topics = ["Git & GitHub", "RESTful API Integration", "SQL & Database Design", "Unit Testing", "System Architecture", "Cloud Fundamentals"]
        for topic in fallback_topics:
            if topic not in target_skills:
                target_skills.append(topic)

        # Build Month 1-6 Milestones dynamically
        m1_skill = target_skills[0] if len(target_skills) > 0 else "Programming Fundamentals"
        m2_skill = target_skills[1] if len(target_skills) > 1 else "Database Systems & SQL"
        m3_skill = target_skills[2] if len(target_skills) > 2 else "Git, GitHub & Clean Code"
        m4_skill = target_skills[3] if len(target_skills) > 3 else "API Design & Backend Frameworks"

        months = [
            {
                "month": "Month 1",
                "phase": "Core Fundamentals",
                "title": f"Master {m1_skill}",
                "description": f"Focus on core concepts, syntax, data structures, and foundational exercises in {m1_skill}.",
                "deliverable": f"Complete 5 coding challenges and basic scripts using {m1_skill}.",
                "icon": "bi-journal-code"
            },
            {
                "month": "Month 2",
                "phase": "Database & Data Layer",
                "title": f"Master {m2_skill}",
                "description": f"Learn database schema design, queries, and data management techniques using {m2_skill}.",
                "deliverable": f"Design and build a database schema for a sample web application.",
                "icon": "bi-database"
            },
            {
                "month": "Month 3",
                "phase": "Version Control & Tooling",
                "title": f"Master {m3_skill}",
                "description": f"Set up clean Git workflow, branch management, collaborative pull requests, and automated scripts using {m3_skill}.",
                "deliverable": f"Create and push 3 repositories with professional README files to GitHub.",
                "icon": "bi-git"
            },
            {
                "month": "Month 4",
                "phase": "Advanced Domain Tech",
                "title": f"Master {m4_skill}",
                "description": f"Deep dive into production architectural patterns, backend/frontend integration, and {m4_skill}.",
                "deliverable": f"Build a modular REST API or backend microservice using best practices.",
                "icon": "bi-diagram-3"
            },
            {
                "month": "Month 5",
                "phase": "Portfolio Project Build",
                "title": f"Build 2 Major Projects for {role_title}",
                "description": f"Integrate all learned skills into building two showcase portfolio projects tailored for {role_title} roles.",
                "deliverable": f"Deploy 2 full-stack / backend projects online with live demonstration links.",
                "icon": "bi-cpu"
            },
            {
                "month": "Month 6",
                "phase": "Interview & Career Readiness",
                "title": "Resume Prep, GitHub Showcase & Mock Interviews",
                "description": "Finalize your technical resume, optimize your GitHub profile, practice DSA problem solving, and conduct mock technical interviews.",
                "deliverable": "Apply to entry-level software positions with a polished resume and active portfolio.",
                "icon": "bi-trophy"
            }
        ]

        return {
            "target_role": role_title,
            "total_months": 6,
            "milestones": months
        }
