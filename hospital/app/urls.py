from django.urls import path, include  # Added include here
from .views import Home, About, Services, Appointment, Login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Home, name='home_root'),
    path('home/', Home, name='home'),
    path('about/', About, name='about'),
    path('services/', Services, name='services'),
    path('appointment/', Appointment, name='appointment'),
    path('admin_login/', Login, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),  # This will include all auth URLs
]