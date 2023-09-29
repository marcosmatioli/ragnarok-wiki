FROM python:3-slim

WORKDIR /app

COPY main.py main.py
COPY requirements.txt requirements.txt
COPY templates/ templates/

RUN ["python3", "-m", "pip", "install", "-r", "requirements.txt"]

ENTRYPOINT [ "python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0" ]
