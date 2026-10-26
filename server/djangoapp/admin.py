from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5


class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'year', 'dealer_id']
    list_filter = ['type']
    search_fields = ['name', 'car_make__name']


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'country_of_origin']
    search_fields = ['name']
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
