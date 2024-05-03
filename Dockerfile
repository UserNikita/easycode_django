FROM python:3.10
WORKDIR /app
ADD requirements /app/requirements/
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install graphviz -y
RUN pip install -r requirements/dev_docker.txt
