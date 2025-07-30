from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



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