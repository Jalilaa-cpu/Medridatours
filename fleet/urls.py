from django.urls import path
from . import views

app_name = 'fleet'

urlpatterns = [
    path('', views.fleet_list, name='fleet_list'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
]
