FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /thestartupfellows_b
COPY requirements.txt requirements.txt
RUN apt-get update \
&& pip3 install -r requirements.txt

COPY . .
CMD flask db init ; \
flask db stamp head && \
flask db migrate && \
flask db upgrade && \
gunicorn --workers 1 --timeout 120 -b 0.0.0.0:5000 --reload thestartupfellows:app
