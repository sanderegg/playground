FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY uvloop_server.py gunicorn.conf.py ./

EXPOSE 8080

CMD ["gunicorn", "uvloop_server:app", "--config", "gunicorn.conf.py"]
