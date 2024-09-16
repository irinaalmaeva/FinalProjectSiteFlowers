from django import forms
from .models import Flower

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
