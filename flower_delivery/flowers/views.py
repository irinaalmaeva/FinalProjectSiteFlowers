from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower
from orders.forms import OrderForm

def flower_catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'flower_catalog.html', {'flowers': flowers})

def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'flower_detail.html', {'flower': flower})

def checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                return redirect('order_history')
        else:
            # Обработка случая, когда пользователь не аутентифицирован
            return redirect('login')  # Или другая логика
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})

