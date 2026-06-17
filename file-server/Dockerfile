FROM python:3.14.5-alpine3.23

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY server.py .

EXPOSE 8080

CMD ["python3","server.py"]