FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"

ENV HOST="0.0.0.0"
ENV PORT=8000

ENV DB_HOST=192.168.1.62
ENV DB_DBNAME=knox_auth
ENV DB_PASSWORD=root
ENV DB_USER=postgres
ENV DB_PORT=5432
ENV DEBUG=True

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD python start_server.py