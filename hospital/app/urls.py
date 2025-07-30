from django.urls import path, include  # Added include here
from .views import Home, About, Services, Appointment, user_login, Logout_admin, Index, Register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Home, name='home_root'),
    path('home/', Home, name='home'),
    path('about/', About, name='about'),
    path('services/', Services, name='services'),
    path('appointment/', Appointment, name='appointment'),
    path('login/', user_login, name='login'),  # Custom login view
    path('logout/', Logout_admin, name='logout_admin'),
    path('admin_dashboard/', Index, name='index'),  # Admin dashboard
    path('register/', Register, name='register'),

]



