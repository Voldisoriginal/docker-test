# Используйте официальный Python образ в качестве базового
FROM python:3.12-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл requirements.txt в контейнер
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте файлы приложения в контейнер
COPY . .

# Укажите команду для выполнения при запуске контейнера
CMD ["uvicorn", "mainapp:app", "--host", "0.0.0.0", "--port", "8000"]