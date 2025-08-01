# from django import forms
# from .models import Patient, Staff
#
# class PatientForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['name', 'age', 'contact', 'bed_number', 'assigned_doctor']
#         widgets = {
#             'bed_number': forms.Select(choices=Patient.BED_NUMBERS),
#         }
#
# class StaffForm(forms.ModelForm):
#     class Meta:
#         model = Staff
#         fields = ['user', 'role', 'department', 'phone']

from django import forms
from .models import Patient, Staff, Appointment, Department
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'contact', 'bed_number', 'assigned_doctor']
        widgets = {
            'bed_number': forms.Select(attrs={'class': 'form-control'}),
            'assigned_doctor': forms.Select(attrs={'class': 'form-control'}),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['role', 'department', 'phone', 'specialization']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'department', 'symptoms', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']