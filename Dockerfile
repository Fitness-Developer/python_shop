# Stage 1: Build the application
FROM python:3.11-bullseye AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install pysqlite3-binary
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Stage 2: Redis
FROM redis:alpine

# Stage 3: RabbitMQ
FROM rabbitmq:3-management

# Stage 4: Nginx
FROM nginx:latest
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./staticfiles /usr/share/nginx/html/static # Важно: скопировать статические файлы

# Stage 5: Final image
FROM python:3.11-bullseye
WORKDIR /app
COPY --from=builder /project /project
COPY --from=redis / /project/redis #Копируем redis - не обязательно, только если нужны файлы redis из образа
COPY --from=rabbitmq / /project/rabbitmq # Копируем rabbitmq - не обязательно, только если нужны файлы rabbitmq из образа
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
EXPOSE 8000
CMD ["/app/entrypoint.sh"]