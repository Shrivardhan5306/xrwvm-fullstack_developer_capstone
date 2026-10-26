from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for about view
    path('about/', views.about, name='about'),

    # path for contact us view
    path('contact/', views.contact, name='contact'),

    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logout
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/review/', views.add_review, name='add_review'),

    # path for getting car makes/models JSON
    path('get_cars/', views.get_cars, name='get_cars'),

    # REST API paths for assessment verification
    path('api/dealers/', views.get_dealers_api, name='get_dealers_api'),
    path('api/reviews/', views.get_dealer_reviews_api, name='get_dealer_reviews_api'),
    path('api/analyze/', views.analyze_review_api, name='analyze_review_api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
