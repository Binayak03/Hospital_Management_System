from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Staff, Department, Appointment
from .forms import PatientForm, StaffForm, AppointmentForm

# Public Views
def Home(request):
    return render(request, 'home.html')

def About(request):
    # Your existing implementation
    departments = Department.objects.all()
    doctors = Staff.objects.filter(role='Doctor')
    return render(request, 'about.html', {
        'departments': departments,
        'doctors': doctors
    })

def Services(request):
    return render(request, 'services.html')

def Appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})

# Authentication Views
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid admin credentials')
    return render(request, 'registration/admin_login.html')

def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'staff_profile') and user.staff_profile.role == 'Doctor':
            login(request, user)
            return redirect('doctor_dashboard')
        messages.error(request, 'Invalid doctor credentials')
    return render(request, 'registration/doctor_login.html')

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not hasattr(user, 'staff_profile'):
            login(request, user)
            return redirect('home')
        messages.error(request, 'Invalid patient credentials')
    return render(request, 'registration/patient_login.html')

def Logout_admin(request):
    logout(request)
    return redirect('home')

def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Dashboard Views
@login_required
def Index(request):
    if not request.user.is_staff:
        return redirect('home')
    return render(request, 'admin/index.html')

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'staff_profile') or request.user.staff_profile.role != 'Doctor':
        return redirect('home')
    appointments = Appointment.objects.filter(doctor=request.user.staff_profile)
    return render(request, 'doctor/dashboard.html', {'appointments': appointments})

# Management Views
@login_required
def patient_list(request):
    if not request.user.is_staff:
        return redirect('home')
    patients = Patient.objects.filter(is_discharged=False)
    return render(request, 'admin/patient_list.html', {'patients': patients})

@login_required
def add_patient(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'admin/add_patient.html', {'form': form})

@login_required
def discharge_patient(request, patient_id):
    if not request.user.is_staff:
        return redirect('home')
    patient = get_object_or_404(Patient, id=patient_id)
    patient.discharge()
    return redirect('patient_list')

@login_required
def staff_list(request):
    if not request.user.is_staff:
        return redirect('home')
    staff_members = Staff.objects.all()
    return render(request, 'admin/staff_list.html', {'staff_members': staff_members})

@login_required
def add_staff(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'admin/add_staff.html', {'form': form})