FROM python:3.8

RUN python -m pip install --upgrade pip

COPY ./app /app/app
COPY requirements.txt /app
COPY setup.py /app

RUN python -m pip --disable-pip-version-check --no-cache-dir install /app/

WORKDIR /app

ENTRYPOINT ["python", "app/consumer/main.py"]
