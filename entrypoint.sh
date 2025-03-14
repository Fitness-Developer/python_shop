#!/bin/bash

source /project/venv/bin/activate

# Запуск RabbitMQ
rabbitmq-server -detached &
until [[ $(curl -s -o /dev/null -w "%{http_code}" http://localhost:15672) == "200" ]]; do
  echo "Waiting for RabbitMQ..."
  sleep 5
done

# Запуск Redis
redis-server &
until [[ $(curl -s -o /dev/null -w "%{http_code}" http://localhost:6379) == "200" ]]; do
  echo "Waiting for Redis..."
  sleep 5
done

sleep 10

/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application