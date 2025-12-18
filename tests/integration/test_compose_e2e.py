import os
import time
import uuid

import pytest
import requests


BASE_AUTH = os.getenv("AUTH_URL", "http://localhost:8001")
BASE_PRODUCT = os.getenv("PRODUCT_URL", "http://localhost:8002")
BASE_INVENTORY = os.getenv("INVENTORY_URL", "http://localhost:8003")
BASE_ORDER = os.getenv("ORDER_URL", "http://localhost:8004")
BASE_PAYMENT = os.getenv("PAYMENT_URL", "http://localhost:8005")
BASE_NOTIFICATION = os.getenv("NOTIFICATION_URL", "http://localhost:8006")


def _wait_ok(url: str, timeout_s: int = 120) -> None:
    deadline = time.time() + timeout_s
    last_err: str | None = None
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
            last_err = f"status={r.status_code} body={r.text[:200]}"
        except Exception as e:
            last_err = str(e)
        time.sleep(2)
    raise AssertionError(f"Service not ready: {url}. Last error: {last_err}")


def _post_json(url: str, payload: dict, headers: dict | None = None) -> requests.Response:
    return requests.post(url, json=payload, headers=headers or {}, timeout=15)


def _get_json(url: str, headers: dict | None = None) -> requests.Response:
    return requests.get(url, headers=headers or {}, timeout=15)


@pytest.mark.integration
def test_compose_happy_path_smoke() -> None:
    # Wait for services
    _wait_ok(f"{BASE_AUTH}/health")
    _wait_ok(f"{BASE_PRODUCT}/health")
    _wait_ok(f"{BASE_INVENTORY}/health")
    _wait_ok(f"{BASE_ORDER}/health")
    _wait_ok(f"{BASE_PAYMENT}/health")
    _wait_ok(f"{BASE_NOTIFICATION}/health")

    # 1) Register admin
    suffix = uuid.uuid4().hex[:10]
    admin_email = f"admin_{suffix}@example.com"
    user_email = f"user_{suffix}@example.com"
    password = "test123"

    r = _post_json(
        f"{BASE_AUTH}/auth/register",
        {"email": admin_email, "password": password, "role": "admin"},
    )
    assert r.status_code == 200, r.text
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2) Create category + product (admin)
    r = _post_json(f"{BASE_PRODUCT}/catalog/categories", {"name": f"cat_{suffix}"}, headers=admin_headers)
    assert r.status_code in (200, 409), r.text

    r = _post_json(
        f"{BASE_PRODUCT}/catalog/products",
        {
            "sku": f"SKU-{suffix}",
            "name": f"Product {suffix}",
            "description": "Test product",
            "price_cents": 1234,
            "category_id": None,
        },
        headers=admin_headers,
    )
    assert r.status_code == 200, r.text
    product_id = int(r.json()["id"])

    # 3) Set inventory (admin)
    r = _post_json(
        f"{BASE_INVENTORY}/inventory/set",
        {"product_id": product_id, "quantity": 10},
        headers=admin_headers,
    )
    assert r.status_code == 200, r.text

    # 4) Register normal user and create an order
    r = _post_json(
        f"{BASE_AUTH}/auth/register",
        {"email": user_email, "password": password, "role": "user"},
    )
    assert r.status_code == 200, r.text
    user_token = r.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}

    r = _post_json(
        f"{BASE_ORDER}/orders",
        {"items": [{"product_id": product_id, "quantity": 1}]},
        headers=user_headers,
    )
    assert r.status_code == 200, r.text
    order = r.json()
    order_id = int(order["id"])
    assert order["user_id"] >= 1
    assert order["status"] in ("paid", "payment_failed", "created")
    assert order["total_cents"] == 1234

    # 5) Notification eventually appears (Kafka -> notification-service)
    deadline = time.time() + 60
    while time.time() < deadline:
        r = _get_json(f"{BASE_NOTIFICATION}/notifications")
        assert r.status_code == 200, r.text
        notifications = r.json()
        if any(int(n.get("order_id")) == order_id for n in notifications):
            return
        time.sleep(2)

    raise AssertionError("Expected notification not found")
