[![Build Status](https://travis-ci.org/UserNikita/easycode.svg?branch=master)](https://travis-ci.org/UserNikita/easycode)


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