FROM python:3-slim

WORKDIR /app

COPY main.py main.py
COPY requirements.txt requirements.txt
COPY docker-entrypoint.sh /

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -r requirements.txt
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]
