FROM python:3.9-slim
# Устанавливаем системный Poppler для работы с PDF
RUN apt-get update && apt-get install -y poppler-utils && apt-get clean
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Запускаем сервер
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
