
FROM python:3.9-slim-buster
LABEL maintainer "Beng Hau Tan, benghau@starboardventures.io"

# set working directory in container
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Copy app folder to app folder in container
COPY /app /usr/src/app/

# Changing to non-root user
RUN useradd -m appUser
USER appUser

# For running on Heroku
# CMD gunicorn --bind 0.0.0.0:$PORT app:server
CMD gunicorn --bind 0.0.0.0:8050 app:server