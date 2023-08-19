<div id="header" align="center">
  <h1>Referral System</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Django-3.2.20-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.14.0-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/PostgreSQL-555555?style=for-the-badge&logo=postgresql&logoColor=F5F5DC">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
</div>

# Данные проекта:
- Проект доступен по [адресу](http://kassschenko.pythonanywhere.com/api/)
- [Документация API](http://kassschenko.pythonanywhere.com/swagger/)
- Данные для админки
  ```
  login: 89962317857
  password: admin
  ```
# Описание API:
- **POST api/auth/**: Аутентификация по номеру телефона.
- **POST api/verify/**: СМС-верификация и получение JWT-токена.
- **GET api/users/**: Список пользователей.
- **GET api/users/me/**: Получить информацию о своём профиле.
- **POST /api/users/{code}/invitation/**: Активация инвайт-кода.
- **DELETE /api/users/{code}/invitation/**: Удаление инвайт-кода.
- **GET/api/users/{id}/**: Получить информацию о профиле по id.
- **/swagger/**: Документация.
# Запуск проекта:
- Клонируйте репозиторий и перейдите в него
- Перейдите в папку **infra** и проверьте, что файл .env заполнен данными представленными ниже:
  ```
  DEBUG=True
  ALLOWED_HOSTS=127.0.0.1
  SQLITE_SELECTED=False
  DB_ENGINE=django.db.backends.postgresql
  DB_NAME=postgres
  POSTGRES_USER=postgres
  DB_HOST=db
  DB_PORT=5432
  POSTGRES_PASSWORD=password
  ```
- Из папки **infra** запустите docker-compose 
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере web выполните миграции, создайте суперпользователя и соберите статику
  ```
  ~$ docker-compose exec web python manage.py makemigrations
  ~$ docker-compose exec web python manage.py migrate
  ~$ docker-compose exec web python manage.py createsuperuser
  ~$ docker-compose exec web python manage.py collectstatic --no-input
  ```

После этого проект будет доступен по url-адресу **127.0.0.1/api/**

Документация к API будет доступна по url-адресу **127.0.0.1/swagger/**
