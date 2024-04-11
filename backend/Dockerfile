FROM python:3.11.8

EXPOSE 8000

COPY ./requirements.txt /

RUN pip install --no-cache-dir pipenv==2023.10.3 \
  pipenv install -r requirements.txt

COPY ./app/ /app

WORKDIR /app

CMD [ "python", "main.py"]
