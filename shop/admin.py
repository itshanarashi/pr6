from django.contrib import admin
from .models import Brand, Category, Customer, Order, OrderItem, Product, Review, Supplier

admin.site.register([Category, Brand, Supplier, Customer, Product, Order, OrderItem, Review])
