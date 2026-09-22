from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Brand, Category, Customer, Order, Product, Review, Supplier


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff



def home(request):
    featured = Product.objects.select_related('category', 'brand').all()[:3]
    return render(request, 'shop/home.html', {'featured': featured})

def about(request): return render(request, 'shop/about.html')
def contacts(request): return render(request, 'shop/contacts.html')
def location(request): return render(request, 'shop/location.html')
def delivery(request): return render(request, 'shop/delivery.html')
def warranty(request): return render(request, 'shop/warranty.html')


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(StaffRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:category_list')
    extra_context = {'page_title': 'Добавление категории', 'cancel_url': reverse_lazy('shop:category_list')}

class CategoryUpdateView(StaffRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:category_list')
    extra_context = {'page_title': 'Изменение категории', 'cancel_url': reverse_lazy('shop:category_list')}

class CategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'shop/object_confirm_delete.html'
    success_url = reverse_lazy('shop:category_list')
    extra_context = {'page_title': 'Удаление категории', 'cancel_url': reverse_lazy('shop:category_list')}


class BrandListView(ListView):
    model = Brand
    template_name = 'shop/brand_list.html'
    context_object_name = 'brands'

class BrandDetailView(DetailView):
    model = Brand
    template_name = 'shop/brand_detail.html'
    context_object_name = 'brand'

class BrandCreateView(StaffRequiredMixin, CreateView):
    model = Brand
    fields = ['name', 'country', 'website', 'description', 'logo']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:brand_list')
    extra_context = {'page_title': 'Добавление бренда', 'cancel_url': reverse_lazy('shop:brand_list')}

class BrandUpdateView(StaffRequiredMixin, UpdateView):
    model = Brand
    fields = ['name', 'country', 'website', 'description', 'logo']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:brand_list')
    extra_context = {'page_title': 'Изменение бренда', 'cancel_url': reverse_lazy('shop:brand_list')}

class BrandDeleteView(StaffRequiredMixin, DeleteView):
    model = Brand
    template_name = 'shop/object_confirm_delete.html'
    success_url = reverse_lazy('shop:brand_list')
    extra_context = {'page_title': 'Удаление бренда', 'cancel_url': reverse_lazy('shop:brand_list')}


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.select_related('category', 'brand', 'supplier')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'brand', 'supplier', 'price', 'stock', 'description', 'image']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:product_list')
    extra_context = {'page_title': 'Добавление товара', 'cancel_url': reverse_lazy('shop:product_list')}

class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'brand', 'supplier', 'price', 'stock', 'description', 'image']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:product_list')
    extra_context = {'page_title': 'Изменение товара', 'cancel_url': reverse_lazy('shop:product_list')}

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'shop/object_confirm_delete.html'
    success_url = reverse_lazy('shop:product_list')
    extra_context = {'page_title': 'Удаление товара', 'cancel_url': reverse_lazy('shop:product_list')}


class SupplierListView(ListView):
    model = Supplier
    template_name = 'shop/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'shop/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(StaffRequiredMixin, CreateView):
    model = Supplier
    fields = ['name', 'contact_person', 'phone', 'email', 'address']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:supplier_list')
    extra_context = {'page_title': 'Добавление поставщика', 'cancel_url': reverse_lazy('shop:supplier_list')}

class SupplierUpdateView(StaffRequiredMixin, UpdateView):
    model = Supplier
    fields = ['name', 'contact_person', 'phone', 'email', 'address']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:supplier_list')
    extra_context = {'page_title': 'Изменение поставщика', 'cancel_url': reverse_lazy('shop:supplier_list')}

class SupplierDeleteView(StaffRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'shop/object_confirm_delete.html'
    success_url = reverse_lazy('shop:supplier_list')
    extra_context = {'page_title': 'Удаление поставщика', 'cancel_url': reverse_lazy('shop:supplier_list')}


class CustomerListView(ListView):
    model = Customer
    template_name = 'shop/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'shop/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(StaffRequiredMixin, CreateView):
    model = Customer
    fields = ['full_name', 'phone', 'email', 'address']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:customer_list')
    extra_context = {'page_title': 'Добавление покупателя', 'cancel_url': reverse_lazy('shop:customer_list')}

class CustomerUpdateView(StaffRequiredMixin, UpdateView):
    model = Customer
    fields = ['full_name', 'phone', 'email', 'address']
    template_name = 'shop/object_form.html'
    success_url = reverse_lazy('shop:customer_list')
    extra_context = {'page_title': 'Изменение покупателя', 'cancel_url': reverse_lazy('shop:customer_list')}

class CustomerDeleteView(StaffRequiredMixin, DeleteView):
    model = Customer
    template_name = 'shop/object_confirm_delete.html'
    success_url = reverse_lazy('shop:customer_list')
    extra_context = {'page_title': 'Удаление покупателя', 'cancel_url': reverse_lazy('shop:customer_list')}


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'
    context_object_name = 'orders'
    def get_queryset(self):
        queryset = Order.objects.select_related('customer', 'user')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = Order.objects.select_related('customer', 'user').prefetch_related('items__product')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

class ReviewListView(ListView):
    model = Review
    template_name = 'shop/review_list.html'
    context_object_name = 'reviews'
    queryset = Review.objects.select_related('product', 'customer')
