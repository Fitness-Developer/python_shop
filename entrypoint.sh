#!/bin/bash
source /opt/venv/bin/activate
redis-server &
rabbitmq-server -detached &
sleep 30 # Дайте время на запуск сервисов
gunicorn --bind 0.0.0.0:8000 project.asgi:application & # или daphne
celery -A project worker -l info -B &
wait