FROM python:3.6-slim

WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install python-dev
RUN pip install Flask
RUN pip install psycopg2-binary
RUN pip install -U flask-cors
RUN pip install flask-bcrypt

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
