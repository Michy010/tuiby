from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def registerView(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect ('accounts:login')
    else:
        register_form = UserRegisterForm()
        
    return render (request, 'accounts/register.html', {'register_form':register_form})

def loginView(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:seller')
        else:
            error = 'Invalid Username or Password'
    return render (request, 'accounts/login.html', {'error':error})

def logoutView(request):
    return render (request, 'accounts/logout.html')