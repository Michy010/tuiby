from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
from django.contrib import messages

# Create your views here.
def registerView(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Creating the User instance and save them to the database
            user = CustomUser.objects.create_user(
                full_name=full_name,
                email=email,
                password=password
            )
            return redirect('accounts:login')
        except IntegrityError:
            messages.error(request, 'The email provided is already existing')

    return render (request, 'main/for_seller.html')

def loginView(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:seller-panel')
        else:
            error = 'Invalid Username or Password'
    return render (request, 'accounts/login.html', {'error':error})

def logoutView(request):
    logout(request)
    return redirect('main:home')