from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from inlet.models import Master
from .serializers import ItemSerializer
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse ,get_object_or_404
from django.urls import reverse 
from rest_framework.renderers import TemplateHTMLRenderer
from inlet.models import ProductIndex
from django.contrib.auth.decorators import login_required
from managment.decorators import *
from datetime import datetime, timedelta
from .forms import ActivationForm
from rest_framework import status
from rest_framework.views import APIView









@login_required(login_url='managment/login/')
@api_view(['GET'])
def get_product(request, uuid):
    try:
        master = Master.objects.get(uuid=uuid)
        s = ItemSerializer(master)
        sd = s.data

        return render(request, 'get_product.html', {'data': sd})
    except Master.DoesNotExist:
        return Response({"message": "Master object not found"}, status=404)
    
    

@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def activate_product(request, old_uuid, new_uuid):
    try:
        # Check if the new UUID is unique (not used before)
        if Master.objects.filter(uuid=new_uuid).exists():
            message = f'UUID {new_uuid} is already in use. Please choose a different UUID.'
        else:
            master_product = get_object_or_404(Master, uuid=old_uuid)
            if request.user.has_perm('inlet.change_master'):
                if master_product.status == 'active':
                    message = f'Product with UUID {new_uuid} is already active.'
                else:
                    activator_name = request.user.username
                    activation_date = timezone.now()
                    activator_ip = request.META.get('REMOTE_ADDR', 'Unknown IP')

                    # Create a new Master with the same attributes as the old one
                    new_master = Master(
                        product=master_product.product,
                        uuid=new_uuid,
                        batch_id=master_product.batch_id,
                        status='active',
                        added_date=master_product.added_date,
                        received_by=master_product.received_by,
                        data_json=master_product.data_json
                    )
                    
                    # Add activator information to the data_json field of the new master
                    new_data = {
                        'activator_name': activator_name,
                        'activator_ip': activator_ip,
                        'activation_date': activation_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'status_changed_to': 'active'
                    }
                    if 'status' not in new_master.data_json:
                        new_master.data_json['status'] = new_data
                    else:
                        new_master.data_json['status'].update(new_data)

                    new_master.save()
                    master_product.delete()

                    message = f'Product with UUID {new_uuid} has been activated.'
                    return HttpResponse(message)
            else:
                message = f'Error In Activation: UUID: {new_uuid}'
    except Master.DoesNotExist as e:
        message = f'Error In Activation: UUID: {new_uuid}\nError: {e}'
        return HttpResponse('Not Activated')



@login_required(login_url='managment/login/')
@allowed_users(['admins', 'inlet_user'])
def api_home(request):

    all_batches = ProductIndex.objects.all()
    filter_date = request.GET.get('filter_date')
    search_query = request.GET.get('search_query')

    if filter_date:
        all_batches = all_batches.filter(arrive_date__date=filter_date)

    if search_query:
        all_batches = all_batches.filter(
            models.Q(batch_id__icontains=search_query) |
            models.Q(product__name__icontains=search_query)
        )

    context = {
        'all_batches': all_batches,
        'filter_date': filter_date,
        'search_query': search_query,
    }
    return render(request, 'api_home.html', context)




def batch_detail(request, batch_id):
    masters = Master.objects.filter(batch_id=batch_id)

    context = {
        'batch_id': batch_id,
        'masters': masters,
    }

    return render(request, 'batch_detail.html', context)





def activate_master(request, uuid):
    if request.method == 'POST':
        form = ActivationForm(request.POST)
        if form.is_valid():
            new_id = form.cleaned_data['id']
            old_id = uuid
            # Call the 'activate_product' view function and pass the arguments
            return activate_product(request, old_uuid=old_id, new_uuid=new_id)
    else:
        form = ActivationForm()

    return render(request, 'activate_master.html', {'form': form})






# OUTLET APIS

class CreateOrder(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)