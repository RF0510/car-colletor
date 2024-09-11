from django.urls import path
# import Home view from the views file
from .views import Home, CarList, CarDetail, GasListCreate, GasDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # new routes below 
  path('cars/', CarList.as_view(), name='car-list'),
  path('cars/<int:id>/', CarDetail.as_view(), name='car-detail'),
  path('cars/<int:car_id>/gas/', GasListCreate.as_view(), name='gas-list-create'),
	path('cars/<int:car_id>/gas/<int:id>/', GasDetail.as_view(), name='gas-detail'),
]

