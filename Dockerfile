# Stage 1: Build the application
FROM python:3.11-bullseye AS builder
WORKDIR /project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install pysqlite3-binary
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Stage 2: Redis
FROM redis:alpine AS redis-stage
RUN mkdir -p /usr/local/bin
COPY --from=redis-stage /usr/local/bin/redis-server /usr/local/bin/

# Stage 3: RabbitMQ
FROM rabbitmq:3-management AS rabbitmq-stage
RUN mkdir -p /usr/sbin
COPY --from=rabbitmq-stage /opt/rabbitmq/sbin/rabbitmq-server /usr/sbin/
COPY --from=rabbitmq-stage /opt/rabbitmq/lib/rabbitmq_server-3/rabbitmq_env /usr/sbin/

# Stage 4: Nginx
FROM nginx:latest
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./staticfiles /usr/share/nginx/html/static

# Stage 5: Final image
FROM python:3.11-bullseye
WORKDIR /project
COPY --from=builder /project /project
COPY --from=redis-stage /usr/local/bin/redis-server /usr/local/bin/
COPY --from=rabbitmq-stage /usr/sbin/rabbitmq-server /usr/sbin/
COPY --from=rabbitmq-stage /usr/sbin/rabbitmq_env /usr/sbin/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENV PATH="/usr/local/bin:/usr/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]