# Stage 1: Build the application
FROM python:3.11-bullseye AS builder
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 -m venv /project/venv
RUN . /project/venv/bin/activate && pip install -r requirements.txt


# Stage 2: RabbitMQ (используем готовый образ)
FROM rabbitmq:3-management AS rabbitmq

# Stage 3: Redis (используем готовый образ)
FROM redis:alpine AS redis

# Stage 4: Final image
FROM python:3.11-bullseye
WORKDIR /project
COPY --from=builder /project /project
COPY --from=rabbitmq /opt/rabbitmq/sbin/rabbitmq-server /usr/sbin/
COPY --from=redis /usr/local/bin/redis-server /usr/local/bin/

ENV PATH="/project/venv/bin:/usr/local/bin:/usr/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]