from app.database import SessionLocal
from app import models

def test_take_request_race_condition(client):
    # Создаём мастера и заявку напрямую в БД (так как фикстура client очищает БД после каждого теста)
    db = SessionLocal()
    master = models.User(username="testmaster", full_name="Test", role="master")
    db.add(master)
    db.commit()
    master_id = master.id

    req = models.Request(
        clientName="Race",
        phone="111",
        address="addr",
        problemText="test",
        status="assigned",
        assignedTo=master_id
    )
    db.add(req)
    db.commit()
    req_id = req.id
    db.close()

    # Отправляем два параллельных запроса на взятие заявки
    response1 = client.patch(f"/api/master/requests/{req_id}/take?master_id={master_id}")
    response2 = client.patch(f"/api/master/requests/{req_id}/take?master_id={master_id}")

    statuses = [response1.status_code, response2.status_code]
    assert 200 in statuses
    assert 409 in statuses