FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "hammer_systems.wsgi:application", "--bind", "0:8000" ] 