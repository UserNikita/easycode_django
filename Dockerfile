FROM python:3.10
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install graphviz -y
WORKDIR /app
ADD requirements /app/requirements/
RUN pip install -r requirements/dev_docker.txt
