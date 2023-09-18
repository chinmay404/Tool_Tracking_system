from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from managment.decorators import *

# Create your views here.


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def home(request):
    username = request.user.username
    email = request.user.email
    sidebar = [
        {'text': 'Dashboard_inlet', 'url': '/dashboard/'},
        {'text': 'Profile_inlet', 'url': '/profile/'},
    ]

    context = {
        'username': username,
        'email': email,
        'sidebar': sidebar,
    }

    return render(request, 'home.html', context)


# Product Related
# @login_required(login_url='managment/login/')
# @allowed_users(['admins','inlet_user'])
# def product_list(requet):
#     return render
