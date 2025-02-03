# MediDoc - Digital Patient Record (DPI) — Backend

This repository contains the **backend** for the Digital Patient Record (DPI) management system. The goal of the platform is to consolidate and centralize patient data—such as medical history, treatments, test results, and prescriptions—into a single, easily accessible digital file. By improving communication between healthcare professionals, this system helps streamline workflows and provides more consistent care for patients.

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)
5. [Installation](#installation)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)  
8. [Testing](#testing)  
9. [Building](#building)  
10. [Further Reading & References](#further-reading--references)  

---

## Project Overview

The **Digital Patient Record (DPI)** is designed to make patient data management as efficient and transparent as possible. By using the DPI, healthcare professionals (doctors, nurses, pharmacists, lab technicians, etc.) can readily access, update, and share patient information. This reduces administrative overhead, minimizes paperwork, and ensures that medical data is synchronized across the entire organization.

### Why MediDoc?
- **Better Patient Care**: Provides quick access to patient history and treatment records.
- **Improved Coordination**: Enables different departments to share updates, results, and prescriptions in real time.
- **Reduced Errors**: Minimizes duplicated tests, missing information, and prescription errors.
  

---

## Key Features

1. **Patient Admission**  
   - Create a digital record with identification details and basic administrative data.
2. **Medical Consultations**  
   - Quickly retrieve a patient’s file by SSN or by scanning a QR code.
3. **Diagnosis & Prescription**  
   - Record visit summaries, prescribe medications, and order additional tests.
4. **Nursing Care**  
   - Track nursing interventions, from administering medications to monitoring patient conditions.
5. **Pharmacy Management**  
   - Access the in-house Hospital Pharmacy Management System (HPMS) to verify and dispense prescriptions.
6. **Lab & Imaging**  
   - Input test results and upload imaging directly into the system.
7. **Patient Self-Service**  
   - Allow patients to view their records, request medical certificates, and access a summary of hospital fees.

---

## Tech Stack

- **Framework**: [Django](https://www.djangoproject.com/) (Python-based)
- **Language**: [Python](https://www.python.org/)
- **API Framework**: [Django Rest Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication**: [JWT (JSON Web Tokens)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- **Database**: [MySQL](https://www.mysql.com/)
- **Build & Tooling**: [Pipenv](https://pipenv.pypa.io/)
- **Testing**: [Pytest](https://docs.pytest.org/)
- **API Documentation**: [Swagger/OpenAPI](https://drf-yasg.readthedocs.io/en/stable/)

---

# Getting Started

## Prerequisites
1. **Python** (version 3.8 or higher)  
   - [Download Python](https://www.python.org/downloads/)
2. **Pipenv**  
   Install Pipenv globally:
   ```bash
   pip install pipenv
   ```
3. **MySQL Database**  
   - [Download MySQL](https://www.mysql.com/downloads/)
4. **Django** and **Django Rest Framework** will be installed as dependencies.

---

## Installation
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/soualahmohammedzakaria/MediDoc-Backend.git
   cd MediDoc-Backend
   ```
2. **Set Up Virtual Environment**  
   Create and activate a virtual environment using Pipenv:
   ```bash
   pipenv install
   pipenv shell
   ```
3. **Configure Database**  
   Update `DATABASES` in `settings.py` to match your MySQL setup:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
4. **Apply Migrations**  
   Run database migrations to set up initial schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Create Superuser**  
   Create an admin account:
   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

Open your browser and navigate to:  
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

> **Note**: Ensure your MySQL database server is running before starting the application.

---

## API Endpoints

This project uses Django Rest Framework for API development. The endpoints are documented using Swagger/OpenAPI.

### Access API Documentation
- Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- ReDoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

> **Note**: Swagger and ReDoc URLs may require authentication if enabled in `settings.py`.

---

## Testing

Run tests using Pytest:
```bash
pytest
```

Generate a coverage report:
```bash
pytest --cov
```

---

## Building

### Collect Static Files:
```bash
python manage.py collectstatic
```

### Production Server:
Use a production-grade server like Gunicorn or uWSGI:
```bash
gunicorn digital_patient_record.wsgi:application --bind 0.0.0.0:8000
```

---

## Further Reading & References

- [MediDoc Frontend](https://github.com/soualahmohammedzakaria/MediDoc)
- [MediDoc SGPH](https://github.com/soualahmohammedzakaria/MediDoc-SGPH)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)  
- [Django Rest Framework Documentation](https://www.django-rest-framework.org/)  
- [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)  
- [Swagger/OpenAPI Documentation](https://swagger.io/specification/)  
- [Pytest Documentation](https://docs.pytest.org/en/latest/)

---

**Thank you for checking out the Digital Patient Record (DPI) MediDoc — Backend project.** If you have any questions, suggestions, or feedback, feel free to open an issue or submit a pull request.  

*Maintained by the MediDoc Team.*
