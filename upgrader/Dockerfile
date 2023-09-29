FROM python:3-slim

WORKDIR /app

COPY main.py main.py
COPY requirements.txt requirements.txt

RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]

ENTRYPOINT [ "python3", "main.py" ]
