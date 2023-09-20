from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from managment.decorators import *
from .models import ProductIndex, Master
from .forms import ProductIndexForm


# Create your views here.


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def home(request):
    username = request.user.username
    email = request.user.email
    sidebar = [
        {'text': 'Index New Product', 'url': '/creat_product_index'},
        {'text': 'List Index Product', 'url': '/product_index'},
        {'text': 'List Master', 'url': '/master'},
    ]

    context = {
        'username': username,
        'email': email,
        'sidebar': sidebar,
    }

    return render(request, 'inlet_home.html', context)


# Product Related
# @login_required(login_url='managment/login/')
# @allowed_users(['admins','inlet_user'])
# def product_list(requet):
#     return render

@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def create_product_index(request):
    if request.method == 'POST':
        form = ProductIndexForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('SUCCESS')
    else:
        form = ProductIndexForm()

    return render(request, 'create_product_index.html', {'form': form})

@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def list_product_index(request):
    product_indexes = ProductIndex.objects.all()
    return render(request, 'product_index_list.html', {'product_indexes': product_indexes})

@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user','managment_user'])
def list_masters(request):
    masters = Master.objects.all()
    return render(request, 'master_list.html', {'masters': masters})
