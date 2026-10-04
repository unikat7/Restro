from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.order_create, name='order_create'),
    path('payment/esewa/success/', views.esewa_success, name='esewa_success'),
    path('payment/esewa/failure/', views.esewa_failure, name='esewa_failure'),
    path('created/<int:order_id>/', views.order_created, name='order_created'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
