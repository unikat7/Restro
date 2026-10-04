from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('', views.reservation_create, name='reservation_create'),
    path('done/', views.reservation_done, name='reservation_done'),
]
