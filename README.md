## ekb-radio-calculator - web-сайт калькулятор расчета стоимости размещения рекламы на радиостанциях.

---

### Возможности проекта:
- Выбор городов для размещения рекламы на радио.
- Выбор радиостанций на основе выбранного города.
- Отображение данных по выбранной радиостанции: лого, описание, числовые показатели и т.д.
- Калькулятор для расчета стоимости размещения рекламы на выбранной радиостанции с возможностью выбора различных параметров:
  - Селекторы и свитчеры для выбора необходимых параметров размещения.
  - Интерактивная таблица с возможностью бронирования рекламных мест.
  - Автоматический расчет стоимости рекламного размещения.
  - Формирование медиаплана в формате pdf для скачивания.
  - Отправка заявки с последующим уведомление в телеграм группу и на почту.
- Админ панель с возможностью редактирования данных радиостанций, справочников, системных данных и т.д.
- Импорт данных в базу данных с помощью Excel файла.

![web-service](https://github.com/mityasun/ekb-radio-calculator/raw/main/backend/media/sample/sample-web-service.png "Пример готового web-сервиса")

---

### Технологии
![Python](https://img.shields.io/badge/Python-3.12.3-%23254F72?style=for-the-badge&logo=python&logoColor=yellow&labelColor=254f72)
![Django](https://img.shields.io/badge/Django-5.0.4-0C4B33?style=for-the-badge&logo=django&logoColor=white&labelColor=0C4B33)
![Django REST](https://img.shields.io/badge/Django%20REST-3.15.1-802D2D?style=for-the-badge&logo=django&logoColor=white&labelColor=802D2D)
![REACT](https://img.shields.io/badge/React-18.2.0-23272F?style=for-the-badge&logo=react&logoColor=58C4DC&labelColor=23272F)
![PostGres](https://img.shields.io/badge/PostGres-31648D?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=31648D)
![Redis](https://img.shields.io/badge/Redis-D5362B?style=for-the-badge&logo=redis&logoColor=white&labelColor=D5362B)
![Nginx](https://img.shields.io/badge/Nginx-009400?style=for-the-badge&logo=nginx&logoColor=white&labelColor=009400)

---

### Документация интерфейса backend API [по ссылке](http://localhost/api/docs/)<br>
<sub>Ссылка откроется после развертывания проекта.</sub>

---

### Как запустить проект локально с помощью Doker compose:

Клонировать репозиторий и перейти в него в терминале:

```
git clone https://github.com/mityasun/ekb-radio-calculator.git
```

Перейдите в директорию с файлом docker compose:

```
cd ekb-radio-calculator/infra/
```

Создать файл .env в этой директории пропишите в нем:

```
SECRET_KEY=Секретный ключ Django
DEBUG=False для прода и True для тестов
ALLOWED_HOSTS=Список разрешенных хостов backend приложения
CSRF_TRUSTED_ORIGINS=Список разрешенных хостов для CSRF
CORS_ALLOWED_ORIGINS=Список разрешенных хостов для CORS
BOT_TOKEN=Токен телеграм бота для отправки заказов
CHAT_ID=id чата в телеграмм для отправки заказов (бот должен быть добавлен в чат)
NGINX_PORT=Порт Nginx
BACKEND_PORT=Порт backend приложения
REDIS_PORT=Порт Redis
REDIS_PASSWORD=Пароль для Redis
PG_ADMIN_PORT=Порт pgAdmin
PGADMIN_DEFAULT_EMAIL=Логин для входа в pgAdmin
PGADMIN_DEFAULT_PASSWORD=Пароль для входа в pgAdmin
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=Название базы данных 
POSTGRES_USER=Имя пользователя БД
POSTGRES_PASSWORD=Пароль пользователя БД
DB_HOST=postgres (название в соответствии с названием сервиса в docker compose)
DB_PORT=Порт базы данных
EMAIL_HOST=SMTP сервер для отправки email уведомлений
EMAIL_HOST_USER=Учетная запись на SMTP сервере (email адрес)
EMAIL_HOST_PASSWORD=Пароль от учетной записи на SMTP сервере
EMAIL_PORT=Порт SMTP сервера (25/465/567)
DEFAULT_FROM_EMAIL=Адрес email, с которого отправляется заказ
ORDER_TO_EMAIL=Адрес email для отправки заказов
```

Создать файл .redis в этой директории пропишите в нем:

```
port 123456 (Порт Redis)
bind redis
requirepass 12345 (Пароль Redis)
```

Запустите образы из файла docker compose:
```
docker-compose -f docker-compose.dev.yml up -d --build
```

Примените миграции:

```
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
```

Соберите статику:

```
docker-compose -f docker-compose.dev.yml exec backend python manage.py collectstatic --no-input
```

Создайте суперпользователя:

```
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser
```

Перейдите [на сайт](http://localhost/) или в [админ панель](http://localhost/admin/)

---

### Заполнение базы данных из Excel файла:

В [админ панели](http://localhost/admin/) перейдите в раздел: <br>
Настройки - Импорт данных - Добавить импорт данных и загрузите Excel файл, который должен соответствовать структуре файла примера:
```
cd ekb-radio-calculator/backend/media/sample/import-sample.xlsx
```

---

### Авторы проекта:
Backend: Петухов Артем [Github](https://github.com/mityasun)<br>
Frontend: Николай [Github](https://github.com/nickoff)
