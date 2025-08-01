from django.urls import path
from .views import (
    Home, About, Services, Appointment,
    user_login, Logout_admin, Index, Register,
    patient_list, add_patient, discharge_patient,
    staff_list, add_staff
)

urlpatterns = [
    # Existing URLs
    path('', Home, name='home_root'),
    path('home/', Home, name='home'),
    path('about/', About, name='about'),
    path('services/', Services, name='services'),
    path('appointment/', Appointment, name='appointment'),
    path('login/', user_login, name='login'),
    path('logout/', Logout_admin, name='logout_admin'),
    path('admin_dashboard/', Index, name='index'),
    path('register/', Register, name='register'),

    # New Admin URLs
    path('admin/patients/', patient_list, name='patient_list'),
    path('admin/patients/add/', add_patient, name='add_patient'),
    path('admin/patients/discharge/<int:patient_id>/', discharge_patient, name='discharge_patient'),
    path('admin/staff/', staff_list, name='staff_list'),
    path('admin/staff/add/', add_staff, name='add_staff'),
]