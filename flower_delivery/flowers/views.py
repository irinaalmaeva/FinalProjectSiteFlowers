from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower  # Импорт модели Flower
from .forms import OrderForm  # Импорт формы OrderForm

def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_catalog.html', {'flowers': flowers})

def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'flower_detail.html', {'flower': flower})

def place_order(request,flower_id):
    flower = get_object_or_404(Flower, id=flower_id) # Получаем выбранный цветок
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user # Привязываем заказ к пользователю
                order.save()
                order.flowers.add(flower)  # Привязываем выбранный цветок к заказу
                return redirect('order_history')
        else:
            # Обработка случая, когда пользователь не аутентифицирован
            return redirect('login')  # Или другая логика
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})

