from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    country = models.CharField('Страна', max_length=100, blank=True)
    website = models.URLField('Сайт', blank=True)
    description = models.TextField('Описание', blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True, null=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField('Название', max_length=150)
    contact_person = models.CharField('Контактное лицо', max_length=120, blank=True)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('E-mail')
    address = models.CharField('Адрес', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Customer(models.Model):
    full_name = models.CharField('ФИО', max_length=150)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('E-mail', unique=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    registered_at = models.DateTimeField('Дата регистрации', auto_now_add=True)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['full_name']

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField('Название', max_length=150)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.PROTECT, related_name='products')
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField('Остаток', default=0)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Фотография', upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    DELIVERY_CHOICES = [
        ('pickup', 'Самовывоз'),
        ('courier', 'Курьер'),
        ('delivery', 'Доставка транспортной компанией'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True, blank=True, related_name='shop_orders')
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    total_amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    delivery_address = models.CharField('Адрес доставки', max_length=255, blank=True)
    delivery_type = models.CharField('Способ получения', max_length=20, choices=DELIVERY_CHOICES, default='pickup')
    comment = models.TextField('Комментарий', blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ №{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField('Количество', default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField('Цена на момент заказа', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'{self.product} × {self.quantity}'


class Review(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField('Оценка', validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField('Текст отзыва')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [models.UniqueConstraint(fields=['product', 'customer'], name='unique_product_customer_review')]

    def __str__(self):
        return f'{self.product}: {self.rating}/5'
