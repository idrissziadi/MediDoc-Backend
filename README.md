# MediDoc - Digital Patient Record (DPI) — Backend

## Overview
This repository contains the backend for the Digital Patient Record (DPI) management system, built using Django and Django REST Framework (DRF). The backend provides a secure and efficient API for managing patient records, medical history, treatments, prescriptions, and test results. It ensures that healthcare professionals have seamless access to up-to-date patient data.

## Table of Contents
- Project Overview
- Key Features
- Tech Stack
- Getting Started
- Running the Application
- API Documentation
- Database Migrations
- Testing
- Deployment
- Further Reading & References

## Key Features
- **User Authentication & Authorization**: Secure login for doctors, nurses, pharmacists, and lab technicians using JWT.
- **Patient Record Management**: Store and retrieve patient demographics, medical history, and visits.
- **Medical Consultations**: Retrieve a patient’s record via unique ID or QR code.
- **Diagnosis & Prescription Management**: Record diagnosis, prescribe medications, and request additional tests.
- **Nursing Care**: Track interventions, medication administration, and patient monitoring.
- **Pharmacy Module**: Manage in-house pharmacy inventory and verify prescriptions.
- **Lab & Imaging Integration**: Store lab test results and medical imaging reports.
- **Patient Self-Service Portal**: Patients can view records, request medical documents, and access billing summaries.
- **Role-Based Access Control (RBAC)**: Ensures proper data access per user role.

## Tech Stack
- **Framework**: Django
- **API Development**: Django REST Framework (DRF)
- **Database**: PostgreSQL (Recommended), SQLite (for development)
- **Authentication**: JWT (JSON Web Tokens)
- **Storage**: AWS S3 / Local storage for file uploads
- **Containerization**: Docker (Optional)

## Getting Started
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL (or SQLite for local development)
- pip & virtualenv

### Installation
Clone the repository:
```bash
git clone (https://github.com/idrissziadi/MediDoc-Backend)
cd MediDoc-Backend
```
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Set up environment variables:
Create a `.env` file in the project root and add the following:
```env
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/medidoc_db
```

### Database Migrations
Run migrations to set up the database schema:
```bash
python manage.py migrate
```

### Running the Application
Start the Django development server:
```bash
python manage.py runserver
```
The API will be available at:
[http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

## API Documentation
API endpoints are documented using **Swagger** and **DRF Spectacular**.
To access API docs:
- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

## Testing
Run automated tests:
```bash
python manage.py test
```

## Deployment
For production deployment, configure:
- **Gunicorn & Nginx** for serving the application.
- **Docker & Docker Compose** (optional) for containerized deployment.
- **CI/CD pipeline** using GitHub Actions or GitLab CI.

Example production setup:
```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 medidoc.wsgi:application
```

## Further Reading & References
- [Django Official Documentation](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Authentication in Django](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

---
Thank you for using **MediDoc - Digital Patient Record (DPI) Backend**. For any issues or contributions, feel free to open a pull request or an issue.

