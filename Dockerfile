FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"

ENV HOST="0.0.0.0"
ENV PORT=8000

ENV DB_PASSWORD=root
ENV DB_USER=postgres
ENV DB_DBNAME=astra
ENV DB_PORT=5432
ENV DB_HOST=db
ENV DEBUG=True

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD python -u start_server.py