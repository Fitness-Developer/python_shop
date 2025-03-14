# Stage 1: Build the application
FROM python:3.11-bullseye AS builder
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install pysqlite3-binary
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
RUN python3 -m venv /project/venv

# Stage 2: Redis
FROM redis:6.2-alpine AS redis-stage

# Stage 4: Nginx
FROM nginx:latest
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./staticfiles /usr/share/nginx/html/static

# Stage 5: Final image (изменено)
FROM python:3.11-bullseye
WORKDIR /project
COPY --from=builder /project /project
COPY --from=builder /project/venv /project/venv
COPY --from=redis-stage /usr/local/bin/redis-server /usr/local/bin/

# Добавляем RabbitMQ напрямую, без копирования
COPY rabbitmq_env /opt/rabbitmq/ #Если нужно, но вероятно, не нужно
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

# Используем готовый образ RabbitMQ
RUN apt-get update && apt-get install -y erlang --no-install-recommends && rm -rf /var/lib/apt/lists/*

FROM rabbitmq:3-management
WORKDIR /project
COPY --from=0 /project/venv /project/venv
COPY --from=0 /project /project
COPY --from=3 /etc/nginx /etc/nginx
COPY --from=3 /usr/share/nginx/html /usr/share/nginx/html
COPY --from=0 ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENV PATH="/project/venv/bin:/usr/local/bin:/usr/sbin:/opt/rabbitmq/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]