FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
COPY dataset.csv .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONUNBUFFERED=1

CMD ["python", "train_model.py"] 
# && ["python", "cpu_load_train.py"] && ["python", "power_train.py"]
