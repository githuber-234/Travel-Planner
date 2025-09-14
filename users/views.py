from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created!")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('full_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'users/profile.html')