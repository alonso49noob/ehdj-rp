# Construir desde la raíz del repo:  docker build -f bot/Dockerfile -t farbeyond-bot .
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY bot/requirements.txt bot/requirements.txt
RUN pip install --no-cache-dir -r bot/requirements.txt
COPY . .
ENV KNOWLEDGE_DIR=/app
WORKDIR /app/bot
CMD ["python", "bot.py"]
