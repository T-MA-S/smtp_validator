FROM python:3.10.10-slim

WORKDIR /code

COPY requirements.txt .

RUN apt-get update &&  apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
