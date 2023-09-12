from rest_framework import serializers
from .models import Menu
  
# Create a model serializer 
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields ='__all__'