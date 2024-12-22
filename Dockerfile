FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY .cache .
COPY main.py .
COPY config.py .

CMD ["python", "main.py"]