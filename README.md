# Best Cars Dealership

- **Repository Name**: `agfzb-CloudAppDevelopment_Capstone`
- **Project Name**: `Best Cars Dealership`

---

## Project Overview

**Best Cars Dealership** is a comprehensive full-stack web application built with Django and Python as part of the **IBM Full-Stack Software Developer Professional Certificate Capstone Project**.

This application allows users to:
- Browse a verified nationwide directory of car dealerships across the United States.
- Filter dealerships dynamically by state (e.g. Kansas, Texas, California).
- View dealer details and customer reviews with IBM Watson NLU sentiment analysis badges.
- Post authenticated reviews and vehicle purchase details for any dealership.
- Explore available car makes and models through REST APIs and the Django admin interface.

---

## Technology Stack

- **Backend**: Django 3.1.3 (Python 3.11)
- **Frontend**: Django Templates, Bootstrap 4, React component integration
- **Database**: SQLite (local development), IBM Cloudant (dealer and review documents)
- **Sentiment Analysis**: IBM Watson Natural Language Understanding (NLU)
- **Deployment**: IBM Cloud Code Engine
- **CI/CD**: GitHub Actions workflows

---

## Repository Structure

```
agfzb-CloudAppDevelopment_Capstone/
├── .github/workflows/          # CI/CD workflows (linter & deployment)
├── server/
│   ├── djangoapp/              # Main Django application
│   │   ├── models.py           # CarMake, CarModel, CarDealer, DealerReview
│   │   ├── views.py            # Application views and REST endpoints
│   │   ├── urls.py             # URL routing
│   │   ├── admin.py            # Admin configuration with inlines
│   │   ├── restapis.py         # Cloud Function and Watson NLU client
│   │   └── templates/          # HTML templates
│   ├── frontend/
│   │   ├── src/components/     # React components (Register.jsx)
│   │   └── static/             # Static pages (About.html, Contact.html)
│   ├── djangobackend/          # Project settings
│   ├── static/                 # Static media and assets
│   └── manage.py
└── README.md
```

---

## Quickstart Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Shrivardhan5306/agfzb-CloudAppDevelopment_Capstone.git
cd agfzb-CloudAppDevelopment_Capstone/server
```

### 2. Set Up Virtual Environment & Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Migrations & Start Server
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visit `http://localhost:8000/djangoapp/` in your browser.

---

## Author & License

- **Author**: Shrivardhan Patil ([@Shrivardhan5306](https://github.com/Shrivardhan5306))
- **License**: Apache License 2.0
