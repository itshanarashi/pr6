from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Basket:
    def __init__(self, request):
        self.session = request.session
        self.data = self.session.get(settings.BASKET_SESSION_ID, {})

    def add(self, product, quantity=1, override=False):
        product_id = str(product.pk)
        quantity = max(1, min(int(quantity), product.stock))
        if product_id not in self.data:
            self.data[product_id] = {'quantity': 0}
        if override:
            self.data[product_id]['quantity'] = quantity
        else:
            self.data[product_id]['quantity'] = min(
                self.data[product_id]['quantity'] + quantity,
                product.stock,
            )
        self.save()

    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.data:
            del self.data[product_id]
            self.save()

    def save(self):
        self.session[settings.BASKET_SESSION_ID] = self.data
        self.session.modified = True

    def clear(self):
        self.session.pop(settings.BASKET_SESSION_ID, None)
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.data.values())

    def __iter__(self):
        product_ids = list(self.data.keys())
        products = Product.objects.filter(pk__in=product_ids).select_related('category', 'brand')
        existing_ids = set()
        for product in products:
            product_id = str(product.pk)
            existing_ids.add(product_id)
            item = self.data[product_id].copy()
            item['product'] = product
            item['price'] = product.price
            item['total_price'] = product.price * item['quantity']
            yield item

        stale_ids = set(product_ids) - existing_ids
        if stale_ids:
            for product_id in stale_ids:
                self.data.pop(product_id, None)
            self.save()

    def total_price(self):
        return sum((item['total_price'] for item in self), Decimal('0'))
