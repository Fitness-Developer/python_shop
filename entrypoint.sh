#!/bin/bash
# Активируем виртуальную среду
. /opt/venv/bin/activate

# Запускаем сервисы, используя их собственные средства
# Это гораздо надёжнее, чем напрямую запускать исполняемые файлы.
# Также, используем ожидание завершения, для большей надёжности.
rabbitmq-server -detached &
redis-server &

# Даём время на запуск
sleep 30

# Запускаем gunicorn или daphne
gunicorn --bind 0.0.0.0:8000 project.asgi:application &

# Запускаем Celery worker в фоне
celery -A project worker -l info -B &

wait