import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview
import os

NLU_URL = os.environ.get('NLU_URL', '')
NLU_API_KEY = os.environ.get('NLU_API_KEY', '')


def get_request(url, **kwargs):
    """Make HTTP GET requests"""
    print("GET from {} ".format(url))
    try:
        if 'api_key' in kwargs:
            params = dict()
            params["text"] = kwargs.get("text", "")
            params["version"] = kwargs.get("version", "2021-08-01")
            params["features"] = kwargs.get("features", "sentiment")
            params["return_analyzed_text"] = kwargs.get("return_analyzed_text", True)
            response = requests.get(
                url,
                params=params,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', kwargs["api_key"])
            )
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, timeout=5)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as err:
        print("Network request error: {0}".format(err))
        return None


def post_request(url, json_payload, **kwargs):
    """Make HTTP POST requests"""
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload, timeout=5)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as err:
        print("Network request error: {0}".format(err))
        return None


def get_dealers_from_cf(url, **kwargs):
    """Get dealers from Cloud Function"""
    results = []
    json_result = get_request(url, **kwargs)
    if json_result and "result" in json_result:
        dealers = json_result["result"]
        for dealer_doc in dealers:
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""),
                city=dealer_doc.get("city", ""),
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id"),
                lat=dealer_doc.get("lat", 0.0),
                long=dealer_doc.get("long", 0.0),
                short_name=dealer_doc.get("short_name", ""),
                st=dealer_doc.get("st", ""),
                zip=dealer_doc.get("zip", "")
            )
            results.append(dealer_obj)
    return results


def get_dealer_by_id_from_cf(url, dealer_id):
    """Get a dealer by ID from Cloud Function"""
    json_result = get_request(url, dealerId=dealer_id)
    if json_result and "result" in json_result and len(json_result["result"]) > 0:
        dealer_doc = json_result["result"][0]
        dealer_obj = CarDealer(
            address=dealer_doc.get("address", ""),
            city=dealer_doc.get("city", ""),
            full_name=dealer_doc.get("full_name", ""),
            id=dealer_doc.get("id"),
            lat=dealer_doc.get("lat", 0.0),
            long=dealer_doc.get("long", 0.0),
            short_name=dealer_doc.get("short_name", ""),
            st=dealer_doc.get("st", ""),
            zip=dealer_doc.get("zip", "")
        )
        return dealer_obj
    return None


def get_dealer_reviews_from_cf(url, dealer_id):
    """Get reviews for a dealer from Cloud Function"""
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result and "result" in json_result:
        reviews = json_result["result"]
        for review_doc in reviews:
            review_obj = DealerReview(
                dealership=review_doc.get("dealership"),
                name=review_doc.get("name"),
                purchase=review_doc.get("purchase"),
                review=review_doc.get("review"),
                purchase_date=review_doc.get("purchase_date"),
                car_make=review_doc.get("car_make"),
                car_model=review_doc.get("car_model"),
                car_year=review_doc.get("car_year"),
                sentiment=analyze_review_sentiments(review_doc.get("review", "")),
                id=review_doc.get("id")
            )
            results.append(review_obj)
    return results


def analyze_review_sentiments(text):
    """Call Watson NLU to analyze sentiment, with rule-based fallback"""
    if NLU_URL and NLU_API_KEY:
        params = dict()
        params["text"] = text
        params["version"] = "2021-08-01"
        params["features"] = "sentiment"
        params["return_analyzed_text"] = True
        try:
            response = get_request(NLU_URL, api_key=NLU_API_KEY, **params)
            if response and "sentiment" in response:
                label = response["sentiment"]["document"]["label"]
                return label
        except Exception as err:
            print("Sentiment error: {}".format(err))

    # Fallback sentiment analysis based on keywords
    text_lower = (text or "").lower()
    positive_words = ["great", "excellent", "best", "good", "love", "fantastic", "amazing", "smooth", "happy", "friendly", "helpful", "recommend", "satisfied"]
    negative_words = ["terrible", "bad", "awful", "horrible", "worst", "poor", "rude", "scam", "broken", "never", "not happy", "unresolved"]

    pos_score = sum(1 for w in positive_words if w in text_lower)
    neg_score = sum(1 for w in negative_words if w in text_lower)

    if pos_score > neg_score:
        return "positive"
    elif neg_score > pos_score:
        return "negative"
    return "neutral"
