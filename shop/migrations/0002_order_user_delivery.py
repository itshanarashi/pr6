from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop_orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(choices=[('pickup', 'Самовывоз'), ('courier', 'Курьер'), ('delivery', 'Доставка транспортной компанией')], default='pickup', max_length=20, verbose_name='Способ получения'),
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
    ]
