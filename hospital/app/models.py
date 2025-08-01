from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Staff(models.Model):
    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
        ('Helper', 'Helper'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Patient(models.Model):
    BED_NUMBERS = [(i, f"Bed {i}") for i in range(1, 151)]  # 150 beds

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    bed_number = models.IntegerField(choices=BED_NUMBERS, unique=True)
    assigned_doctor = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,
                                        limit_choices_to={'role': 'Doctor'})
    admission_date = models.DateTimeField(auto_now_add=True)
    is_discharged = models.BooleanField(default=False)
    discharge_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Bed {self.bed_number})"

    def discharge(self):
        self.is_discharged = True
        self.discharge_date = timezone.now()
        self.save()


# Add to your existing models.py
# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Confirmed', 'Confirmed'),
#         ('Cancelled', 'Cancelled'),
#         ('Completed', 'Completed'),
#     ]
#
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'role': 'Doctor'})
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     symptoms = models.CharField(max_length=255)
#     appointment_date = models.DateField()
#     appointment_time = models.TimeField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     notes = models.TextField(blank=True)
#
#     def __str__(self):
#         return f"{self.patient.name} with Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"
#
#     class Meta:
#         ordering = ['-appointment_date', 'appointment_time']