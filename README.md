# REST API Сервис поиска ближайших машин для перевозки грузов.

# Описание проекта
### Приложение, которое по ZIP коду отправления находит ближайшие автомобили.

### Стек технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)

## Краткое описание функционала:
### Уровень 1

Сервис поддерживает следующие базовые функции:

- Создание нового груза (характеристики локаций pick-up, delivery определяются 
  по введенному zip-коду); ```http://127.0.0.1:8000/api/v1/cargos/```
- Получение списка грузов (локации pick-up, delivery, количество ближайших 
  машин до груза ( =< 450 миль)`Поле nearest_trucks`); ```http://127.0.0.1:8000/api/v1/cargos/```
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, 
  вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза`поле all_trucks`); ```http://127.0.0.1:8000/api/v1/cargos/<id>```
- Редактирование машины по ID (локация (определяется по введенному zip-коду)); ```http://127.0.0.1:8000/api/v1/trucks/<id>```
- Редактирование груза по ID (вес, описание); ```http://127.0.0.1:8000/api/v1/cargos/<id>```
- Удаление груза по ID. ```http://127.0.0.1:8000/api/v1/cargos/<id>```
- Получение всех локаций ``http://127.0.0.1:8000/api/v1/locations/`` реализовано с пагинацией. Выводится по 100 объектов, для просмотра следующих нужно в url передавать параметр ?page=1, 2, и тд

### Уровень 2

Все что в уровне 1 + дополнительные функции:

- Фильтр списка грузов (вес, мили ближайших машин до грузов);`Параметры передаются в url:` ```http://127.0.0.1:8000/api/v1/cargos/<id>/?weight=10&&?distance=1000```
- Автоматическое обновление локаций всех машин раз в 3 минуты (локация 
  меняется на другую случайную). ``Реализовано на Celery``

## Запуск в docker контейнерах (django, redis, celery, nginx, postgres):

- Если докер не установлен, то устанавливаем:
```bash
sudo apt update && sudo apt upgrade -y
sudo wget -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo wget -SL https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64 -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose
```

- Клонируем репозиторий:
```bash
git@github.com:potapovjakov/delivery_service.git
```

- Переходим в папку со склонированным проектом 
```bash
сd delivery_service
```
  В папке присутствует файл ```.env.example```. Переименовываем его в ```.env``` (Так делать с чувствительными данными нельзя, но в этом проекте можно%)
```bash
mv .env.example .env
```

- еще раз все проверяем и запускаем командой:
```bash
docker-compose up --build
``` 

- Приложение создаст базу данных и заполнит таблицу локаций значениями из csv файла. 
- Так же добавятся 20 автомобилей со случайными характеристиками (ручное добавление не реализовывал, так как не было в ТЗ)
  и будет доступно по адресу ``http://127.0.0.1:8000/api/v1/trucks/``

- Для остановки приложения запустить команду:
```bash
docker-compose down
``` 
- Либо Ctrl+C в терминале


### Если приложение не останавливать, то:
- Celery будет каждые 3 минуты обновлять локации всех автомобилей случайным образом

## Документация API находится по адресу ``http://127.0.0.1:8000/swagger/``
#### Выполнил [Яков Потапов](https://github.com/potapovjakov)
