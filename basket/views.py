from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from shop.models import Customer, Order, OrderItem, Product

from .basket import Basket
from .forms import BasketAddProductForm, OrderForm


def basket_detail(request):
    basket = Basket(request)
    for item in basket:
        item['update_form'] = BasketAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
        })
    return render(request, 'basket/detail.html', {'basket': basket})


@login_required
@require_POST
def basket_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.stock < 1:
        messages.error(request, 'Товара нет в наличии.')
        return redirect('shop:product_detail', pk=product.pk)

    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        quantity = min(form.cleaned_data['quantity'], product.stock)
        Basket(request).add(
            product=product,
            quantity=quantity,
            override=form.cleaned_data['override'],
        )
        messages.success(request, 'Товар добавлен в корзину.')
    else:
        messages.error(request, 'Укажите корректное количество товара.')
    return redirect('basket:detail')


@login_required
@require_POST
def basket_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Basket(request).remove(product)
    return redirect('basket:detail')


@login_required
@require_POST
def basket_clear(request):
    Basket(request).clear()
    return redirect('basket:detail')


@login_required
def order_create(request):
    basket = Basket(request)
    if len(basket) == 0:
        messages.error(request, 'Корзина пуста.')
        return redirect('basket:detail')

    available_items = []
    for item in basket:
        quantity = min(item['quantity'], item['product'].stock)
        if quantity > 0:
            available_items.append((item, quantity))

    if not available_items:
        messages.error(request, 'Товары из корзины закончились на складе.')
        return redirect('basket:detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                customer = _customer_for_user(request.user)
                order = form.save(commit=False)
                order.user = request.user
                order.customer = customer
                order.total_amount = Decimal('0')
                order.save()

                total = Decimal('0')
                for item, quantity in available_items:
                    product = Product.objects.select_for_update().get(pk=item['product'].pk)
                    quantity = min(quantity, product.stock)
                    if quantity < 1:
                        continue
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )
                    total += product.price * quantity
                    product.stock -= quantity
                    product.save(update_fields=['stock'])

                if not order.items.exists():
                    order.delete()
                    messages.error(request, 'Не удалось создать заказ: товары закончились.')
                    return redirect('basket:detail')

                order.total_amount = total
                order.save(update_fields=['total_amount'])
                basket.clear()

            messages.success(request, f'Заказ №{order.pk} создан.')
            return redirect('shop:order_detail', pk=order.pk)
    else:
        form = OrderForm()

    return render(request, 'basket/order_form.html', {'basket': basket, 'form': form})


def _customer_for_user(user):
    email = user.email or f'{user.username}@local.invalid'
    customer = Customer.objects.filter(email=email).first()
    if customer:
        return customer
    return Customer.objects.create(
        full_name=user.get_full_name() or user.username,
        phone='',
        email=email,
        address='',
    )
