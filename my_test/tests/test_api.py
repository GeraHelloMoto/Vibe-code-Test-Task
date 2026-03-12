from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine, Base
from app import models
import pytest

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

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

def test_take_request_race_condition(client):
    db = SessionLocal()
    master = models.User(username="testmaster", full_name="Test", role="master")
    db.add(master)
    db.commit()
    master_id = master.id

    req = models.Request(clientName="Race", phone="111", address="addr", problemText="test", status="assigned", assignedTo=master_id)
    db.add(req)
    db.commit()
    req_id = req.id
    db.close()

    response1 = client.patch(f"/api/master/requests/{req_id}/take?master_id={master_id}")
    response2 = client.patch(f"/api/master/requests/{req_id}/take?master_id={master_id}")

    statuses = [response1.status_code, response2.status_code]
    assert 200 in statuses
    assert 409 in statuses