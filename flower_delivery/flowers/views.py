from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower, Cart, CartItem  # Импорт модели Flower
from .forms import OrderForm  # Импорт формы OrderForm
from django.contrib.auth.decorators import login_required  # Декоратор для проверки аутентификации
from django.http import JsonResponse

def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_catalog.html', {'flowers': flowers})

def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'flower_detail.html', {'flower': flower})

@login_required
def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Привязываем заказ к пользователю
            order.save()
            form.save_m2m()  # Сохраняем связь с цветами (ManyToManyField)
            return redirect('order_success')

            # Получаем все товары из корзины и убираем пустые значения
            cart_items = [item_id for item_id in request.POST.getlist('cart_items') if item_id]

            # Проверяем, есть ли товары в корзине
            if cart_items:
                for item_id in cart_items:
                    cart_item = get_object_or_404(CartItem, id=item_id)
                    order.flowers.add(cart_item.flower)  # Привязываем выбранный цветок к заказу
                    cart_item.delete()  # Удаляем товар из корзины

            return redirect('order_history')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form})

# --- Новые функции для корзины ---
@login_required
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:

        cart = Cart.objects.filter(user=None).first() or Cart.objects.create()

    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')
@login_required
def view_cart(request):
    cart = Cart.objects.get(user=request.user)  # Предполагается, что у вас есть логика для получения корзины пользователя
    cart_items = CartItem.objects.filter(cart=cart)

    # Расчитываем общую стоимость
    total_price = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart') # Вернуться в корзину после удаления

def flower_catalog_api(request):
    flowers = Flower.objects.all()  # Получаем все цветы из базы данных
    flowers_list = [
        {
            'id': flower.id,
            'name': flower.name,
            'price': flower.price,
            'description': flower.description,
        }
        for flower in flowers
    ]
    return JsonResponse(flowers_list, safe=False)

