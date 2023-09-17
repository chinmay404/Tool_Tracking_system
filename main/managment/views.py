from django.shortcuts import render ,redirect ,HttpResponse
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm,CustomUserAuthenticationForm



# Create your views here.
@login_required
def user_check(request):
    username = request.user.username
    email = request.user.email

    context = {
        'username': username,
        'email': email,
    }

    return render(request, 'user_check.html', context)


def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('user_check')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomUserAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_check')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)




def logout_view(request):
    logout(request)
    return redirect('login') 