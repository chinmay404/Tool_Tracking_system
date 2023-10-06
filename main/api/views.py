from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from inlet.models import Master
from .serializers import ItemSerializer
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse ,get_object_or_404
@api_view(['GET'])
def get_product(request, uuid):
    try:
        master = Master.objects.get(uuid=uuid)
        s = ItemSerializer(master)
        
        return Response(s.data)
    except Master.DoesNotExist:
        return Response({"message": "Master object not found"}, status=404)
    
    

@api_view(['GET'])
def activate_product(request, uuid):
    try:
        master_product = get_object_or_404(Master, uuid=uuid)
        if request.user.has_perm('inlet.change_master'):
            if master_product.status == 'active':
                return Response({'message': f'Product with UUID {uuid} is already active.'})
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
                return Response({'message': f'Product with UUID {uuid} has been activated.'})
            except Exception as e:
                pass
        else:
            return Response({'message': f'Error In Activation: UUID: {uuid}'})
    except Master.DoesNotExist as e:
        return Response({'message': f'Error In Activation: UUID: {uuid} \nError: {e}'})