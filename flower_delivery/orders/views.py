from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from flowers.models import Flower
from .models import Order
from .forms import OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json

def order_success(request):
    return render(request, 'order_success.html')

def order_history(request):
    if request.user.is_authenticated:  # Проверяем, аутентифицирован ли пользователь
        # Используем prefetch_related для загрузки связанных цветов
        orders = Order.objects.filter(user=request.user).prefetch_related('flowers')
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
            order.user = request.user  # Привязываем текущего пользователя (если реализована система пользователей)
            order.save()
            order.flowers.add(flower)  # Привязываем выбранный цветок к заказу


            return redirect('order_success')
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Пожалуйста, проверьте введенные данные.')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'flower': flower})

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        flowers_ids = data.get('flowers_ids', [])
        address = data.get('address')

        try:
            user = User.objects.get(id=user_id)
            order = Order.objects.create(user=user, address=address)
            for flower_id in flowers_ids:
                flower = Flower.objects.get(id=flower_id)
                order.flowers.add(flower)
            order.save()
            return JsonResponse({'status': 'success', 'order_id': order.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



