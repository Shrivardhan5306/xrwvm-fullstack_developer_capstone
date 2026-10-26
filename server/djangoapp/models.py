from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Name')
    description = models.CharField(null=False, max_length=200, default='Description')

    def __str__(self):
        return "Name: " + self.name + "," + "Description: " + self.description


class CarModel(models.Model):
    CarMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Name')
    dealer_id = models.IntegerField(null=True)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('SPORT', 'Sport'),
        ('PICKUP', 'Pickup'),
    ]
    type = models.CharField(null=False, max_length=10, choices=CAR_TYPES, default='SUV')
    year = models.IntegerField(
        null=True,
        validators=[MaxValueValidator(2023), MinValueValidator(2015)]
    )

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.type
