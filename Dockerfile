FROM python:3.11-bullseye

WORKDIR /project

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r requirements.txt \
    && /opt/venv/bin/pip install pysqlite3-binary # Установка pysqlite3-binary - здесь важно

COPY . .

ENV PATH="/opt/venv/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=project.settings
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

VOLUME ["/project/db.sqlite3"]

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "project.asgi:application"]