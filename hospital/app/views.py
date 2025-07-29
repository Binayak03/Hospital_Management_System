from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

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

def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('index')  # Redirect on successful login
        else:
            error = "yes"  # Login failed

    return render(request, 'login.html', {'error': error})

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')

    logout(request)
    return redirect('login')

