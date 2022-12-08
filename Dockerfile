FROM python:3.8.0-slim

RUN apt-get update \
    && apt-get install -y \
        cmake libsm6 libxext6 libxrender-dev protobuf-compiler \
    && rm -r /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /app

CMD ["uvicorn", "server:app"]

