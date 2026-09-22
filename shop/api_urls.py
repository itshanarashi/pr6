from rest_framework.routers import DefaultRouter

from .api import (
    BrandViewSet,
    CategoryViewSet,
    CustomerViewSet,
    OrderItemViewSet,
    OrderViewSet,
    ProductViewSet,
    ReviewViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='api-category')
router.register('brands', BrandViewSet, basename='api-brand')
router.register('products', ProductViewSet, basename='api-product')
router.register('suppliers', SupplierViewSet, basename='api-supplier')
router.register('customers', CustomerViewSet, basename='api-customer')
router.register('orders', OrderViewSet, basename='api-order')
router.register('order-items', OrderItemViewSet, basename='api-order-item')
router.register('reviews', ReviewViewSet, basename='api-review')

urlpatterns = router.urls
