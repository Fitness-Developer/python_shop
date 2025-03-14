#!/bin/bash
/usr/local/bin/redis-server &
/opt/rabbitmq/sbin/rabbitmq-server &

sleep 10

daphne -b 0.0.0.0 -p 8000 project.asgi:application