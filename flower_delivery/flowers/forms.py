from django import forms
from .models import Flower
from orders.models import Order  # Импорт модели Order из приложения orders


class FlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['name', 'description', 'price', 'image']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'image': 'Изображение'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']  # Или другие поля формы


