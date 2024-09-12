from rest_framework import serializers
from .models import Car, Gas, Accessories


class AccessoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Accessories
    fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
  filled_up_today = serializers.SerializerMethodField()
  accessories = AccessoriesSerializer(many=True, read_only=True)
  class Meta:
        model = Car
        fields = '__all__'
        
  def get_filled_up_today(self, obj):
    return obj.filled_up_today()      
        
class GasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gas
        fields = '__all__'
        read_only_fields = ('car',)
        
class AccessoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Accessories
    fields = '__all__'