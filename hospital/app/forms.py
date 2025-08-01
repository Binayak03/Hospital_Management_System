from django import forms
from .models import Patient, Staff

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'contact', 'bed_number', 'assigned_doctor']
        widgets = {
            'bed_number': forms.Select(choices=Patient.BED_NUMBERS),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'role', 'department', 'phone']