# Stage 1: Build the application
FROM python:3.11-bullseye AS builder
WORKDIR /project
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install pysqlite3-binary
COPY . .

# Stage 2: RabbitMQ (используем готовый образ)
FROM rabbitmq:3-management AS rabbitmq

# Stage 3: Redis (используем готовый образ)
FROM redis:alpine AS redis

# Stage 4: Final image
FROM python:3.11-bullseye
WORKDIR /project
COPY --from=builder /project /project
COPY --from=rabbitmq /opt/rabbitmq/sbin/rabbitmq-server /usr/local/bin/
COPY --from=redis /usr/local/bin/redis-server /usr/local/bin/
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV PATH="/opt/venv/bin:/usr/local/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=project.settings
ENV CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
CMD ["/entrypoint.sh"]