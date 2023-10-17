# pull official base image
FROM python:3.11.4
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get clean 

# install dependencies
RUN pip install --upgrade pip

# set work directory
WORKDIR /sigma

COPY ./requirements.txt /sigma
RUN pip install -r requirements.txt --no-cache-dir

COPY ./docker-entrypoint.sh /sigma
COPY ./worker-entrypoint.sh /sigma
# copy project
COPY . /sigma/

RUN chmod +x /sigma/docker-entrypoint.sh
RUN chmod +x /sigma/worker-entrypoint.sh


