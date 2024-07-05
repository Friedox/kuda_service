FROM python:3.12-slim

RUN apt-get update && apt-get install -y gcc redis-server postgresql-client
COPY pip.conf /root/.pip/pip.conf
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir --upgrade wheel
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

WORKDIR /app

COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

CMD ["./backend/app/wait-for-postgres.sh","&&", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]