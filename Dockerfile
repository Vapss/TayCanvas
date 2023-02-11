FROM python:3.10-slim-bullseye
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/app

WORKDIR /code/app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
