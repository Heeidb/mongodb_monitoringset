#Dockerfile

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y python3-pip 
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "/app/replica_set_metrics.py"]
