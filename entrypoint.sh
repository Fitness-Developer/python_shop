#!/bin/bash
source /project/venv/bin/activate
echo "Starting RabbitMQ..."
rabbitmq-server -detached &
echo "Starting Redis..."
redis-server &
sleep 30 # Дайте сервисам время запуститься
echo "Starting Daphne..."
/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application