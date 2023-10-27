from rest_framework import serializers
from inlet.models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
        
        
class ProductIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIndex
        fields = '__all__'