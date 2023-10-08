from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from inlet.models import Master
from .serializers import ItemSerializer
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse ,get_object_or_404
from django.urls import reverse  # Import reverse to generate the URL
from rest_framework.renderers import TemplateHTMLRenderer

@api_view(['GET'])
def get_product(request, uuid):
    try:
        master = Master.objects.get(uuid=uuid)
        s = ItemSerializer(master)
        sd = s.data

        return render(request, 'get_product.html', {'data': sd})
    except Master.DoesNotExist:
        return Response({"message": "Master object not found"}, status=404)
    
    

# @api_view(['GET'])
def activate_product(request, uuid):
    try:
        master_product = get_object_or_404(Master, uuid=uuid)
        if request.user.has_perm('inlet.change_master'):
            if master_product.status == 'active':
                message = f'Product with UUID {uuid} is already active.'
            try:
                master_product.status = 'active'
                activator_name = request.user.username 
                activation_date = timezone.now()  
                activator_ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
                current_data = master_product.data_json or {}
                current_data['status'] = {
                    'activator_name': activator_name,
                    'activator_ip': activator_ip,
                    'activation_date': activation_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'status_changed_to': 'active',
                }
                master_product.data_json = current_data
                master_product.save()
                message = f'Product with UUID {uuid} has been activated.'
                return redirect('blank', {'message': message})
            except Exception as e:
                pass
        else:
            message = f'Error In Activation: UUID: {uuid}'
    except Master.DoesNotExist as e:
        message = f'Error In Activation: UUID: {uuid} \nError: {e}'
    
    # Redirect with the message
    return redirect('blank', {'message': message})
