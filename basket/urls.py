from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_detail, name='detail'),
    path('add/<int:product_id>/', views.basket_add, name='add'),
    path('remove/<int:product_id>/', views.basket_remove, name='remove'),
    path('clear/', views.basket_clear, name='clear'),
    path('order/', views.order_create, name='order_create'),
]
