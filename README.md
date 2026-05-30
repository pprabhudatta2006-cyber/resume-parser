# AI Resume Parser API

A production-ready AI-powered Resume Parsing and Candidate Matching API built with Django, Django REST Framework, and spaCy.

## Features

- **Resume Parsing**: Automatically extracts Name, Email, Phone, Skills, Education, and Experience from PDF and DOCX files.
- **NLP Powered**: Uses `spaCy` for Named Entity Recognition (NER) and profile classification.
- **Candidate Classification**: Classifies candidates into profiles (AI/ML, Data Science, DevOps, etc.).
- **Matching Engine**: Ranks candidates against Job Descriptions based on skills and experience.
- **Secure**: JWT Authentication and file validation.
- **Scalable Architecture**: Follows Clean Architecture principles.
- **API Documentation**: Interactive Swagger/OpenAPI UI.

## Tech Stack

- **Backend**: Python 3.12, Django 5, DRF
- **NLP**: spaCy, PyMuPDF, python-docx
- **Database**: PostgreSQL
- **Auth**: SimpleJWT
- **Containerization**: Docker, Docker Compose

---

## Installation & Setup

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd resume-parser
   ```

2. **Create .env file**:
   ```env
   DEBUG=1
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://postgres:postgres@db:5432/resume_parser_db
   ```

3. **Build and run**:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   - API: `http://localhost:8000/api/`
   - Documentation: `http://localhost:8000/api/docs/`

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/refresh/` - Refresh access token

### Resumes
- `POST /api/resumes/` - Upload a resume (PDF/DOCX)
- `GET /api/resumes/` - List uploaded resumes
- `POST /api/resumes/{id}/parse/` - Trigger NLP parsing
- `GET /api/resumes/parsed/{id}/` - Get structured data

### Matching
- `POST /api/jobs/jobs/` - Create a Job Description
- `POST /api/jobs/jobs/{id}/match/` - Match candidates to JD
- `GET /api/jobs/candidates/ranking/` - Get ranked candidates

---

## Architecture

```text
├── apps/                 # Django applications
│   ├── authentication/   # User management & JWT
│   ├── resumes/          # Resume upload & parsing
│   └── matching/         # Matching engine
├── services/             # Core business logic (NLP, Matching)
├── repositories/         # Data access layer
├── utils/                # Helper functions (File extraction)
├── config/               # Project settings & URL routing
└── Dockerfile            # Container configuration
```

## NLP & AI Logic

The current system uses `spaCy` (Medium model) and Regex for data extraction. To improve accuracy for complex sections like Education and Work Experience, you can:
1. **Custom NER Training**: Train a spaCy model on labeled resume data.
2. **LLM Integration**: Use Gemini 1.5 or GPT-4o for structured extraction (replaces the `NLPService` logic).
3. **Pydantic Validation**: Use Pydantic models for strict schema validation of extracted data.

---

## Deployment Guide

### AWS (Elastic Beanstalk / ECS)
- Push image to ECR.
- Set up RDS PostgreSQL.
- Configure Environment Variables (SECRET_KEY, DATABASE_URL).
- Use `gunicorn` as the WSGI server.

### Render
- Connect your GitHub repo.
- Select Web Service.
- Add PostgreSQL database.
- Add Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_md`
- Start Command: `gunicorn config.wsgi:application`
