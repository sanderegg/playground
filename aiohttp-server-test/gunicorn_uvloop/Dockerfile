FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn.conf.py ./

EXPOSE 8080

CMD ["gunicorn", "aiohttp_app:app", "--config", "gunicorn.conf.py"]
