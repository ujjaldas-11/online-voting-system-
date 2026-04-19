from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages



def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password2 != password1:      
            messages.error(request, "password do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "username already taken")
        elif len(password1) < 4:
            messages.error(request, "Passowrd must be atleast 4 characters.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            # login(request, user)
            messages.success(request, "user registered sucessfully.")
            return redirect('login')
    return render(request, 'accounts/register.html')



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        else:
            messages.error(request, "Invalid Credeantials.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')