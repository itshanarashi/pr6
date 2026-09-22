# VoltMarket

## Практическая работа 6

Настроена RELEASE-версия проекта.
Добавлены PostgreSQL, Gunicorn и Nginx.
Проект запускается через Docker Compose.
При запуске выполняются миграции и сбор static-файлов.

## Запуск через Docker

```bash
cp .env.example .env
docker compose up --build -d
```

Проверка контейнеров:

```bash
docker compose ps
```

Сайт:

`http://localhost/`

Админ-панель:

`http://localhost/admin/`

Остановка:

```bash
docker compose down
```