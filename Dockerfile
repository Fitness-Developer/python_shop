FROM python:3.11-bullseye

WORKDIR /project


COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m venv /project/venv

# Устанавливаем RabbitMQ и Erlang
RUN apt-get update && apt-get install -y erlang rabbitmq-server --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Устанавливаем Redis
RUN curl -sSL https://packages.redis.io/gpg | apt-key add -
RUN echo "deb [arch=amd64] https://packages.redis.io/deb/ stable main" > /etc/apt/sources.list.d/redis.list
RUN apt-get update && apt-get install -y redis-server --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Настраиваем RabbitMQ
COPY rabbitmq_env /opt/rabbitmq/
RUN mkdir -p /var/lib/rabbitmq && chown rabbitmq:rabbitmq /var/lib/rabbitmq


ENV PATH="/project/venv/bin:/usr/local/bin:/usr/sbin:/opt/rabbitmq/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]