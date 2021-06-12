FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python -m pip install --upgrade pip

COPY ./app /app/app
COPY requirements.txt /app
COPY setup.py /app

RUN python -m pip --disable-pip-version-check --no-cache-dir install /app/

WORKDIR /app

ENV APP_MODULE=app.producer.main:app
