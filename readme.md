[![Build Status](https://travis-ci.org/UserNikita/easycode.svg?branch=master)](https://travis-ci.org/UserNikita/easycode)


### Запуск в докере

1. В папке с проектом выполнить команду
    ```bash
    docker-compose up -d
    ```


### Обновление на сервере pythonanywhere

1. Создать новую консоль

2. Активировать виртуальное окружение
    ```bash
    source env/bin/activate
    ```

3. Перейти в папку с проектом

4. Обновить код из репозитория
    ```bash
    git pull origin master
    ```

5. Выполнить миграции и собрать статику
    ```bash
    python manage.py migrate --settings=settings.env.prod_pythonanywhere
    python manage.py collectstatic --settings=settings.env.prod_pythonanywhere
    ``` 
    

### Измерение покрытия кода тестами

1. Запустить coverage
   ```bash
   coverage run --source='apps' manage.py test --settings=settings.env.test
   ```

2. Вывести отчёт в консоль
   ```bash
   coverage report -m 
   ```
   или сформировать отчёт в html формате
   ```bash
   coverage html
   ```


### Снятие дампа в фикстуры

1. Активировать виртуальное окружение
    ```bash
    source env/bin/activate
    ```

2. Выполнить команду
    ```bash
    python manage.py dumpdata library --indent=2 --output=./apps/library/fixtures/library_data.json --settings=settings.env.prod_pythonanywhere
    ```


### Построить диаграму моделей проекта для всех приложений

Данная возможность доступна только если проект запущен в докере

1. Войти в контейнер
    ```bash
    docker exec -ti easycode_web_1 bash
    ```

2. Выполнить команду
    ```bash
    python manage.py graph_models -a -g -o media/project_diagram.png
    ```