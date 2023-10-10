# Сервис доставки грузов
Сервис разработан на Django Rest Framework с Celery/RabbitMQ и с Swagger docs

## Установка и запуск

1. Склонировать репозиторий с Github
2. Перейти в директорию проекта
3. Создать файл .env заполнить в нем поля, на основе env.cope
4. Запустить контейнеры
```
sudo docker-compose up -d
```
5. Остановка работы контейнеров
```
sudo docker-compose stop
```
***
```http://0.0.0.0:8000/swagger/``` - Документация ко всем endpoints

