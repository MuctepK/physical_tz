# Тестовое задание для Physical
Для запуска проекта установите: docker, docker-compose, git


Для того чтобы клонировать содержимое репозитория выполните команду:
```bash
git clone https://github.com/MuctepK/physical_tz .
```

После клонирования перейдите в склонированную папку и вывполните следующие команды:

Соберите контейнеры
```bash
docker-compose build
```
Запустите контейнеры
```bash
docker-compose up
```
После, вы можете запустить тесты
```
docker-compose run --rm --entrypoint pytest web api/tests.py
```


Данные для входа в админку:
```
Username: admin
password: admin
```