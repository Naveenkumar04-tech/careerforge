class RecommendationService:
    """
    Rule-based recommendation engine evaluating 12 tech job roles
    against a student's technical skills, education, projects, certifications, and interests.
    """

    CAREER_ROLES = [
        {
            "id": "software_developer",
            "title": "Software Developer",
            "description": "Designs, builds, and maintains core desktop and application software using clean object-oriented code.",
            "required_skills": ["C++", "Python", "Java", "C", "Data Structures", "Algorithms", "Git", "SQL"],
            "preferred_skills": ["Design Patterns", "Unit Testing", "REST API", "Linux"],
            "min_recommended_cgpa": 7.0,
            "relevant_interests": ["Software Development", "Backend Development", "General Programming"]
        },
        {
            "id": "backend_developer",
            "title": "Backend Developer",
            "description": "Constructs robust server-side APIs, database management systems, and backend infrastructure.",
            "required_skills": ["Python", "Java", "Node.js", "Flask", "Django", "SQL", "MongoDB", "REST API", "Git"],
            "preferred_skills": ["PostgreSQL", "Docker", "Redis", "Microservices", "Authentication"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["Backend Development", "Web Development", "Database Development"]
        },
        {
            "id": "frontend_developer",
            "title": "Frontend Developer",
            "description": "Creates beautiful, responsive, and intuitive web user interfaces for modern web applications.",
            "required_skills": ["HTML", "CSS", "JavaScript", "Bootstrap", "Tailwind", "Git"],
            "preferred_skills": ["React", "Vue", "TypeScript", "Responsive Design", "Web Accessibility"],
            "min_recommended_cgpa": 6.0,
            "relevant_interests": ["Web Development", "UI/UX Design", "Frontend Development"]
        },
        {
            "id": "fullstack_developer",
            "title": "Full Stack Developer",
            "description": "Builds end-to-end web applications handling client-side UI, server logic, and database layer.",
            "required_skills": ["HTML", "CSS", "JavaScript", "Python", "Flask", "Node.js", "SQL", "MongoDB", "REST API", "Git"],
            "preferred_skills": ["React", "Docker", "AWS", "TypeScript", "GraphQL"],
            "min_recommended_cgpa": 7.0,
            "relevant_interests": ["Web Development", "Backend Development", "Full Stack Development"]
        },
        {
            "id": "data_analyst",
            "title": "Data Analyst",
            "description": "Transforms raw operational data into meaningful business insights using statistical tools and visualization.",
            "required_skills": ["Python", "SQL", "Excel", "Pandas", "NumPy", "Data Visualization"],
            "preferred_skills": ["Tableau", "Power BI", "Statistics", "R", "Metabase"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["Data Science", "Data Analysis", "Database Development"]
        },
        {
            "id": "data_scientist",
            "title": "Data Scientist",
            "description": "Applies statistical modeling, predictive analytics, and machine learning to solve complex data challenges.",
            "required_skills": ["Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Statistics", "Data Visualization"],
            "preferred_skills": ["R", "TensorFlow", "PyTorch", "BigQuery", "Spark"],
            "min_recommended_cgpa": 7.5,
            "relevant_interests": ["Data Science", "AI/ML", "Statistics"]
        },
        {
            "id": "ml_engineer",
            "title": "Machine Learning Engineer",
            "description": "Builds and deploys scalable production machine learning and deep learning models.",
            "required_skills": ["Python", "Scikit-Learn", "TensorFlow", "PyTorch", "Math", "Statistics", "Git"],
            "preferred_skills": ["MLOps", "Docker", "CUDA", "NLP", "Computer Vision"],
            "min_recommended_cgpa": 7.5,
            "relevant_interests": ["AI/ML", "Data Science", "Backend Development"]
        },
        {
            "id": "cloud_engineer",
            "title": "Cloud Engineer",
            "description": "Architects, provisions, and manages secure cloud infrastructure on public cloud platforms.",
            "required_skills": ["AWS", "Azure", "GCP", "Linux", "Networking", "Python", "Git"],
            "preferred_skills": ["Terraform", "Docker", "Kubernetes", "Shell Scripting", "Security"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["Cloud Computing", "DevOps", "Cybersecurity"]
        },
        {
            "id": "devops_engineer",
            "title": "DevOps Engineer",
            "description": "Automates CI/CD pipelines, containerization, and infrastructure deployment for high availability.",
            "required_skills": ["Linux", "Git", "Docker", "CI/CD", "Python", "Bash", "Shell Scripting"],
            "preferred_skills": ["Kubernetes", "Terraform", "Ansible", "AWS", "Monitoring"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["DevOps", "Cloud Computing", "Backend Development"]
        },
        {
            "id": "database_developer",
            "title": "Database Developer",
            "description": "Designs optimized database schemas, writes complex SQL queries, and tunes database performance.",
            "required_skills": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Database Design", "Performance Tuning"],
            "preferred_skills": ["PL/SQL", "Redis", "NoSQL", "ETL", "Data Modeling"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["Database Development", "Backend Development", "Data Science"]
        },
        {
            "id": "cybersecurity_analyst",
            "title": "Cybersecurity Analyst",
            "description": "Protects networks, applications, and systems against security vulnerabilities and cyber threats.",
            "required_skills": ["Networking", "Linux", "Security", "Python", "Cryptography", "Ethical Hacking"],
            "preferred_skills": ["Wireshark", "Metasploit", "SOC", "Firewalls", "SIEM"],
            "min_recommended_cgpa": 6.5,
            "relevant_interests": ["Cybersecurity", "Networking", "Cloud Computing"]
        },
        {
            "id": "qa_engineer",
            "title": "QA / Test Engineer",
            "description": "Ensures high software quality through automated test frameworks, regression testing, and bug verification.",
            "required_skills": ["Python", "Java", "Selenium", "Unit Testing", "Test Automation", "Git", "SQL"],
            "preferred_skills": ["Pytest", "Postman", "API Testing", "Jira", "CI/CD"],
            "min_recommended_cgpa": 6.0,
            "relevant_interests": ["Quality Assurance", "Testing", "Web Development"]
        }
    ]

    # Algorithm Component Weights
    WEIGHT_SKILLS = 0.40
    WEIGHT_EDUCATION = 0.15
    WEIGHT_PROJECTS = 0.15
    WEIGHT_CERTIFICATIONS = 0.10
    WEIGHT_INTERESTS = 0.10
    WEIGHT_EXPERIENCE = 0.10

    @classmethod
    def evaluate_profile(cls, student_profile):
        """
        Evaluates a student's profile against all 12 job roles.
        Returns a sorted list of recommendations from highest to lowest matching score.
        """
        user_skills = [s.strip().lower() for s in student_profile.get("skills", []) if s.strip()]
        user_certs = [c.strip().lower() for c in student_profile.get("certifications", []) if c.strip()]
        user_interests = [i.strip().lower() for i in student_profile.get("interests", []) if i.strip()]
        user_projects = student_profile.get("projects", [])
        
        # Education parsing
        education = student_profile.get("education", {})
        try:
            cgpa = float(education.get("cgpa", 0))
        except (ValueError, TypeError):
            cgpa = 0.0

        exp_level = student_profile.get("experience_level", "Beginner").lower()
        preferred_role = student_profile.get("preferred_career", "").strip().lower()

        results = []

        for role in cls.CAREER_ROLES:
            req_skills = [s.lower() for s in role["required_skills"]]
            pref_skills = [s.lower() for s in role["preferred_skills"]]
            all_role_skills = req_skills + pref_skills

            # 1. Skill Score Calculation
            matched_req = [s for s in role["required_skills"] if s.lower() in user_skills]
            matched_pref = [s for s in role["preferred_skills"] if s.lower() in user_skills]
            
            req_score = len(matched_req) / len(req_skills) if req_skills else 1.0
            pref_score = len(matched_pref) / len(pref_skills) if pref_skills else 0.5
            
            # 70% weight for required skills, 30% for preferred skills
            skill_score = (req_score * 0.7) + (pref_score * 0.3)

            # 2. Education Score Calculation
            min_cgpa = role["min_recommended_cgpa"]
            if cgpa >= min_cgpa:
                edu_score = 1.0
            elif cgpa >= (min_cgpa - 1.0):
                edu_score = 0.75
            elif cgpa > 0:
                edu_score = 0.50
            else:
                edu_score = 0.30

            # 3. Projects Score Calculation
            proj_count = len(user_projects)
            if proj_count >= 3:
                proj_score = 1.0
            elif proj_count == 2:
                proj_score = 0.85
            elif proj_count == 1:
                proj_score = 0.65
            else:
                proj_score = 0.30

            # 4. Certifications Score Calculation
            cert_matched = 0
            for cert in user_certs:
                if any(k in cert for k in [role["title"].lower()] + [s.lower() for s in role["required_skills"]]):
                    cert_matched += 1
            cert_score = min(1.0, 0.5 + (cert_matched * 0.25)) if user_certs else 0.40

            # 5. Interests Score Calculation
            interest_matched = False
            for interest in user_interests:
                if any(ri.lower() in interest or interest in ri.lower() for ri in role["relevant_interests"]):
                    interest_matched = True
                    break
            interest_score = 1.0 if interest_matched else 0.40

            # 6. Experience Score Calculation
            if exp_level == "advanced":
                exp_score = 1.0
            elif exp_level == "intermediate":
                exp_score = 0.85
            else:
                exp_score = 0.60

            # Total Weighted Score
            total_score = (
                (cls.WEIGHT_SKILLS * skill_score) +
                (cls.WEIGHT_EDUCATION * edu_score) +
                (cls.WEIGHT_PROJECTS * proj_score) +
                (cls.WEIGHT_CERTIFICATIONS * cert_score) +
                (cls.WEIGHT_INTERESTS * interest_score) +
                (cls.WEIGHT_EXPERIENCE * exp_score)
            ) * 100.0

            # Bonus for explicit preferred career selection
            if preferred_role and preferred_role in role["title"].lower():
                total_score = min(100.0, total_score + 5.0)

            match_percentage = round(total_score, 1)

            # Matched & Missing skills lists (preserving original casing)
            all_matched = matched_req + matched_pref
            all_missing = [s for s in role["required_skills"] if s not in matched_req]

            results.append({
                "role_id": role["id"],
                "role_title": role["title"],
                "description": role["description"],
                "match_percentage": match_percentage,
                "matched_skills": all_matched,
                "missing_skills": all_missing,
                "recommended_skills": all_missing[:4],
                "min_cgpa": role["min_recommended_cgpa"]
            })

        # Sort recommendations descending by match percentage
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return results
