from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Patient, Staff
from .forms import PatientForm, StaffForm
from django.core.paginator import Paginator


def Home(request):
    return render(request, 'home.html')

def About(request):
    Departments = [
        {'name': 'Cardiology'},
        {'name': 'Neurology'},
        {'name': 'Pediatrics'},
        {'name': 'Orthopedics'},
        {'name': 'Gynecology'},
        {'name': 'Opthalology'}
    ]

    Doctors = [
        {
            'name': 'Prof. Dr. Bin Bhattarai',
            'dept': 'Cardiology',
            'email': 'binbhattarai@binayakhospital.com',
            'img': 'Doctor1.jpg'
        },
        {
            'name': 'Prof. Dr. Hari Sharma ',
            'dept': 'Neurology',
            'email': 'hari@binayakhospital.com',
            'img': 'Doctor8.jpg'
        },
        {
            'name': 'Prof. Dr. Arjun Mahadev',
            'dept': 'Ophthalmology',
            'email': 'arjun@binayakhospital.com',
            'img': 'Doctor3.jpg'
        },
        {
            'name': 'Prof. Dr. Madhav Shree',
            'dept': 'Orthopedic',
            'email': 'Mahadav@binayakhospital.com',
            'img': 'Doctor2.jpg'
        },
        {
            'name': 'Prof. Dr. Anjana Sharma',
            'dept': "Women's Gynecology",
            'email': 'anjana@binayakhospital.com',
            'img': 'img.png'
        },
        {
            'name': 'Prof. Dr. Ganesh Bhattarai',
            'dept': 'Child Care',
            'email': 'ganesh@binayakhospital.com',
            'img': 'Doctor6.JPG'
        },
    ]

    return render(request, 'about.html', {
        'departments': Departments,
        'doctors': Doctors
    })

def Services(request):
    return render(request, 'services.html')

def Appointment(request):
    return render(request, 'appointment.html')


def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'index.html')


def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            # Only set is_staff=True for actual admin users
            # Or remove this line to default to False
            user.save()

            # Authenticate and login the user
            authenticated_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if authenticated_user:
                auth_login(request, authenticated_user)
                messages.success(request, "Registration successful! You are now logged in.")
                return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration.html', {'form': form})


def user_login(request):  # Renamed from 'login' to avoid conflict
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)  # Use the renamed import
                messages.success(request, "Logged in successfully!")
                if user.is_staff:
                    return redirect('index')  # Staff go to admin dashboard
                return redirect('home')  # Regular users go to home
            else:
                messages.error(request, "Account is not active")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def Logout_admin(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')  # Redirect to home after logout


@login_required
def patient_list(request):
    if not request.user.is_staff:
        return redirect('login')

    patients = Patient.objects.filter(is_discharged=False).select_related('assigned_doctor')
    total_beds = 150
    occupied_beds = patients.count()
    available_beds = total_beds - occupied_beds

    context = {
        'patients': patients,
        'total_beds': total_beds,
        'occupied_beds': occupied_beds,
        'available_beds': available_beds,
        'bed_status': f"{occupied_beds}/{total_beds} beds occupied",
    }
    return render(request, 'admin/patient_list.html', context)


@login_required
def add_patient(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            # Check if bed is already occupied
            bed_number = form.cleaned_data['bed_number']
            if Patient.objects.filter(bed_number=bed_number, is_discharged=False).exists():
                messages.error(request, f"Bed {bed_number} is already occupied!")
                return render(request, 'admin/add_patient.html', {'form': form})

            form.save()
            messages.success(request, "Patient added successfully!")
            return redirect('patient_list')
    else:
        form = PatientForm()

    # Get available beds
    occupied_beds = Patient.objects.filter(is_discharged=False).values_list('bed_number', flat=True)
    available_beds = [bed for bed in range(1, 151) if bed not in occupied_beds]

    return render(request, 'admin/add_patient.html', {
        'form': form,
        'available_beds': available_beds,
    })


@login_required
def discharge_patient(request, patient_id):
    if not request.user.is_staff:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)
    if not patient.is_discharged:
        patient.discharge()
        messages.success(request, f"Patient {patient.name} discharged from Bed {patient.bed_number}")
    else:
        messages.warning(request, "Patient was already discharged")

    return redirect('patient_list')

@login_required
def staff_list(request):
    if not request.user.is_staff:
        return redirect('login')

    staff_members = Staff.objects.select_related('department').all()
    return render(request, 'admin/staff_list.html', {
        'staff_members': staff_members,
        'roles': Staff.ROLE_CHOICES,
    })


@login_required
def add_staff(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            # Check if user is already assigned as staff
            user = form.cleaned_data['user']
            if Staff.objects.filter(user=user).exists():
                messages.error(request, "This user is already assigned as staff")
                return render(request, 'admin/add_staff.html', {'form': form})

            form.save()
            messages.success(request, "Staff member added successfully!")
            return redirect('staff_list')
    else:
        form = StaffForm()

    # Get users not already assigned as staff
    staff_users = Staff.objects.values_list('user_id', flat=True)
    available_users = User.objects.exclude(id__in=staff_users)

    return render(request, 'admin/add_staff.html', {
        'form': form,
        'available_users': available_users,
    })


@login_required
def patient_list(request):
    if not request.user.is_staff:
        return redirect('login')

    patient_list = Patient.objects.filter(is_discharged=False).select_related('assigned_doctor')
    paginator = Paginator(patient_list, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_beds = 150
    occupied_beds = patient_list.count()
    available_beds = total_beds - occupied_beds

    context = {
        'patients': page_obj,
        'page_obj': page_obj,
        'total_beds': total_beds,
        'occupied_beds': occupied_beds,
        'available_beds': available_beds,
    }
    return render(request, 'admin/patient_list.html', context)