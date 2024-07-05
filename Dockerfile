FROM python:3.12-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    libffi-dev \
    libssl-dev \
    make \
    docker.io \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf from the official repository
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.pip ./requirements.pip
RUN pip install --upgrade pip && \
    pip install -r requirements.pip

COPY ./run.py ./run.py
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]