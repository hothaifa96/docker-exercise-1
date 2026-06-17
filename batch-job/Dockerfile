FROM python:3.14.5-alpine3.23

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY generator.py .

ENV TARGET_DIR='/data'

CMD ["python3","generator.py"]