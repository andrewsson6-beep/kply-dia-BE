FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8080

CMD ["sh", "-c", "uvicorn main:app --app-dir /app/src --host 0.0.0.0 --port ${PORT:-8080}"]