from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower, Cart, CartItem  # Импорт модели Flower
from .forms import OrderForm  # Импорт формы OrderForm
from django.contrib.auth.decorators import login_required  # Декоратор для проверки аутентификации

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

            # Добавляем все товары из корзины в заказ
            cart_items = request.POST.get('cart_items', '')
            item_ids = cart_items.split(',')
            for item_id in item_ids:
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
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = Cart.objects.filter(user=None).first()

    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart') # Вернуться в корзину после удаления
