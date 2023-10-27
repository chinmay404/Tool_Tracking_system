from django.shortcuts import render, redirect, HttpResponse ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserAuthenticationForm
from .decorators import unauth_user, allowed_users
from django.contrib.auth.models import Group
from inlet.models import Master,ProductIndex,Product
from django.db.models import Q
from django.db.models import Count, Case, When, IntegerField





@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'managment_user',])
def home(request):
    activated_product_index = ProductIndex.objects.filter(status='active')
    products = Product.objects.all()
    
    context = {
        'activated_product_index':activated_product_index,
        'products': products,
    }

    return render(request, 'managment_home.html', context)



@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'managment_user',])
def inventory_detail(request, product_id):
    masters = Master.objects.filter(product__product_id=product_id)
    masters_count = masters.count()
    product = Product.objects.filter(product_id=product_id)
    
    
    
    context = {
        'masters': masters,
        'masters_count': masters_count,
        'product':product
    }
    return render(request, 'inventory_detail.html', context)





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
            if group == 'admins' or group == 'managment_user' or user.username =='admin':
                return redirect('managment_home')
            elif group == 'inlet_user':
                return redirect(('inlet_home'))
            elif group == 'activators':
                return redirect('list_batch')
            elif  group == 'outlet_user':
                return redirect('outlet_home')
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
            group = Group.objects.get(name='wait_list')
            user.groups.add(group)
            login(request, user)
            return redirect('wating_feild')
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


@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'managment_user'])
def inquiry(request):
    search_results = None

    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            fields_to_search = ['uuid', 'batch_id', 'product__name', 'status', 'added_date', 'received_by__username','status']
            queries = [Q(**{f'{field}__icontains': query}) for field in fields_to_search]
            search_query = Q()
            for query in queries:
                search_query |= query

            search_results = Master.objects.filter(search_query)

    return render(request, 'inquiry.html', {'search_results': search_results})




@login_required(login_url='managment/login/')
@allowed_users(allowed_roles=['admins', 'managment_user','activators'])
def list_batch(request):
    product_indexes = ProductIndex.objects.all().order_by('-arrive_date')

    context = {
        'product_indexes': product_indexes
    }

    return render(request, 'list_batch.html', context)




