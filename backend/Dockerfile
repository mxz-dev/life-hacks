# backend/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./ 
RUN apt-get update && apt-get install -y \
gcc \
libpq-dev \
python3-dev \
&& rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
EXPOSE 8880
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
