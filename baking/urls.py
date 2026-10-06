from django.urls import path
from . import views

app_name = 'baking'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('custom-order/', views.custom_order, name='custom_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]