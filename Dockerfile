FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"
ENV HOST="0.0.0.0"
ENV PORT=8000

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt
EXPOSE ${PORT}

CMD python manage.py runserver ${HOST}:${PORT}