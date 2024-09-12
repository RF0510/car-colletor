from rest_framework import serializers
from .models import Car, Gas, Accessories
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class AccessoriesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Accessories
    fields = '__all__'

class CarSerializer(serializers.ModelSerializer):
  filled_up_today = serializers.SerializerMethodField()
  accessories = AccessoriesSerializer(many=True, read_only=True)
  user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make the user field read-only
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