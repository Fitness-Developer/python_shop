FROM python:3.11-bullseye

WORKDIR /project

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m venv /project/venv

# Устанавливаем RabbitMQ и Erlang и Redis
RUN apt-get update && apt-get install -y --no-install-recommends erlang rabbitmq-server redis-server && rm -rf /var/lib/apt/lists/*


ENV PATH="/project/venv/bin:/usr/local/bin:/usr/sbin:/opt/rabbitmq/sbin:$PATH"
EXPOSE 8000
CMD ["/project/entrypoint.sh"]