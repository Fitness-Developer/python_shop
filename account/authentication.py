from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from social_core.exceptions import AuthForbidden
from django.utils.text import slugify

User = get_user_model()


def create_user(strategy, details, *args, **kwargs):
    if 'email' in details:
        email = details['email']
        user = User.objects.filter(email=email).first()

        if user:
            return {'user': user}
        else:
            # Получаем имя и фамилию из деталей
            first_name = details.get('first_name', '')
            last_name = details.get('last_name', '')

            # Создаем username на основе имени и фамилии
            if first_name and last_name:
                username = f"{first_name}_{last_name}"
            elif first_name:
                username = first_name
            elif last_name:
                username = last_name
            else:
                username = email.split('@')[0]  # Резервный вариант

            # Убедитесь, что имя пользователя уникально
            username = slugify(username)  # Преобразуем в безопасный формат
            counter = 1
            original_username = username

            while User.objects.filter(username=username).exists():
                username = f"{original_username}_{counter}"
                counter += 1

            user = User.objects.create_user(username=username, email=email)

            return {'user': user}
    else:
        raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None