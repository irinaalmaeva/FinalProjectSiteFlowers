from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from flowers.models import Flower
from .models import Order
from .forms import OrderForm

def order_success(request):
    return render(request, 'order_success.html')

def order_history(request):
    if request.user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
        orders = Order.objects.filter(user=request.user)
        return render(request, 'order_history.html', {'orders': orders})
    else:
        messages.error(request, 'Вы должны быть аутентифицированы для просмотра истории заказов.')
        return redirect('login')  # Перенаправляем на страницу входа

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'order_detail.html', {'order': order})


def place_order(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.flower = flower  # Привязываем цветок к заказу
            order.user = request.user  # Привязываем текущего пользователя (если реализована система пользователей)
            order.save()
            messages.success(request, 'Ваш заказ успешно оформлен!')
            return redirect('order_success')
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Пожалуйста, проверьте введенные данные.')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'flower': flower})

