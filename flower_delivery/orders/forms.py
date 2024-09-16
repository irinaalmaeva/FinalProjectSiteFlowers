from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    address = forms.CharField(label='Адрес', widget=forms.Textarea(attrs={'rows': 3}))
    flowers = forms.CharField(label='Цветы', widget=forms.Textarea(attrs={'rows': 5}))
