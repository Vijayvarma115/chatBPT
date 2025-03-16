from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import UserPreferences

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            if not User.objects.filter(username=username).exists():
                error_message = 'User does not exist'
            else:
                error_message = 'Invalid credentials'
    return render(request, 'users/login.html', {'error': error_message})

@login_required
def user_preferences(request):
    preferences, created = UserPreferences.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        preferences.theme = theme
        preferences.save()
        
        # Set the theme cookie
        response = redirect('user_preferences')
        response.set_cookie('theme', theme, max_age=30*24*60*60)  # Cookie expires in 30 days
        return response
    return render(request, 'core/user_preferences.html', {'preferences': preferences})