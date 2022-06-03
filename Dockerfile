FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

COPY . /app

EXPOSE 8050

CMD ["python", "app.py"]