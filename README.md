# Книжковий магазин

Навчальний Django-проєкт для перегляду книжок, керування кошиком і створення замовлень через Stripe Checkout.

## Запуск проєкту

1. Створіть та активуйте віртуальне середовище Python.
2. Встановіть залежності: `pip install -r requirements.txt`.
3. Створіть файл `.env` із параметрами бази даних та ключами Stripe.
4. Виконайте міграції: `python manage.py migrate`.
5. Запустіть сервер: `python manage.py runserver`.

## Тести та coverage

Запуск тестів:

```bash
pytest
```

Перевірка coverage моделей:

```bash
pytest --cov=shop.models --cov-report=term-missing
```

## AI Usage

AI використано як помічник для code review трьох складних views, генерації та перевірки тестів моделей, написання docstrings і оновлення документації. Остаточні рішення перевірено та відредаговано вручну.

Використані промпти наведені у файлі `AI_PROMPTS.md`, а результати review — у `AI_REVIEW.md`.
