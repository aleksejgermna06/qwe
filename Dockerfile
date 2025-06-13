## Используем официальный образ Python
#FROM python:3.11-slim
#
## Устанавливаем рабочую директорию
#WORKDIR /app
#
## Копируем зависимости
#COPY requirements.txt .
#
## Устанавливаем зависимости
#RUN pip install --no-cache-dir -r requirements.txt
#
## Копируем остальной проект
#COPY . .
#
## Открываем порт, на котором работает FastAPI
#EXPOSE 8000
#
## Запуск приложения
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



#
#------------------------------------------------------------
## Используем официальный образ Python
#FROM python:3.11-slim
#
## Устанавливаем переменные окружения
#ENV PYTHONDONTWRITEBYTECODE=1 \
#    PYTHONUNBUFFERED=1 \
#    PYTHONPATH=/app
#
## Устанавливаем рабочую директорию внутри контейнера
#WORKDIR /app
#
## Копируем зависимости и устанавливаем их
#COPY api/requirements.txt .
#
#RUN pip install --upgrade pip && pip install -r requirements.txt
#
## Копируем всё приложение
#COPY api/ ./api
#
## Указываем команду запуска
#CMD ["python", "api/main.py"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы из текущей директории (включая key.pem и cert.pem)
COPY . .

CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--ssl-keyfile", "/app/key.pem", \
     "--ssl-certfile", "/app/cert.pem"]
