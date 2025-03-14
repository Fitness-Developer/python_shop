#!/bin/bash
/usr/local/bin/redis-server &
/usr/sbin/rabbitmq-server &

sleep 10

/project/daphne -b 0.0.0.0 -p 8000 project.asgi:application