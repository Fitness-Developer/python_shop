FROM python:3.11-bullseye

WORKDIR /project

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install psycopg2-binary # Установка psycopg2-binary

COPY . .

# Добавление команд для миграций
RUN /opt/venv/bin/python manage.py makemigrations
RUN /opt/venv/bin/python manage.py migrate


ENV PATH="/opt/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=project.settings
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//



CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"]