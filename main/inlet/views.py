from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managment.decorators import *
from .models import ProductIndex, Master,Product
from .forms import ProductIndexForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import csv

# Create your views here.


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def home(request):
    username = request.user.username
    email = request.user.email
    sidebar = [
        {'url': 'create_product_index', 'text': 'Index New Product'},
        {'url': 'list_masters', 'text': 'List Master'},
    ]
    product_indexes = ProductIndex.objects.all()

    context = {
        'username': username,
        'email': email,
        'sidebar': sidebar,
        'product_indexes': product_indexes
        
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
            received_by = request.user
            form.instance.received_by = received_by 
            form.save()
            return redirect('inlet_home')
    else:
        form = ProductIndexForm()

    return render(request, 'create_product_index.html', {'form': form})


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def list_product_index(request):
    product_indexes = ProductIndex.objects.all()
    return render(request, 'product_index_list.html', {'product_indexes': product_indexes})


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user'])
def list_masters(request):
    masters = Master.objects.all()
    return render(request, 'master_list.html', {'masters': masters})




@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user'])
def product_specification(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_indexes = ProductIndex.objects.filter(product=product)
    context = {
        'product': product,
        'product_indexes': product_indexes,
        # Add other specification data to the context as needed
    }
    
    return render(request, 'product_specification.html', context)


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user'])
def product_quantity(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_indexes = ProductIndex.objects.filter(product=product)
    
    context = {
        'product': product,
        'product_indexes': product_indexes,
    }
    
    return render(request, 'product_quantity.html', context)



@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user'])
def product_batch(request, batch_id):
    products = Master.objects.filter(batch_id=batch_id)
    context = {
        'products': products,
        'batch_id_info': batch_id,  
    }
    return render(request, 'product_batch.html', context)



@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user'])
def download_ids(request, batch_id):

    products = Master.objects.filter(batch_id=batch_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="unique_ids_batch_{batch_id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Unique ID'])
    for product in products:
        writer.writerow([product.uuid])
    return response




@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def activation(request):
    
    pass