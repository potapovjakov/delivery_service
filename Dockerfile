FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY ./docker-entrypoint.sh .

COPY . ./
RUN chmod +x /app/docker-entrypoint.sh
