FROM python:3.7
ADD requirements/ /easycode/requirements/
WORKDIR /easycode
RUN apt-get update -y && apt-get install graphviz -y
RUN pip install -r requirements/dev_docker.txt