from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from .tasks import save_review


def contains_prohibited_words(content):
    prohibited_words = ['сука','пизда']  # Добавьте свои слова
    return any(word in content.lower() for word in prohibited_words)


def reviews(request):
    reviews = Review.objects.order_by('-created')

    if request.method == 'GET' and request.user.is_authenticated:
        return render(request, 'review/reviews.html', {
            'reviews': reviews,
            'form': ReviewForm(user=request.user),
            'author': request.user
        })
    else:
        form = ReviewForm(request.POST or None, user=request.user)

        if form.is_valid():
            memo = form.cleaned_data['memo']

            # Валидация длины текста
            if len(memo) > 500:
                return render(request, 'review/reviews.html', {
                    'reviews': reviews,
                    'form': form,
                    'error': 'Отзыв не должен превышать 500 символов.'
                })
            if len(memo) == 0:
                return render(request, 'review/reviews.html', {
                    'reviews': reviews,
                    'form': form,
                    'error': 'Нельзя отправить пустую форму.'
                })
            # Фильтрация нежелательных слов
            if contains_prohibited_words(memo):
                return render(request, 'review/reviews.html', {
                    'reviews': reviews,
                    'form': form,
                    'error': 'Ваш отзыв содержит недопустимые слова.'
                })

            # Отправка задачи в Celery для сохранения отзыва
            save_review.delay(request.user.id, memo)

            # Уведомление об успешной отправке
            return render(request, 'review/reviews.html', {
                'reviews': reviews,
                'form': ReviewForm(user=request.user),
                'author': request.user,
                'success': 'Ваш отзыв был успешно отправлен и будет опубликован после проверки.'
            })
        else:
            return render(request, 'review/reviews.html', {
                'reviews': reviews,
                'form': form,
                'error': 'Переданы неверные данные. Попробуйте ещё раз.'
            })




