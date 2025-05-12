FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn_server.py gunicorn.conf.py ./

EXPOSE 8080

CMD ["gunicorn", "gunicorn_server:app", "--config", "gunicorn.conf.py"]
