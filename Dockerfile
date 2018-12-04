FROM python:3
ADD requirements/ /easycode/requirements/
WORKDIR /easycode
RUN pip install -r requirements/dev_docker.txt
# Инструкция по запуску без docker-compose
# Сборка образа
# docker build . --tag easycode
# Запуск командой
# docker run -ti -p 8000:8000 -v d:\projects\python\easycode:/easycode/ easycode python manage.py runserver 0.0.0.0:8000 --settings=settings.env.dev_docker