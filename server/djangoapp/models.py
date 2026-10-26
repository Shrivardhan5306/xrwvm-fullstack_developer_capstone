from django.db import models
from django.utils.timezone import now


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Name')
    description = models.CharField(null=False, max_length=200, default='Description')
    country_of_origin = models.CharField(null=True, max_length=50, default='USA')

    def __str__(self):
        return "Name: " + self.name + ", " + "Description: " + self.description


# Car Model model
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Name')
    dealer_id = models.IntegerField(null=True)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('SPORT', 'Sport'),
        ('COUPE', 'Coupe'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(null=False, max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.type


# Plain Python class to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# Plain Python class to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review + " by " + self.name
