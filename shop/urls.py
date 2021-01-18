from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/<str:pk>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('order_info/', views.orderInfo, name='order_info'),
    path('update_item/', views.updateItem, name='update_item'),
    path('send_order/', views.sendOrder, name='send_order'),
]
