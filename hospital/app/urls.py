from django.urls import path
from .views import Home, About, Services, Appointment

urlpatterns = [
    path('', Home, name='home_root'),  # Handles root URL
    path('home/', Home, name='home'),
    path('about/', About, name='about'),
    path('services/', Services, name='services'),
    path('appointment/', Appointment, name='appointment'),  # Removed views. prefix
]