#!/bin/bash

# Активируем виртуальную среду (исправленный путь)
source /project/venv/bin/activate

# Используйте абсолютные пути к исполняемым файлам
/opt/rabbitmq/sbin/rabbitmq-server -detached &
/usr/local/bin/redis-server &

sleep 10

/project/venv/bin/daphne -b 0.0.0.0 -p 8000 project.asgi:application