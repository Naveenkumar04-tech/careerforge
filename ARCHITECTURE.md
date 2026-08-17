# Architecture & Technical Design Document

## 🏗️ System Architecture Overview

The **Student Career & Job Recommendation System** follows a modular Model-View-Controller (MVC) architecture with a dedicated **Service Layer** for domain logic (Scoring and Recommendations).

```
+-----------------------------------------------------------------------+
|                            USER BROWSER                               |
|          HTML5 + CSS3 (Bootstrap 5) + Vanilla JS (Fetch API)          |
+-----------------------------------+-----------------------------------+
                                    | HTTP Requests / JSON responses
                                    v
+-----------------------------------------------------------------------+
|                           FLASK BACKEND                               |
|                                                                       |
|   +-------------------+    +--------------------+                     |
|   |  Routes Layer     |--->|  Service Layer     |                     |
|   | (main, student)   |    | (Scoring, Recommend|                     |
|   +---------+---------+    +---------+----------+                     |
|             |                        |                                |
|             v                        |                                |
|   +-------------------+              |                                |
|   |  Jinja2 Templates |              |                                |
|   +-------------------+              v                                |
|                            +--------------------+                     |
|                            |   Model / Data     |                     |
|                            |   (Student DB)     |                     |
|                            +---------+----------+                     |
+--------------------------------------+--------------------------------+
                                       | PyMongo Client
                                       v
+-----------------------------------------------------------------------+
|                           MONGODB DATABASE                            |
|                  (Collection: `students` in `career_db`)              |
+-----------------------------------------------------------------------+
```

---

## 🗄️ Database Schema (`students` collection)

```json
{
  "_id": "ObjectId(...)",
  "name": "Alex Vance",
  "email": "alex@example.com",
  "education": {
    "degree": "B.Tech",
    "branch": "Computer Science & Engineering",
    "cgpa": 8.5,
    "graduation_year": 2026
  },
  "skills": ["Python", "Flask", "JavaScript", "HTML", "CSS", "SQL"],
  "certifications": ["AWS Certified Cloud Practitioner", "Python Essentials"],
  "interests": ["Web Development", "Backend Development", "Cloud Computing"],
  "experience_level": "Intermediate",
  "projects": [
    {
      "title": "E-Commerce REST API",
      "description": "Built using Flask, PostgreSQL, and Docker."
    }
  ],
  "preferred_career": "Backend Developer",
  "created_at": "2026-08-13T22:00:00Z",
  "updated_at": "2026-08-13T22:00:00Z"
}
```

---

## 🧮 Recommendation & Scoring Engine Design

### 1. Career Match Scoring Formula

For each of the 12 supported target job roles, a compatibility score $S_{\text{role}} \in [0, 100]$ is computed using weighted domain components:

$$\text{Score} = (W_{\text{skills}} \times S_{\text{skills}}) + (W_{\text{edu}} \times S_{\text{edu}}) + (W_{\text{proj}} \times S_{\text{proj}}) + (W_{\text{cert}} \times S_{\text{cert}}) + (W_{\text{int}} \times S_{\text{int}}) + (W_{\text{exp}} \times S_{\text{exp}})$$

#### Weight Distribution:
- **Technical Skills ($W_{\text{skills}} = 0.40$)**: Jaccard similarity / coverage of required & preferred skills for the role.
- **Education & CGPA ($W_{\text{edu}} = 0.15$)**: Match against branch relevance and CGPA thresholds (e.g. CGPA $\ge 7.0 \Rightarrow 100\%$, $6.0 - 7.0 \Rightarrow 80\%$).
- **Projects ($W_{\text{proj}} = 0.15$)**: Count and relevance of student's completed projects.
- **Certifications ($W_{\text{cert}} = 0.10$)**: Matches with domain-specific certification keywords.
- **Interests ($W_{\text{int}} = 0.10$)**: Alignment between user's selected career interests and role domain.
- **Experience Level ($W_{\text{exp}} = 0.10$)**: Progression from Beginner (60%) to Intermediate (85%) to Advanced (100%).

---

### 2. Career Readiness Score Formula

Overall Student Readiness Index $R \in [0, 100]$ evaluates general employability readiness:
- **Skill Breadth & Depth**: 35 points
- **Academic Standard (CGPA)**: 20 points
- **Practical Projects**: 20 points
- **Industry Certifications**: 15 points
- **Domain Focus & Experience**: 10 points

---

## 🔌 API & Endpoint Routing Architecture

| Method | Endpoint | Description | View / Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Home Landing Page | `templates/index.html` |
| `GET` | `/profile` | Profile Form (Create / Edit) | `templates/profile.html` |
| `POST` | `/analyze` | Form submission & analysis | Redirects to `/dashboard/<student_id>` |
| `GET` | `/dashboard/<student_id>` | Student Overview Dashboard | `templates/dashboard.html` |
| `GET` | `/results/<student_id>` | Full Career Recommendations | `templates/results.html` |
| `GET` | `/roadmap/<student_id>` | 6-Month Personalised Roadmap | `templates/roadmap.html` |
| `GET` | `/about` | Project & System Info | `templates/about.html` |
| `GET` | `/health` | Application & DB Healthcheck | JSON `{ "status": "healthy", "database": "connected" }` |
| `API GET` | `/api/student/<student_id>` | Get Student Raw Data | JSON response |
| `API PUT` | `/api/student/<student_id>` | Update Student Profile | JSON status update |

---

## 📁 Directory & Folder Structure Design

```
StudentCareerSystem/
│
├── app.py                      # Application entry point & factory
├── config.py                   # Configuration management (Dev, Test, Prod)
├── requirements.txt            # Dependency declarations
├── README.md                   # Portfolio documentation
├── .gitignore                  # Git exclusion rules
├── .env.example                # Template environment variables
│
├── models/
│   ├── __init__.py
│   └── student_model.py        # Mongo schema & DB access wrapper
│
├── services/
│   ├── __init__.py
│   ├── recommendation_service.py # Recommendation & role dataset logic
│   ├── scoring_service.py       # Readiness score calculation logic
│   └── roadmap_service.py       # Dynamic 6-month roadmap generator
│
├── routes/
│   ├── __init__.py
│   ├── main_routes.py          # General web routes (home, about, health)
│   └── student_routes.py       # Profile, dashboard, analysis routes
│
├── templates/
│   ├── base.html               # Master layout wrapper with navbar & footer
│   ├── index.html              # Landing page
│   ├── profile.html            # Profile entry & edit form
│   ├── dashboard.html          # Student dashboard
│   ├── results.html            # Detailed match breakdown
│   ├── roadmap.html            # Dynamic career roadmap view
│   ├── about.html              # About project & developer page
│   └── 404.html                # Custom 404 page
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom theme & responsive CSS styling
│   ├── js/
│   │   └── main.js             # Client validation & dynamic UI handlers
│   └── images/                 # Favicons & project graphics
│
└── tests/
    ├── __init__.py
    ├── test_scoring.py         # Unit tests for scoring logic
    ├── test_recommendation.py  # Unit tests for recommendation algorithm
    └── test_routes.py          # Integration tests for Flask endpoints
```
