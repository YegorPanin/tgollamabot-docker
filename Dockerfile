# Используем базовый образ
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY main.py /app
COPY requirements.txt /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду для запуска приложения
CMD ["python", "main.py"]
