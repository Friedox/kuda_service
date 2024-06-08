FROM python:3.12-slim

# Установим зависимости
RUN apt-get update && apt-get install -y gcc redis-server
COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем приложение
COPY . /app

WORKDIR /app

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
