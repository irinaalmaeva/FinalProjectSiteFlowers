from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from flowers.models import Flower
from .models import Order
from .forms import OrderForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import requests
from django.conf import settings
import json
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

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

            # Вызываем функцию отправки уведомления
            send_order_notification(order)


            return redirect('order_success')
        else:
            messages.error(request, 'Ошибка при оформлении заказа. Пожалуйста, проверьте введенные данные.')
    else:
        form = OrderForm()

    return render(request, 'checkout.html', {'form': form, 'flower': flower})


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            # Логируем полученные данные
            data = json.loads(request.body)
            logger.info(f"Полученные данные: {data}")

            user_id = data.get('user_id')
            flowers_ids = data.get('flowers_ids', [])
            address = data.get('address')

            # Проверяем наличие обязательных данных
            if not user_id or not flowers_ids or not address:
                return JsonResponse({'status': 'error', 'message': 'Отсутствуют обязательные данные.'})

            # Проверяем наличие пользователя
            try:
                user = User.objects.get(id=user_id)
                logger.info(f"Найден пользователь: {user.username}")
            except User.DoesNotExist:
                logger.error(f"Пользователь с ID {user_id} не найден.")
                return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})


                # Создаем новый заказ
                order = Order.objects.create(user=user, address=address,is_from_telegram=True  # Устанавливаем, что заказ из Telegram
            )
                for flower_id in flowers_ids:
                    flower = Flower.objects.get(id=flower_id)
                    order.flowers.add(flower)
                order.save()

            logger.info(f"Заказ создан: {order.id}")

            return JsonResponse({'status': 'success', 'order_id': order.id})
        except User.DoesNotExist:
            logger.error("Ошибка: Пользователь не найден.")
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'})
        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")
            return JsonResponse(
                {'status': 'error', 'message': 'Произошла ошибка при оформлении заказа. Попробуйте позже.'})

def update_order_status(request, order_id, new_status):
    # Проверка, что новый статус допустим
    valid_statuses = dict(Order.STATUS_CHOICES).keys()
    if new_status not in valid_statuses:
        return ("Недопустимый статус")

    order = get_object_or_404(Order, id=order_id)
    order.status = new_status
    order.save()
    return redirect('order_detail', pk=order.id)  # Перенаправление на страницу деталей заказа


def send_order_notification(order):
    token = settings.TELEGRAM_BOT_TOKEN  # Токен бота из настроек
    chat_id = settings.TELEGRAM_CHAT_ID  # Идентификатор чата из настроек
    url = f"https://api.telegram.org/bot{token}/sendPhoto"

    # Получаем данные о заказе
    flowers = order.flowers.all()  # Получаем все цветы в заказе
    flower_details = []

    for flower in flowers:
        flower_name = flower.name
        price = flower.price
        image_url = flower.image.url  # URL изображения цветка

        # Формируем информацию по каждому цветку
        flower_details.append(
            f"{flower_name} - {price} руб."
        )

    # Объединяем информацию о всех цветах
    flower_details_str = "\n".join(flower_details)

    order_date = order.order_date.strftime('%Y-%m-%d %H:%M:%S')
    delivery_address = order.address

    # Формируем текст сообщения
    message_text = (
        f"Новый заказ!\n\n"
        f"Цветы:\n{flower_details_str}\n\n"
        f"Дата и время заказа: {order_date}\n"
        f"Адрес доставки: {delivery_address}"
    )

    # Полный URL для изображения первого цветка (если есть)
    if flowers.exists():
        photo_url = f"{settings.YOUR_DOMAIN}{flowers[0].image.url}"
    else:
        photo_url = None

    # Подготовка данных для отправки
    data = {
        'chat_id': chat_id,
        'caption': message_text,
    }
    logging.info(f"Отправка данных в Telegram: {data}")

    try:
        # Отправляем фото, если оно есть, иначе только текст
        if photo_url:
            data['photo'] = photo_url
            response = requests.post(url, data=data)
        else:
            text_url = f"https://api.telegram.org/bot{token}/sendMessage"
            response = requests.post(text_url, data={'chat_id': chat_id, 'text': message_text})

        response.raise_for_status()  # Проверка на ошибки HTTP
        logging.info(f"Успешно отправлено сообщение в Telegram: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения в Telegram: {e}")

    return response.status_code