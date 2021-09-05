FROM python:3.9.5-alpine

# setting up workdir, better for multistage builds
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GOOGLE_APPLICATION_CREDENTIALS ./spring-gift-270312-95978d74290d.json
# setting stage variables for django
ENV DEBUG_MODE=false

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000


CMD python manage.py migrate && \
        gunicorn Youtube.wsgi:application --bind 0.0.0.0:8000