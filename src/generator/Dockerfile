FROM python:3.11.2-slim as build-stage

WORKDIR /generator

RUN pip install --upgrade pip

RUN apt-get update

RUN apt-get install -y curl

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--access-log", "--proxy-headers"]
