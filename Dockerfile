FROM python:3.7

ENV JANGO_PORT=8000

RUN mkdir /app

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE $JANGO_PORT

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:$JANGO_PORT