# Lab2 — Microservices E-commerce (Kafka + PostgreSQL)

Сервисы:

- Auth (Identity): `http://localhost:8001`
- Product (Catalog): `http://localhost:8002`
- Inventory (Stock): `http://localhost:8003`
- Order: `http://localhost:8004`
- Payment: `http://localhost:8005`
- Notification: `http://localhost:8006`

## Запуск

1) Запуск инфраструктуры и сервисов:

```bash
docker compose up --build
```

2) Swagger:

- Auth: `http://localhost:8001/docs`
- Product: `http://localhost:8002/docs`
- Inventory: `http://localhost:8003/docs`
- Order: `http://localhost:8004/docs`
- Payment: `http://localhost:8005/docs`
- Notification: `http://localhost:8006/docs`

## Быстрый старт (admin)

Для CRUD в Catalog/Inventory нужны права `admin`. В этой лабе роль задается при регистрации:

- POST `auth-service` → `/auth/register` с полем `role: "admin"`.

## Kafka

Order service публикует события в topic `order-events`. Notification service слушает этот topic и сохраняет уведомления в свою БД.
