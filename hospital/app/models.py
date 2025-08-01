from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
        ('Helper', 'Helper'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='staff_members')
    phone = models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=100, blank=True)  # For doctors only

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Patient(models.Model):
    BED_NUMBERS = [(i, f"Bed {i}") for i in range(1, 151)]  # 150 beds

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    bed_number = models.IntegerField(choices=BED_NUMBERS, unique=True, blank=True, null=True)  # Make optional
    assigned_doctor = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'Doctor'},
        related_name='assigned_patients'
    )

# In models.py
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'Doctor'})
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    symptoms = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.user.get_full_name()} - {self.appointment_date}"