# Best Cars Dealership - IBM Full-Stack Development Capstone

## Project Overview

Best Cars Dealership is a full-stack web application built with Django and Python as part of the IBM Full-Stack Software Developer Professional Certificate capstone project.

This application allows users to:
- Browse a list of car dealerships across the United States
- Read reviews for individual dealerships
- Submit reviews for dealerships (authenticated users only)
- View car makes and models available at dealerships

## Technology Stack

- **Backend**: Django 3.1.3 (Python)
- **Frontend**: Django Templates + Bootstrap 4
- **Database**: SQLite (local), IBM Cloudant (dealer/review data)
- **Sentiment Analysis**: IBM Watson Natural Language Understanding
- **Deployment**: IBM Cloud Code Engine / Docker
- **CI/CD**: GitHub Actions

## Project Structure

```
server/
├── djangoapp/          # Main Django application
│   ├── models.py       # CarMake, CarModel, CarDealer, DealerReview
│   ├── views.py        # All view functions
│   ├── urls.py         # URL routing
│   ├── admin.py        # Admin configuration
│   ├── restapis.py     # Cloud Function integration & Watson NLU
│   └── templates/      # HTML templates
├── djangobackend/      # Django project settings
├── static/             # Static assets
└── manage.py
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Shrivardhan5306/agfzb-CloudAppDevelopment_Capstone.git
cd agfzb-CloudAppDevelopment_Capstone/server
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

Visit http://localhost:8000/djangoapp/ to see the application.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /djangoapp/` | List all dealerships |
| `GET /djangoapp/dealer/<id>/` | Dealer reviews |
| `GET /djangoapp/dealer/<id>/review/` | Add review form |
| `POST /djangoapp/dealer/<id>/review/` | Submit a review |
| `GET /djangoapp/get_cars/` | All car makes and models |
| `GET /djangoapp/about/` | About Us page |
| `GET /djangoapp/contact/` | Contact Us page |
| `GET /djangoapp/registration/` | Registration page |
| `POST /djangoapp/login/` | Login |
| `GET /djangoapp/logout/` | Logout |

## Environment Variables

Set the following environment variables for production:

- `NLU_URL` - IBM Watson NLU API URL
- `NLU_API_KEY` - IBM Watson NLU API Key
- `DEALER_CF_URL` - IBM Cloud Function URL for dealers
- `REVIEW_CF_URL` - IBM Cloud Function URL for reviews
- `POST_REVIEW_CF_URL` - IBM Cloud Function URL for posting reviews

## License

Apache License 2.0 - see LICENSE file for details.

## Author

Shrivardhan Patil (Shrivardhan5306)
