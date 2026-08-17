# CareerForge – Student Career & Job Recommendation System

[![Python Version](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/database-MongoDB-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A full-stack, rule-based career analytics and job recommendation application designed to help computer science students and fresh graduates identify suitable technology job roles, quantify employability readiness, analyze skill gaps, and generate personalized 6-month learning roadmaps.

---

## 🌟 Features

- **Interactive Profile Assessment**: Multi-section form capturing degree, branch, CGPA, technical skills, certifications, domain interests, experience level, and portfolio projects.
- **Rule-Based Recommendation Engine**: Compares profiles against 12 high-demand software job roles (*Software Developer, Backend, Frontend, Full Stack, Data Analyst, Data Scientist, ML Engineer, Cloud, DevOps, Database Dev, Cybersecurity, QA*).
- **Employability Readiness Index (0–100)**: Diagnostic score breakdown across Technical Skills, CGPA Standard, Projects, Certifications, and Experience.
- **Dynamic 6-Month Roadmap Generator**: Custom step-by-step monthly learning plan tailored to bridge identified missing skills.
- **Interactive Dashboard**: Visual overview featuring readiness score gauge, top 3 role matches, strengths, and missing skills.
- **MongoDB Integration with Fallback**: PyMongo storage layer supporting local MongoDB, MongoDB Atlas cloud, and automatic local fallback storage if MongoDB is offline.
- **Automated Test Suite**: Pytest suite covering scoring logic, recommendation algorithm, data models, and Flask routes.

---

## 🏗️ System Architecture

```
+-----------------------------------------------------------------------+
|                            USER BROWSER                               |
|          HTML5 + CSS3 (Bootstrap 5) + Vanilla JS (Fetch API)          |
+-----------------------------------+-----------------------------------+
                                    | HTTP Requests / HTML & JSON
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
                                       | PyMongo Client (with Fallback)
                                       v
+-----------------------------------------------------------------------+
|                           MONGODB DATABASE                            |
|                  (Collection: `students` in `career_db`)              |
+-----------------------------------------------------------------------+
```

---

## 📐 Recommendation Algorithm & Math Formula

For each of the 12 target job roles, a compatibility score $S_{\text{role}} \in [0, 100]$ is computed using weighted domain components:

$$\text{Score} = (W_{\text{skills}} \times S_{\text{skills}}) + (W_{\text{edu}} \times S_{\text{edu}}) + (W_{\text{proj}} \times S_{\text{proj}}) + (W_{\text{cert}} \times S_{\text{cert}}) + (W_{\text{int}} \times S_{\text{int}}) + (W_{\text{exp}} \times S_{\text{exp}})$$

### Component Weights:
- **Technical Skills (40%)**: Coverage of required and preferred skills.
- **Academic CGPA (15%)**: Evaluated against role CGPA thresholds.
- **Projects (15%)**: Quantity and technical detail of portfolio projects.
- **Certifications (10%)**: Relevance of industry certifications.
- **Interests (10%)**: Domain alignment.
- **Experience Level (10%)**: Progression from Beginner (60%) to Advanced (100%).

---

## 📁 Directory Structure

```
StudentCareerSystem/
│
├── app.py                      # Application entry point & factory
├── config.py                   # Configuration management (Dev, Test, Prod)
├── requirements.txt            # Dependency declarations
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusion rules
├── .env.example                # Template environment variables
│
├── models/
│   └── student_model.py        # MongoDB model wrapper with fallback storage
│
├── services/
│   ├── recommendation_service.py # Recommendation & 12-role dataset logic
│   ├── scoring_service.py       # Readiness score calculation logic
│   └── roadmap_service.py       # Dynamic 6-month roadmap generator
│
├── routes/
│   ├── main_routes.py          # Landing, about, healthcheck routes
│   └── student_routes.py       # Profile assessment, dashboard, api routes
│
├── templates/
│   ├── base.html               # Master layout wrapper with navbar & footer
│   ├── index.html              # Landing page
│   ├── profile.html            # Profile assessment form
│   ├── dashboard.html          # Student overview dashboard
│   ├── results.html            # Detailed match breakdown
│   ├── roadmap.html            # Dynamic career roadmap view
│   ├── about.html              # About project page
│   └── 404.html                # Custom error page
│
├── static/
│   ├── css/style.css           # Modern custom CSS styles
│   └── js/main.js              # Dynamic form handlers & validation
│
└── tests/
    ├── test_scoring.py         # Unit tests for scoring logic
    ├── test_recommendation.py  # Unit tests for recommendation engine
    └── test_routes.py          # Integration tests for Flask endpoints
```

---

## ⚡ Quick Start & Local Running Instructions

### Prerequisites
- Python 3.10+
- Git

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-username/StudentCareerSystem.git
cd StudentCareerSystem
```

### 2. Create Virtual Environment & Install Dependencies
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🧪 Running Automated Tests

Run the full pytest suite:
```bash
pytest -v
```

---

## 🚀 Deployment Instructions

### Deploying to Render.com / PythonAnywhere

1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Add `gunicorn` to `requirements.txt`:
   ```
   pip install gunicorn
   pip freeze > requirements.txt
   ```
3. Set Environment Variables in deployment platform dashboard:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-production-secret-key`
   - `MONGODB_URI=your-mongodb-atlas-uri`

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).

## Live Demo

🚀 Live Demo: Coming soon

📂 GitHub: https://github.com/Naveenkumar04-tech/careerforge
