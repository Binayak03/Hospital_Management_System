from django.urls import path
from .views import (
    Home, About, Services, Appointment,
    admin_login, doctor_login, patient_login,
    Logout_admin, Index, Register,
    patient_list, add_patient, discharge_patient,
    staff_list, add_staff, doctor_dashboard
)

urlpatterns = [
    # Public URLs
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('services/', Services, name='services'),
    path('appointment/', Appointment, name='appointment'),

    # Authentication URLs
    path('admin/login/', admin_login, name='admin_login'),
    path('doctor/login/', doctor_login, name='doctor_login'),
    path('patient/login/', patient_login, name='patient_login'),
    path('logout/', Logout_admin, name='logout'),
    path('register/', Register, name='register'),

    # Dashboard URLs
    path('admin/dashboard/', Index, name='admin_dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),

    # Management URLs
    path('admin/patients/', patient_list, name='patient_list'),
    path('admin/patients/add/', add_patient, name='add_patient'),
    path('admin/patients/discharge/<int:patient_id>/', discharge_patient, name='discharge_patient'),
    path('admin/staff/', staff_list, name='staff_list'),
    path('admin/staff/add/', add_staff, name='add_staff'),
]