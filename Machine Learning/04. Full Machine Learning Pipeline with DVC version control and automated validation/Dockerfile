FROM ghcr.io/mlflow/mlflow:v3.10.0

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
