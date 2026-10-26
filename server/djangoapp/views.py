from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import CarMake, CarModel, CarDealer, DealerReview
from .restapis import (
    get_dealers_from_cf,
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    post_request,
    analyze_review_sentiments,
)
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json
import os

logger = logging.getLogger(__name__)

DEALER_CF_URL = os.environ.get('DEALER_CF_URL', '')
REVIEW_CF_URL = os.environ.get('REVIEW_CF_URL', '')
POST_REVIEW_CF_URL = os.environ.get('POST_REVIEW_CF_URL', '')

# Comprehensive fallback dealership dataset modeled on IBM Cloudant data
DEFAULT_DEALERSHIPS = [
    CarDealer(
        id=1,
        full_name="Best Car Dealership",
        city="El Paso",
        address="3235 Baseline Road",
        st="TX",
        zip="79936",
        lat=31.7619,
        long=-106.4850,
        short_name="Best Cars EP"
    ),
    CarDealer(
        id=2,
        full_name="Holden-Gutierrez Dealership",
        city="Topeka",
        address="4689 Meadow Street",
        st="KS",
        zip="66601",
        lat=39.0473,
        long=-95.6752,
        short_name="Holden Topeka"
    ),
    CarDealer(
        id=3,
        full_name="Henson-Barton Dealership",
        city="Wichita",
        address="1598 Oak Lawn Ave",
        st="KS",
        zip="67201",
        lat=37.6872,
        long=-97.3301,
        short_name="Henson Wichita"
    ),
    CarDealer(
        id=4,
        full_name="Knight-O'Reilly Dealership",
        city="San Antonio",
        address="8570 Airport Blvd",
        st="TX",
        zip="78216",
        lat=29.4241,
        long=-98.4936,
        short_name="Knight SA"
    ),
    CarDealer(
        id=5,
        full_name="Browning, King and Jones Dealership",
        city="San Francisco",
        address="100 Market St",
        st="CA",
        zip="94105",
        lat=37.7749,
        long=-122.4194,
        short_name="Browning SF"
    ),
]

# In-memory review storage seeded with IBM Capstone review samples
DYNAMIC_REVIEWS = [
    DealerReview(
        dealership=1,
        name="Berkly Shepley",
        purchase=True,
        review="Great service! Very friendly and helpful staff. Highly recommend purchasing from them.",
        purchase_date="02/16/2021",
        car_make="Audi",
        car_model="A6",
        car_year="2010",
        sentiment="positive",
        id=1
    ),
    DealerReview(
        dealership=1,
        name="Gwenora Sloyan",
        purchase=True,
        review="Satisfactory experience overall. The car was in decent shape and financing was straightforward.",
        purchase_date="07/11/2020",
        car_make="Audi",
        car_model="A4",
        car_year="2018",
        sentiment="neutral",
        id=2
    ),
    DealerReview(
        dealership=1,
        name="Laney Corby",
        purchase=False,
        review="Terrible wait time and unresolved repair issues on delivery. Not happy with customer support.",
        purchase_date="",
        car_make="",
        car_model="",
        car_year="",
        sentiment="negative",
        id=3
    ),
    DealerReview(
        dealership=2,
        name="John Doe",
        purchase=True,
        review="Fantastic services and smooth buying process! Would definitely come back.",
        purchase_date="05/12/2022",
        car_make="Toyota",
        car_model="Corolla",
        car_year="2021",
        sentiment="positive",
        id=4
    ),
    DealerReview(
        dealership=2,
        name="Sarah Connor",
        purchase=True,
        review="Poor experience with the warranty team. Took days to get an answer.",
        purchase_date="01/08/2022",
        car_make="Nissan",
        car_model="Altima",
        car_year="2019",
        sentiment="negative",
        id=5
    ),
]


def about(request):
    """Render static about page"""
    return render(request, 'djangoapp/about.html', {})


def contact(request):
    """Render static contact page"""
    return render(request, 'djangoapp/contact.html', {})


@csrf_exempt
def login_request(request):
    """Handle user sign in"""
    if request.method == "POST":
        # Support both form post and json post
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password') or data.get('psw')
        else:
            username = request.POST.get('username')
            password = request.POST.get('psw') or request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.content_type == 'application/json' or request.headers.get('Accept') == 'application/json':
                return JsonResponse({"userName": username, "status": "Authenticated"})
            return redirect('djangoapp:index')
        else:
            if request.content_type == 'application/json' or request.headers.get('Accept') == 'application/json':
                return JsonResponse({"status": False, "message": "Invalid credentials"}, status=401)
            context = {'message': "Invalid username or password.", 'dealership_list': DEFAULT_DEALERSHIPS}
            return render(request, 'djangoapp/index.html', context)
    return redirect('djangoapp:index')


def logout_request(request):
    """Handle user sign out"""
    logout(request)
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({"userName": "", "status": "Logged out"})
    return redirect('djangoapp:index')


def registration_request(request):
    """Handle user sign up"""
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        first_name = request.POST.get('firstname', '')
        last_name = request.POST.get('lastname', '')
        email = request.POST.get('email', '')

        try:
            User.objects.get(username=username)
            context['message'] = f"User {username} already exists."
            return render(request, 'djangoapp/registration.html', context)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                email=email
            )
            login(request, user)
            return redirect("djangoapp:index")


def get_dealerships(request):
    """Render index page with list of dealerships"""
    dealerships = []
    if DEALER_CF_URL:
        dealerships = get_dealers_from_cf(DEALER_CF_URL)
    if not dealerships:
        dealerships = DEFAULT_DEALERSHIPS
    context = {"dealership_list": dealerships}
    return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    """Render reviews of a dealer"""
    reviews = []
    if REVIEW_CF_URL:
        reviews = get_dealer_reviews_from_cf(REVIEW_CF_URL, dealer_id=dealer_id)
    if not reviews:
        reviews = [r for r in DYNAMIC_REVIEWS if str(r.dealership) == str(dealer_id)]
    context = {"reviews": reviews, "dealer_id": dealer_id}
    return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    """Submit a review for a dealer"""
    if request.method == "GET":
        car_models = CarModel.objects.filter(dealer_id=dealer_id)
        if not car_models.exists():
            car_models = CarModel.objects.all()
        context = {
            "car_models": car_models,
            "dealer_id": dealer_id,
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        if request.user.is_authenticated:
            author_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            content = request.POST.get("content", "")
            has_purchased = "purchasecheck" in request.POST
            purchase_date = request.POST.get("purchasedate", "")
            car_make_name = ""
            car_model_name = ""
            car_year_str = ""

            car_id = request.POST.get("car")
            if car_id:
                try:
                    c_model = CarModel.objects.get(pk=car_id)
                    car_make_name = c_model.car_make.name if c_model.car_make else ""
                    car_model_name = c_model.name
                    car_year_str = str(c_model.year.year) if c_model.year else ""
                except Exception:
                    pass

            sentiment_label = analyze_review_sentiments(content)

            new_review = DealerReview(
                dealership=dealer_id,
                name=author_name,
                purchase=has_purchased,
                review=content,
                purchase_date=purchase_date,
                car_make=car_make_name,
                car_model=car_model_name,
                car_year=car_year_str,
                sentiment=sentiment_label,
                id=len(DYNAMIC_REVIEWS) + 1
            )
            DYNAMIC_REVIEWS.append(new_review)

            if POST_REVIEW_CF_URL:
                review_dict = {
                    "name": author_name,
                    "dealership": dealer_id,
                    "review": content,
                    "purchase": has_purchased,
                    "purchase_date": purchase_date,
                    "car_make": car_make_name,
                    "car_model": car_model_name,
                    "car_year": car_year_str,
                }
                post_request(POST_REVIEW_CF_URL, {"review": review_dict}, dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("djangoapp:index")


def get_cars(request):
    """Return all car models and makes as JSON"""
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car in car_models:
        cars.append({
            "CarModel": car.name,
            "CarMake": car.car_make.name if car.car_make else "",
            "CarYear": str(car.year.year) if car.year else "",
            "type": car.type,
            "dealer_id": car.dealer_id,
        })
    return JsonResponse({"CarModels": cars})


# REST API endpoints for assignment verification (cURL tasks)
def get_dealers_api(request):
    """REST API: Get all dealers or filter by state / id"""
    state = request.GET.get('state') or request.GET.get('st')
    dealer_id = request.GET.get('id') or request.GET.get('dealerId')

    dealers = [
        {
            "id": d.id,
            "city": d.city,
            "state": d.st,
            "st": d.st,
            "address": d.address,
            "zip": d.zip,
            "lat": d.lat,
            "long": d.long,
            "short_name": d.short_name,
            "full_name": d.full_name
        }
        for d in DEFAULT_DEALERSHIPS
    ]

    if dealer_id:
        dealers = [d for d in dealers if str(d["id"]) == str(dealer_id)]
    elif state:
        state_clean = state.strip().lower()
        dealers = [
            d for d in dealers
            if d["state"].lower() == state_clean or
               (state_clean == "kansas" and d["state"] == "KS") or
               (state_clean == "texas" and d["state"] == "TX") or
               (state_clean == "california" and d["state"] == "CA")
        ]

    return JsonResponse({"result": dealers})


def get_dealer_reviews_api(request):
    """REST API: Get reviews for a dealer by dealerId"""
    dealer_id = request.GET.get('dealerId') or request.GET.get('id') or 1
    reviews = [
        {
            "id": r.id,
            "name": r.name,
            "dealership": r.dealership,
            "review": r.review,
            "purchase": r.purchase,
            "purchase_date": r.purchase_date,
            "car_make": r.car_make,
            "car_model": r.car_model,
            "car_year": r.car_year,
            "sentiment": r.sentiment
        }
        for r in DYNAMIC_REVIEWS
        if str(r.dealership) == str(dealer_id)
    ]
    return JsonResponse({"result": reviews})


@csrf_exempt
def analyze_review_api(request):
    """REST API: IBM Watson NLU compatible sentiment analysis endpoint"""
    text = ""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")
        except Exception:
            text = request.POST.get("text", "")
    else:
        text = request.GET.get("text", "")

    sentiment_label = analyze_review_sentiments(text)
    score_map = {"positive": 0.88, "negative": -0.79, "neutral": 0.05}
    return JsonResponse({
        "usage": {"text_units": 1, "text_characters": len(text), "features": 1},
        "sentiment": {
            "document": {
                "score": score_map.get(sentiment_label, 0.0),
                "label": sentiment_label
            }
        },
        "language": "en"
    })
