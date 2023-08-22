# Foodgram

### Описание

«Продуктовый помощник»: приложение, на котором пользователи публикуют рецепты кулинарных изделий, подписываться на публикации других авторов и добавлять рецепты в свое избранное. Сервис «Список покупок» позволит пользователю создавать список продуктов, которые нужно купить для приготовления выбранных блюд согласно рецепта/ов.
Деплой приложения реализован с помощью контейнеризации. Применена автоматизация проекта: CI/CD.

#### Технологии использованные в проекте:

* Python
* Django
* DRF
* Nginx
* Gunicorn
* Docker
* Workflow

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/BankaiSS/foodgram-project-react
```

```
cd kittygram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Сайт доступен по адресу: 
https://foodgrambankai.hopto.org/

Доступ в админку:
login: testadmin@mail.ru
password: admin

Автор: Baibanov Eldar