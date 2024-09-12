from django.urls import path
# import Home view from the views file
from .views import Home, CarList, CarDetail, GasListCreate, GasDetail, AccessoriesList, AccessoriesDetail, AddAccessoriesToCar, RemoveAccessoriesFromCar

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # new routes below 
  path('cars/', CarList.as_view(), name='car-list'),
  path('cars/<int:id>/', CarDetail.as_view(), name='car-detail'),
  path('cars/<int:car_id>/gas/', GasListCreate.as_view(), name='gas-list-create'),
	path('cars/<int:car_id>/gas/<int:id>/', GasDetail.as_view(), name='gas-detail'),
  path('accessories/', AccessoriesList.as_view(), name='accessories-list'),
  path('accessories/<int:id>/', AccessoriesDetail.as_view(), name='accessories-detail'),
  path('cars/<int:car_id>/add_accessories/<int:accessories_id>/', AddAccessoriesToCar.as_view(), name='add-accessories-to-cat'),
  path('cars/<int:car_id>/remove_accessories/<int:accessories_id>/', RemoveAccessoriesFromCar.as_view(), name='remove-accessories-from-car'),
]

