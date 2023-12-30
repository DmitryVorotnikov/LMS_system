FROM python:3

WORKDIR /lms_system

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
