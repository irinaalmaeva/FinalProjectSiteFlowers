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
    return redirect('view_cart')
