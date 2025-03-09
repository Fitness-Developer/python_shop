from celery import shared_task
from .models import Review
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def save_review(user_id, memo):
    try:
        user = User.objects.get(id=user_id)
        review = Review(author=user, memo=memo)
        review.save()
        logger.info("Review saved successfully for user_id: %s", user_id)
    except Exception as e:
        logger.error("Error saving review: %s", e)