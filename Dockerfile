FROM python:3.7
WORKDIR /

COPY . /
RUN python3 -m pip install -r requirements.txt
ENV PORT 8080

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 server:app 