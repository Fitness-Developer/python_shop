import logging
from celery import shared_task
from .models import ReviewsOfProduct, Product
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def save_review(user_id, product_id, memo):
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)
        review = ReviewsOfProduct(author=user, product=product, memo=memo)
        review.save()
        logger.info(f"Review saved successfully. user_id={user_id}, product_id={product_id}, memo={memo}")
        return True # Возвращаем True, если сохранение прошло успешно
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
        return False
    except Product.DoesNotExist:
        logger.error(f"Product with id {product_id} does not exist.")
        return False
    except Exception as e:
        logger.exception(f"An unexpected error occurred while saving the review: {e}")
        return False

@shared_task
def send_purchase_email(email, product_title):
    subject = 'Ваш заказ успешно оформлен!'
    message = f'Спасибо за покупку {product_title}. Ваш заказ был успешно оформлен.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )