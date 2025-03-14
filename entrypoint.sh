#!/bin/bash
/usr/local/bin/redis-server &
/usr/sbin/rabbitmq-server -detached &

sleep 10

# Используйте полный путь к daphne
/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application