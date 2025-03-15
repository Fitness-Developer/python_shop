#!/bin/bash

source /project/venv/bin/activate

# Запуск RabbitMQ (изменено)
rabbitmq-server -detached &
while ! rabbitmqctl status > /dev/null 2>&1; do
  sleep 5
  echo "Waiting for RabbitMQ..."
done

# Запуск Redis (изменено)
redis-server &
while ! redis-cli ping > /dev/null 2>&1; do
  sleep 5
  echo "Waiting for Redis..."
done

sleep 10

/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application