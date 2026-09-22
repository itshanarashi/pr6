from rest_framework import filters, viewsets

from .models import Brand, Category, Customer, Order, OrderItem, Product, Review, Supplier
from .pagination import ApiPagination
from .permissions import ApiAccessPermission
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    CustomerSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductSerializer,
    ReviewSerializer,
    SupplierSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [ApiAccessPermission]
    pagination_class = ApiPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering = ['id']


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name', 'description']
    ordering_fields = ['id', 'name', 'created_at']


class BrandViewSet(BaseViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    search_fields = ['name', 'country', 'description']
    ordering_fields = ['id', 'name', 'country']


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    search_fields = ['name', 'contact_person', 'phone', 'email', 'address']
    ordering_fields = ['id', 'name', 'email']


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ['full_name', 'phone', 'email', 'address']
    ordering_fields = ['id', 'full_name', 'registered_at']


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.select_related('category', 'brand', 'supplier').all()
    serializer_class = ProductSerializer
    search_fields = ['name', 'description', 'category__name', 'brand__name', 'supplier__name']
    ordering_fields = ['id', 'name', 'price', 'stock', 'created_at']


class OrderViewSet(BaseViewSet):
    queryset = Order.objects.select_related('customer').all()
    serializer_class = OrderSerializer
    search_fields = ['customer__full_name', 'status']
    ordering_fields = ['id', 'created_at', 'status', 'total_amount']


class OrderItemViewSet(BaseViewSet):
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer
    search_fields = ['product__name']
    ordering_fields = ['id', 'order', 'quantity', 'price']


class ReviewViewSet(BaseViewSet):
    queryset = Review.objects.select_related('product', 'customer').all()
    serializer_class = ReviewSerializer
    search_fields = ['product__name', 'customer__full_name', 'text']
    ordering_fields = ['id', 'rating', 'created_at']
