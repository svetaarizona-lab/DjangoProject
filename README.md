# ProjectA — Bookshop REST API

##  Опис проєкту

**ProjectA** — основний Django-проєкт книжкового магазину, реалізований як REST API.

Проєкт є частиною фінальної роботи, яка складається з двох незалежних Django-сервісів:

* **ProjectA** — основний сервіс книжкового магазину;
* **ProjectB** — додатковий сервіс керування складськими залишками.

ProjectA реалізує роботу з користувачами, категоріями та книгами, замовленнями, оплатою через Stripe, автентифікацією та авторизацією, кешуванням, фоновими задачами та моніторингом.

---

## Архітектура

Проєкт побудований за принципом контейнеризованої сервісної архітектури.

```text
                         ┌──────────────────┐
                         │      Client      │
                         │ Browser / API    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      NGINX       │
                         │ Reverse Proxy    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Gunicorn     │
                         │      Django      │
                         │      ProjectA    │
                         └───────┬───┬──────┘
                                 │   │
                    ┌────────────┘   └────────────┐
                    ▼                             ▼
             ┌──────────────┐              ┌──────────────┐
             │  PostgreSQL  │              │    Redis     │
             │   Database   │              │    Cache     │
             └──────────────┘              └──────┬───────┘
                                                  │
                                                  ▼
                                           ┌──────────────┐
                                           │    Celery    │
                                           │    Worker    │
                                           └──────────────┘

                         ProjectA
                             │
                             │ REST API
                             ▼
                         ProjectB
                     Warehouse Service
```

ProjectA та ProjectB працюють як окремі Django-проєкти та взаємодіють через REST API.

---

## 🚀 Основний функціонал

### Користувачі

* власна модель користувача на основі `AbstractUser`;
* реєстрація та авторизація;
* JWT authentication;
* розмежування доступу;
* групи та permissions;
* підтримка адміністратора.

### Книги

* створення книг;
* перегляд списку книг;
* перегляд деталей книги;
* редагування;
* видалення;
* категорії;
* автор;
* ціна;
* опис;
* кількість доступних книг;
* фільтрація;
* сортування;
* пагінація.

### Замовлення

* створення замовлень;
* робота з позиціями замовлення;
* зв'язок замовлення з користувачем;
* контроль кількості товару;
* збереження інформації про замовлення.

### Оплата

Інтегровано **Stripe Checkout**.

Передбачена обробка webhook-подій Stripe та оновлення статусу замовлення після успішної оплати.

---

## 🔐 Автентифікація

Для захисту REST API використовується **JWT authentication**.

Основний механізм:

```text
User
 │
 ├── Login
 │
 ▼
JWT Access Token
 │
 ▼
Authorization: Bearer <token>
 │
 ▼
Protected API endpoint
```

Захищені endpoint-и потребують валідного JWT access token.

---

## 📖 REST API

API побудований за допомогою Django REST Framework.

Основні ресурси:

```text
/api/books/
/api/categories/
/api/orders/
/api/auth/
```

Конкретний набір endpoint-ів визначається поточною конфігурацією API.

---

## 📑 Swagger / OpenAPI

Для документування REST API використовується `drf-spectacular`.

Swagger дозволяє:

* переглядати всі API endpoint-и;
* переглядати HTTP methods;
* переглядати параметри запитів;
* переглядати request/response schemas;
* тестувати API безпосередньо через браузер;
* працювати з JWT authentication.

OpenAPI schema використовується для автоматичної генерації документації.

---

## 🗄️ База даних

Проєкт використовує **PostgreSQL**.

Основні сутності:

```text
User
Category
Book
Order
OrderItem
```

Зв'язки між моделями реалізовані засобами Django ORM.

Міграції виконуються автоматично під час запуску Docker-контейнера.

---

## ⚡ Redis

**Redis** використовується як:

* backend для кешування;
* broker для Celery;
* result backend для Celery tasks.

Приклад логічної схеми:

```text
Django
  │
  ├── Cache ───────► Redis
  │
  └── Celery Task ─► Redis ─► Celery Worker
```

---

## 🔄 Celery

Для виконання фонових задач використовується **Celery**.

Окремо передбачені:

* Celery Worker;
* Celery Beat;
* Redis як message broker;
* Redis як result backend.

Фонові задачі дозволяють не блокувати основний HTTP request.

---

## 🌐 NGINX + Gunicorn

У production-конфігурації Django працює через **Gunicorn**.

NGINX використовується як reverse proxy.

```text
Client
   │
   ▼
 NGINX
   │
   ▼
Gunicorn
   │
   ▼
Django
```

NGINX також відповідає за обробку статичних файлів.

---

## 🐳 Docker

Проєкт повністю контейнеризований за допомогою Docker.

Основні сервіси:

```text
web
db
redis
celery
celery-beat
nginx
```

### Запуск

Перейти до каталогу ProjectA та виконати:

```bash
docker compose up --build
```

Для запуску у фоновому режимі:

```bash
docker compose up --build -d
```

Перевірити стан контейнерів:

```bash
docker compose ps
```

Переглянути логи:

```bash
docker compose logs
```

Логи окремого сервісу:

```bash
docker compose logs web
```

---

## 🧱 Структура проєкту

Основна структура ProjectA:

```text
ProjectA/
│
├── shop/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tasks.py
│   ├── urls.py
│   ├── views.py
│   └── tests/
│
├── project/
│   ├── settings/
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── nginx/
│   └── default.conf
│
├── docker-compose.yml
├── Dockerfile
├── docker-entrypoint.sh
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🌍 Internationalization

Проєкт підтримує міжнародність Django.

Передбачена можливість роботи щонайменше з двома мовами.

Використовуються стандартні механізми Django:

```python
LANGUAGE_CODE
LANGUAGES
USE_I18N
```

---

## 🔒 Permissions та Groups

Для контролю доступу використовуються Django permissions та groups.

Приклад ролі:

```text
Admin
User
```

Доступ до захищених операцій залежить від прав користувача.

---

## 💳 Stripe

Проєкт інтегрований зі Stripe Checkout.

Основний процес:

```text
User
 │
 ▼
Create Order
 │
 ▼
Stripe Checkout Session
 │
 ▼
Payment
 │
 ▼
Stripe Webhook
 │
 ▼
ProjectA
 │
 ▼
Update Order
```

Секретні ключі Stripe зберігаються в environment variables та не повинні потрапляти до Git repository.

---

## 🚨 Sentry

Для моніторингу помилок використовується **Sentry**.

Sentry дозволяє:

* відстежувати exceptions;
* отримувати stack trace;
* бачити URL запиту;
* аналізувати помилки production-середовища;
* контролювати стабільність застосунку.

Для перевірки інтеграції передбачений тестовий endpoint.

---

## 🧪 Testing

Для тестування використовується:

* `pytest`;
* `pytest-django`;
* `factory_boy`;
* mocking для зовнішніх сервісів.

Тести охоплюють основний функціонал проєкту:

* моделі;
* API;
* authentication;
* permissions;
* orders;
* Stripe;
* views;
* background tasks.

Запуск тестів:

```bash
docker compose exec web pytest
```

Перевірка coverage:

```bash
docker compose exec web pytest --cov=.
```

---

## 🔧 Environment Variables

Конфіденційні параметри не зберігаються безпосередньо в коді.

Використовуються environment variables.

Приклад:

```text
DEBUG=
SECRET_KEY=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=

REDIS_URL=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

SENTRY_DSN=
```

Файл `.env` не повинен додаватися до Git repository.

---

## 🔗 Взаємодія з ProjectB

ProjectA є основним сервісом системи.

ProjectB відповідає за складський облік.

Взаємодія відбувається через REST API:

```text
┌──────────────────────┐
│       ProjectA       │
│      Bookshop API    │
└──────────┬───────────┘
           │
           │ HTTP REST API
           ▼
┌──────────────────────┐
│       ProjectB       │
│ Warehouse / Inventory│
└──────────────────────┘
```

ProjectA передає інформацію про книги/товари, а ProjectB відповідає за їх складські залишки.

---

## 📊 Основні технології

| Технологія            | Призначення       |
| --------------------- | ----------------- |
| Python                | Основна мова      |
| Django                | Web framework     |
| Django REST Framework | REST API          |
| PostgreSQL            | Database          |
| Redis                 | Cache / Broker    |
| Celery                | Background tasks  |
| Celery Beat           | Scheduled tasks   |
| Docker                | Containerization  |
| Docker Compose        | Orchestration     |
| NGINX                 | Reverse proxy     |
| Gunicorn              | WSGI server       |
| JWT                   | Authentication    |
| Stripe                | Payments          |
| drf-spectacular       | OpenAPI / Swagger |
| Sentry                | Error monitoring  |
| pytest                | Testing           |
| factory_boy           | Test factories    |

---

## ▶️ Швидкий запуск

### 1. Клонувати repository

```bash
git clone <repository-url>
```

### 2. Перейти до ProjectA

```bash
cd ProjectA
```

### 3. Створити `.env`

Додати необхідні environment variables.

### 4. Запустити Docker Compose

```bash
docker compose up --build -d
```

### 5. Перевірити контейнери

```bash
docker compose ps
```

### 6. Перевірити API

Відкрити API у браузері або через Swagger.

---

## 📚 API Documentation

Документація REST API доступна через Swagger/OpenAPI.

Swagger UI використовується для перегляду та тестування endpoint-ів.

OpenAPI schema дозволяє інтегрувати API з іншими клієнтами та сервісами.

---

## 🛡️ Production considerations

Для production-середовища передбачено:

* `DEBUG=False`;
* Gunicorn замість Django development server;
* NGINX reverse proxy;
* PostgreSQL;
* Redis;
* Celery;
* environment variables;
* Sentry monitoring;
* static files через NGINX;
* Docker containers.

---

## 📌 Project Status

ProjectA реалізує основну частину функціоналу книжкового магазину та підготовлений до інтеграції з ProjectB.

Основні компоненти:

* ✅ Django
* ✅ Django REST Framework
* ✅ PostgreSQL
* ✅ Redis
* ✅ Celery
* ✅ Celery Beat
* ✅ Docker
* ✅ Docker Compose
* ✅ NGINX
* ✅ Gunicorn
* ✅ JWT authentication
* ✅ Permissions / Groups
* ✅ Swagger / OpenAPI
* ✅ Stripe Checkout
* ✅ Stripe Webhook
* ✅ Sentry
* ✅ i18n
* ✅ API testing
* ✅ ProjectB REST API integration

---

## 👩‍💻 Автор

Final Django REST API project.

**ProjectA — Bookshop**
