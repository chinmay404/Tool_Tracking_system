from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from managment.decorators import *
from .models import ProductIndex, Master,Product
from .forms import ProductIndexForm
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import csv
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator

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
    product_indexes = ProductIndex.objects.all().order_by('-arrive_date')

    context = {
        'username': username,
        'email': email,
        'sidebar': sidebar,
        'product_indexes': product_indexes
        
    }

    return render(request, 'inlet_home.html', context)


@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def create_product_index(request):
    if request.method == 'POST':
        try:
            form = ProductIndexForm(request.POST)
            if form.is_valid():
                received_by = request.user
                form.instance.received_by = received_by 
                form.save()
            return redirect('inlet_home')
        except Exception as E:
            print("ERRORRRRRRRRRRRR : ",E)
            pass
        
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
    masters = Master.objects.all().order_by('-added_date') 
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
@allowed_users(['admins', 'inlet_user', 'managment_user','activators'])
def product_batch(request, batch_id):
    products = Master.objects.filter(batch_id=batch_id)
    context = {
        'products': products,
        'batch_id_info': batch_id,  
    }
    return render(request, 'product_batch.html', context)



@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user','activators'])
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
@allowed_users(['admins', 'inlet_user', 'managment_user','activators'])
def download_id(request, master_id):

    try:
        product = Master.objects.get(uuid=id)
        products = [product]
        response['Content-Disposition'] = f'attachment; filename="unique_id_{id}.csv"'
    except Master.DoesNotExist:
            messages.error(request, 'Invalid ID. Product not found.')
    writer = csv.writer(response)
    writer.writerow(['Unique ID'])
    for product in products:
        writer.writerow([product.uuid])
    return response




@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user' ,'activators'])
def activation(request):
    if request.method == 'POST':
        uuid_to_activate = request.POST.get('uuid_to_activate').replace(" ", "")
        try:
            master_product = Master.objects.get(uuid=uuid_to_activate)
            if request.user.has_perm('inlet.change_master'):
                try:
                    master_product.status = 'active'
                    activator_name = request.user.username 
                    activation_date = timezone.now()  
                    current_data = master_product.data_json or {}
                    current_data['status'] = {
                        'activator_name': activator_name,
                        'activation_date': activation_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'status_changed_to': 'active',
                    }
                    master_product.data_json = current_data
                    master_product.save()
                    messages.success(request, 'Product activated successfully.')
                except Exception as e:
                    pass
            else:
                messages.error(request, 'You are not authorized to activate this product.')
        except Master.DoesNotExist:
            messages.error(request, 'Invalid UUID. Product not found.')

    return render(request, 'activation.html')




@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user', 'managment_user','activators'])
def view_master(request, product_id):
    product = get_object_or_404(Master, uuid=product_id)
    context = {
        'product': product,
    }
    return render(request, 'view_product.html', context)