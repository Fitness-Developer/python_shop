#!/bin/bash

# Активируем виртуальную среду
source /project/venv/bin/activate

# Используйте абсолютные пути к исполняемым файлам
/opt/rabbitmq/sbin/rabbitmq-server -detached &
/usr/local/bin/redis-server &

sleep 10

# Используйте полный путь к daphne
/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application