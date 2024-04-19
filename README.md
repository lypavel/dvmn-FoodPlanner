# Продажа букетов через телеграм-бота

Телеграм-бот, с помощью которого можно просматривать кулинарные рецепты.

## Пример взаимодействия с ботом

![FlowerBot-Example]()

## Установка

1. Скачайте код с репозитория.
2. Установите Python [3.10.12](https://www.python.org/downloads/release/python-31012/)
3. Установите все необходимые зависимости с помощью `pip` (или `pip3`)

```bash
pip install -r requirements.txt
```

### Задайте переменные окружения в файле `.env`
О том, как получить токен для телеграм бота, вы можете узнать в [документации к Telegram Bot API](https://core.telegram.org/bots/features#botfather).

```
SECRET_KEY='SECRET_KEY'
TELEGRAM_BOT_TOKEN='TELEGRAM_BOT_TOKEN'  # токен телеграм-бота
```

## Как запустить

1. Наполните базу данных, с которой должен будет работать бот (или используйте нашу [тестовую]()).
2. Создайте суперпользователя для доступа в Django-админку:
    ```python
    python3 manage.py createsuperuser
    ```
3. Создайте и примените миграции
    ```python
    python3 manage.py makemigrations
    ```
    ```python
    python3 manage.py migrate
    ```
4. Запустите телеграм-бота:
    ```python
    python3 python3 manage.py bot
    ```
5. Запустите сервер Django для работы с базой данных:
    ```python
    python3 manage.py runserver 0:8000
    ```
    Админ-интерфейс будет доступен по адресу `127.0.0.1:8000/admin`.<br>
    Для доступа используйте логин и пароль, созданный в п.2.
***
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [Devman](dvmn.org).
