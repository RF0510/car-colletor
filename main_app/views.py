from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Car, Gas, Accessories
from .serializers import CarSerializer, GasSerializer, AccessoriesSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied 

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the car-collector api home route!'}
    return Response(content)

class CarList(generics.ListCreateAPIView):
  serializer_class = CarSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return cars belonging to the logged-in user
      user = self.request.user
      return Car.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created car with the logged-in user
      serializer.save(user=self.request.user)


class CarDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = CarSerializer
  lookup_field = 'id'
  
  def get_queryset(self):
    user = self.request.user
    return Car.objects.filter(user=user)
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    
    accessories_not_associated = Accessories.objects.exclude(id__in=instance.accessories.all())
    accessories_serializer = AccessoriesSerializer(accessories_not_associated, many=True)
    
    return Response({
        'car': serializer.data,
        'accessories_not_associated': accessories_serializer.data
    })
    
  def perform_update(self, serializer):
    car = self.get_object()
    if car.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this car."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this car."})
    instance.delete()
  
class GasListCreate(generics.ListCreateAPIView):
  serializer_class = GasSerializer

  def get_queryset(self):
    car_id = self.kwargs['car_id']
    return Gas.objects.filter(car_id=car_id)

  def perform_create(self, serializer):
    car_id = self.kwargs['car_id']
    car = Car.objects.get(id=car_id)
    serializer.save(car=car)  
    
class GasDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = GasSerializer
  lookup_field = 'id'

  def get_queryset(self):
    car_id = self.kwargs['car_id']
    return Gas.objects.filter(car_id=car_id)
  
class AccessoriesList(generics.ListCreateAPIView):
  queryset = Accessories.objects.all()
  serializer_class = AccessoriesSerializer

class AccessoriesDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Accessories.objects.all()
  serializer_class = AccessoriesSerializer
  lookup_field = 'id'
  
class AddAccessoriesToCar(APIView):
  def post(self, request, car_id, accessories_id):
    car = Car.objects.get(id=car_id)
    accessories = Accessories.objects.get(id=accessories_id)
    car.accessories.add(accessories)
    return Response({'message': f'Accessories {accessories.name} added to Car {car.name}'})
  
class RemoveAccessoriesFromCar(APIView):
  def post(self, request, car_id, accessories_id):
    car = Car.objects.get(id=car_id)
    accessories = Accessories.objects.get(id=accessories_id)
    car.accessories.remove(accessories)
    return Response({'message': f'Accessories {accessories.name} removed from Car {car.name}'})
  
# include the registration, login, and verification views below
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })