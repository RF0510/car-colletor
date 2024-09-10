from django.urls import path
# import Home view from the views file
from .views import Home, CarList, CarDetail 

urlpatterns = [
  path('', Home.as_view(), name='home'),
  # new routes below 
  path('cars/', CarList.as_view(), name='car-list'),
  path('cars/<int:id>/', CarDetail.as_view(), name='car-detail'),
]

