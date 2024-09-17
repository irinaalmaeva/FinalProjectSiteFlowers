from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']  # Здесь мы включаем только адрес, так как цветок привязан в views
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес доставки'}),
        }
