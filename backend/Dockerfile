FROM python:3.12.3-alpine3.19

WORKDIR /backend

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

LABEL project='backend' version=1.0

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000", "--timeout", "180"]