
# Установка Django

pip install django
poetry add django

# Проверка установки
django-admin --version

# Создание проекта
django-admin startproject config .

# Запуск проекта
python manage.py runserver

# Создание приложения
python manage.py startapp store_app

# Применение миграции
python manage.py migrate

# Создание миграции
python manage.py makemigrations


# Создание суперпользователя
python manage.py createsuperuser

# Интерактивная консоль Django
python manage.py shell

# Создание загрузки данных в бд из json
# 1. создать файл store_fixture.json
python manage.py loaddata ./store_fixture.json

# Выгрузка даннных в json
python manage.py dumpdata > ./store_fixture.json
python manage.py dumpdata --indent 4> ./store_fixture.json
python manage.py dumpdata store_app --indent 4> ./store_fixture.json
python manage.py dumpdata store_app.Product --indent 4> ./store_fixture.json


<h5><a href="{% url 'product_detail' product.id %}">{{ product.name }}</a></h5>

# Базовая команда (ищет store_app/fixtures/store_fixture.json)
python manage.py load_store_data

# Указать конкретный файл
python manage.py load_store_data --file=/путь/к/файлу.json

# Очистить старые данные перед загрузкой
python manage.py load_store_data --clear

# Указать другое приложение
python manage.py load_store_data --app=other_app

# Показать help
python manage.py load_store_data --help