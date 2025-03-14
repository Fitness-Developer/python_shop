#!/bin/bash
# запускаем redis и rabbitmq в фоне
/project/redis/bin/redis-server &
/project/rabbitmq/sbin/rabbitmq-server &

# Даем время на запуск redis и rabbitmq
sleep 10

# Запускаем Django
daphne -b 0.0.0.0 -p 8000 project.asgi:application