from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Car, Gas, Accessories
from .serializers import CarSerializer, GasSerializer, AccessoriesSerializer


# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the car-collector api home route!'}
    return Response(content)

class CarList(generics.ListCreateAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer

class CarDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Car.objects.all()
  serializer_class = CarSerializer
  lookup_field = 'id'
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    
    accessories_not_associated = Accessories.objects.exclude(id__in=instance.accessories.all())
    accessories_serializer = AccessoriesSerializer(accessories_not_associated, many=True)
    
    return Response({
        'car': serializer.data,
        'accessories_not_associated': accessories_serializer.data
    })
  
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