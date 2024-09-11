from rest_framework import serializers
from .models import Car, Gas, Accessories


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        
class GasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gas
        fields = '__all__'
        read_only_fields = ('car',)
        
class AccessoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Accessories
    fields = '__all__'