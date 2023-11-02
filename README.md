<div id="header" align="center">
  <h1>Referral System</h1>
  <img src="https://img.shields.io/badge/Python-3.7.9-F8F8FF?style=for-the-badge&logo=python&logoColor=20B2AA">
  <img src="https://img.shields.io/badge/Django-3.2.20-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.14.0-F8F8FF?style=for-the-badge&logo=django&logoColor=00FF00">
  <img src="https://img.shields.io/badge/Docker-555555?style=for-the-badge&logo=docker&logoColor=2496ED">
</div>

# Запуск проекта:
- Клонируйте репозиторий и перейдите в него.
- Перейдите в папку **infra** и проверьте, что файл .env заполнен данными представленными ниже:
  ```
  DEBUG=True
  ALLOWED_HOSTS=127.0.0.1
  ```
- Из папки **infra** запустите docker-compose 
  ```
  ~$ docker-compose up -d --build
  ```
- В контейнере web выполните миграции, создайте суперпользователя и соберите статику
  ```
  ~$ docker-compose exec web python manage.py migrate
  ~$ docker-compose exec web python manage.py createsuperuser
  ~$ docker-compose exec web python manage.py collectstatic --no-input
  ```

После этого проект будет доступен по url-адресу [127.0.0.1](http://127.0.0.1/)

Документация к API будет доступна по url-адресу [127.0.0.1/api/docs](http://127.0.0.1/api/docs/)

# Описание API:
- **POST api/auth/**: Аутентификация по номеру телефона.
- **POST api/verify/**: СМС-верификация и получение JWT-токена.
- **GET api/users/**: Список пользователей.
- **GET api/user/me/**: Получить информацию о своём профиле.
- **GET/api/user/{id}/**: Получить информацию о профиле по id.
- **POST /api/user/invitation/**: Активация инвайт-кода.
- **DELETE /api/user/invitation/**: Удаление инвайт-кода.