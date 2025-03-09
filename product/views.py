from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404, redirect
from .models import Product,ReviewsOfProduct
from Purchased.models import Purchased
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .utils import search_products
from .forms import PayForm,ReviewForm
from django.contrib import messages
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer
from django.dispatch import receiver
from social_core.pipeline.social_auth import social_user
from social_core.exceptions import AuthForbidden
from .tasks import save_review, send_purchase_email
from yookassa import Configuration, Payment
from uuid import uuid4
from django.core.mail import send_mail
from django.conf import settings
import logging
import socket

Configuration.configure('1010382', 'test_3OArUjeWFRS8sjIa44FSJeIKMOlH6pDVBL5Q6kjuk6A')
def index(request):
    product, search_query = search_products(request)
    room_name = "Support-chat"

    if request.user.is_authenticated:
        return render(request, 'products/index.html',
                      {'products': product, 'search_query': search_query,'room_name': room_name, 'is_index_page': True})

    else:
        return render(request, 'products/index.html',
                      {'products': product, 'search_query': search_query,'room_name': room_name, 'is_index_page': True})



def main(request):
    return render(request, 'products/main.html', {'main': main})


def contains_prohibited_words(content):
    prohibited_words = ['сука','пизда']  # Добавьте свои слова
    return any(word in content.lower() for word in prohibited_words)


# logger = logging.getLogger(__name__)
#
#
# @login_required(login_url="loginuser")
# def detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     reviews = product.reviews.all()
#
#     logger.info(f"Request to detail view: product_id={product_id}, method={request.method}")
#
#     if request.method == 'POST':
#         if request.user is None:
#             logger.warning("Unauthorized access attempt to POST /detail/")
#             return JsonResponse({'success': False, 'error': 'Вы не авторизованы'}, status=401)
#
#
#         review_form = ReviewForm(request.POST)
#         logger.debug(f"Form data: {request.POST}")
#
#
#         if review_form.is_valid():
#             memo = review_form.cleaned_data['memo']
#
#             if len(memo) > 500:
#                 logger.warning(f"Review too long: {len(memo)} characters")
#                 return render(request, 'products/details.html', {
#                     'product': product,
#                     'reviews': reviews,
#                     'review_form': review_form,
#                     'error': 'Отзыв не должен превышать 500 символов.'
#                 })
#             if len(memo) == 0:
#                 logger.warning("Empty review submitted")
#                 return render(request, 'products/details.html', {
#                     'product': product,
#                     'reviews': reviews,
#                     'review_form': review_form,
#                     'error': 'Нельзя отправить пустую форму.'
#                 })
#             # Фильтрация нежелательных слов (предполагается, что функция contains_prohibited_words существует)
#             if contains_prohibited_words(memo):
#                 logger.warning(f"Review contains prohibited words: {memo}")
#                 return render(request, 'products/details.html', {
#                     'product': product,
#                     'reviews': reviews,
#                     'review_form': review_form,
#                     'error': 'Ваш отзыв содержит недопустимые слова.'
#                 })
#
#             try:
#                 user_id = request.user.id
#                 logger.info(f"Saving review: user_id={user_id}, product_id={product_id}, memo={memo}")
#                 result = save_review.delay(user_id, product_id, memo)
#                 logger.info(f"Celery task started: {result}")
#                 return JsonResponse({'success': True})
#             except Exception as e:
#                 logger.exception(f"Error saving review: {e}")
#                 return JsonResponse({'success': False, 'error': 'Ошибка сервера'}, status=500)
#
#         else:
#             logger.warning(f"Invalid form data: {review_form.errors}")
#             return render(request, 'products/details.html', {
#                 'product': product,
#                 'reviews': reviews,
#                 'review_form': review_form,
#                 'error': 'Переданы неверные данные. Попробуйте ещё раз.'
#             })
#     else:
#         review_form = ReviewForm()
#         return render(request, 'products/details.html', {
#             'product': product,
#             'reviews': reviews,
#             'review_form': review_form,
#         })



@login_required(login_url="loginuser")
def detail(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()  # Получаем отзывы для продукта

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            memo = review_form.cleaned_data['memo']

            # Валидация длины текста
            if len(memo) > 500:
                return render(request, 'products/details.html', {
                    'product': product,
                    'reviews': reviews,
                    'review_form': review_form,
                    'error': 'Отзыв не должен превышать 500 символов.'
                })
            if len(memo) == 0:
                return render(request, 'products/details.html', {
                    'product': product,
                    'reviews': reviews,
                    'review_form': review_form,
                    'error': 'Нельзя отправить пустую форму.'
                })
            # Фильтрация нежелательных слов
            if contains_prohibited_words(memo):
                return render(request, 'products/details.html', {
                    'product': product,
                    'reviews': reviews,
                    'review_form': review_form,
                    'error': 'Ваш отзыв содержит недопустимые слова.'
                })

            # Отправка задачи в Celery для сохранения отзыва
            save_review.delay(request.user.id,product.id, memo)

            # Уведомление об успешной отправке
            return redirect('detail', product_id=product.id)  # Перенаправляем на ту же страницу с сообщением об успехе

        else:
            return render(request, 'products/details.html', {
                'product': product,
                'reviews': reviews,
                'review_form': review_form,
                'error': 'Переданы неверные данные. Попробуйте ещё раз.'
            })
    else:
        review_form = ReviewForm()  # Создаем пустую форму для отображения

    return render(request, 'products/details.html', {
        'product': product,
        'reviews': reviews,  # Передаем отзывы в шаблон
        'review_form': review_form,  # Передаем форму в шаблон
    })

# def deleteprod(request, product_id):
#     product = get_object_or_404(Product,pk=product_id)
#     wallet_user = CustomUser.objects.get(user=request.user)
#     product.price = int(product.price)
#     if wallet_user.value >= product.price:
#         if request.method == "POST":
#             wallet_user.value -= product.price
#             wallet_user.save()
#             del_obj=Purchased(title=product.title,description=product.description,price=product.price,image=product.image.path,author=request.user)
#             del_obj.save()
#             product.delete()
#             return redirect('index')
#         return redirect('index')
#     else:
#         return render(request, 'products/details.html', {
#                  'product': product,
#                  'wallet_user': wallet_user,
#                  'error_message': 'У вас недостаточно средств.'
#              })


def payform(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email  # Сохранение email в сессии
            request.session['product_id'] = product_id  # Сохранение product_id в сессии

            # Создание платежа в YooKassa

            if request.get_host().startswith('localhost'):
                base_url = "http://localhost:8000"
            else:
                base_url = "https://python-shop.onrender.com"

            payment = Payment.create({
                "amount": {
                    "value": str(product.price),
                    "currency": "RUB"  # Укажите нужную валюту
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"{base_url}/{product_id}/success/",  # URL для перенаправления после успешной оплаты
                },
                "capture": True,
                "description": f"Оплата за {product.title}",
            }, uuid4())

            # Сохранение payment_id в сессии
            request.session['payment_id'] = payment.id

            # Перенаправление на страницу оплаты YooKassa
            return redirect(payment.confirmation.confirmation_url)

    else:
        form = PayForm()

    return render(request, 'products/pay_form.html', {
        'product': product,
        'form': form,
    })






def payment_success(request, product_id):
    payment_id = request.session.get('payment_id')
    email = request.session.get('email')

    # Проверка статуса платежа
    payment = Payment.find_one(payment_id)

    if payment.status == 'succeeded':
        product = get_object_or_404(Product, pk=product_id)

        # Создание записи о покупке
        purchased = Purchased(
            title=product.title,
            description=product.description,
            price=product.price,
            image=product.image,
            author=request.user,
            email=email
        )
        purchased.save()
        product.delete()
        # Отправка сообщения на почту
        send_mail(
            'Ваш заказ успешно оплачен',
            f'Спасибо за покупку {product.title}.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Очистка сессии
        del request.session['payment_id']
        del request.session['email']

        return render(request, 'products/success.html', {'product': product})

    return render(request, 'products/failure.html')
def payment_failure(request):
    return render(request, 'products/failure.html')

# def product_detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     reviews = product.reviews.all()
#
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#
#         if review_form.is_valid():
#             review = ReviewsOfProduct(
#                 product=product,
#                 author=request.user,
#                 memo=review_form.cleaned_data['memo']
#             )
#             review.save()
#             return redirect('detail', product_id=product.id)
#     else:
#         review_form = ReviewForm()
#
#     return render(request, 'products/details.html', {
#         'product': product,
#         'reviews': reviews,
#         'review_form': review_form,
#     })

def signupuser(request):
    if request.method == "GET":
        return render(request, 'products/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'products/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Такое имя пользователя уже существует. Задайте другое'})
        else:
            return render(request, 'products/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')


def loginuser(request):
    if request.method == "GET":
        return render(request,'products/loginuser.html',{'form': AuthenticationForm()})
    else:
        user = authenticate(request,username=request.POST['username'],password= request.POST['password'])
        if user is None:
            return render(request, 'products/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('index')



# class SignupView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
#
# class CustomTokenObtainPairView(TokenObtainPairView):
#     # Вы можете переопределить метод, если хотите добавить дополнительные поля в токен.
#     pass




