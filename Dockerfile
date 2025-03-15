FROM python:3.11-bullseye

WORKDIR /project

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m venv /project/venv

# Устанавливаем RabbitMQ и Erlang
RUN apt-get update && apt-get install -y --no-install-recommends erlang rabbitmq-server redis-server && rm -rf /var/lib/apt/lists/*

# Настраиваем RabbitMQ (изменено)
RUN mkdir -p /var/lib/rabbitmq
RUN chown rabbitmq:rabbitmq /var/lib/rabbitmq


# Добавляем пользователя rabbitmq (если его нет)
RUN groupadd --gid 200 rabbitmq && useradd --uid 200 --gid 200 --shell /bin/false --create-home rabbitmq

ENV PATH="/project/venv/bin:/usr/local/bin:/usr/sbin:/opt/rabbitmq/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]