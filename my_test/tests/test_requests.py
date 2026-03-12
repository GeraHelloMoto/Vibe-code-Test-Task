def test_create_request(client):
    response = client.post("/api/requests/", json={
        "clientName": "Тест",
        "phone": "123",
        "address": "Адрес",
        "problemText": "Проблема"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["clientName"] == "Тест"
    assert data["status"] == "new"

def test_dispatcher_assign_and_cancel(client):
    # Создаём заявку
    response = client.post("/api/requests/", json={
        "clientName": "ДиспетчерТест",
        "phone": "999",
        "address": "Тестовый адрес",
        "problemText": "Проблема для диспетчера"
    })
    assert response.status_code == 200
    req_id = response.json()["id"]

    # Назначаем мастера (ID 2 должен существовать в сидах)
    response = client.patch(f"/api/dispatcher/requests/{req_id}/assign?master_id=2")
    assert response.status_code == 200
    # Проверяем статус
    response = client.get("/api/requests/")
    requests = response.json()
    req = next(r for r in requests if r["id"] == req_id)
    assert req["status"] == "assigned"
    assert req["assignedTo"] == 2

    # Отменяем заявку
    response = client.patch(f"/api/dispatcher/requests/{req_id}/cancel")
    assert response.status_code == 200
    response = client.get("/api/requests/")
    requests = response.json()
    req = next(r for r in requests if r["id"] == req_id)
    assert req["status"] == "canceled"