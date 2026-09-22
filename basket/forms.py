from django import forms

from shop.models import Order


class BasketAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, label='Количество')
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'delivery_type', 'comment']
        widgets = {
            'delivery_address': forms.TextInput(attrs={'placeholder': 'Адрес доставки'}),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Комментарий к заказу'}),
        }
