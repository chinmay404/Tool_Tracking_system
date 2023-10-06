from rest_framework import serializers
from inlet.models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'