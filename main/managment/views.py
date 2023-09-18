from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from .decorators import unauth_user, allowed_users
from django.urls import reverse
from django.contrib.auth.models import Group


@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'managment_user',])
def home(request):
    username = request.user.username
    email = request.user.email
    sidebar = [
        {'text': 'Dashboard_managment', 'url': '/dashboard/'},
        {'text': 'Profile_managmnet', 'url': '/profile/'},
    ]

    context = {
        'username': username,
        'email': email,
        'sidebar': sidebar,
    }

    return render(request, 'home.html', context)


@unauth_user  # IF User is Already Logged in no need to go for login page again
def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            # REDIRECTING USERS ACCORDING TO THEIR GROUPS
            if user.groups.exists():
                group = user.groups.all()[0].name
            if group == 'admins' or group == 'managment_user':
                return redirect('home')
            elif group == 'inlet_user':
                return redirect(reverse('inlet:home'))
            else:
                return redirect('wating_feild')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


@unauth_user
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Replace with your group name
            group = Group.objects.get(name='pending_user')
            user.groups.add(group)
            login(request, user)
            return redirect('user_check')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


@login_required(login_url='managment/login/')
def logout_view(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['admins'])
def admin_only(request):
    return redirect('admin:index')





@login_required(login_url='managment/login/')
def wating_feild(request):
    return render(request,'wating_feild.html')