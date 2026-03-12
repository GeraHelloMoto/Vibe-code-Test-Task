from app.database import SessionLocal
from app import models

def seed_data():
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        dispatcher = models.User(username="dispatcher", full_name="Диспетчер Иванов", role="dispatcher")
        master1 = models.User(username="master1", full_name="Мастер Петров", role="master")
        master2 = models.User(username="master2", full_name="Мастер Сидоров", role="master")
        db.add_all([dispatcher, master1, master2])
        db.commit()

        req1 = models.Request(
            clientName="Клиент А",
            phone="111",
            address="ул. Ленина, д.1",
            problemText="Не работает стиральная машина",
            status="new"
        )
        req2 = models.Request(
            clientName="Клиент Б",
            phone="222",
            address="ул. Пушкина, д.2",
            problemText="Течет кран",
            status="assigned",
            assignedTo=master1.id
        )
        req3 = models.Request(
            clientName="Клиент В",
            phone="333",
            address="ул. Толстого, д.3",
            problemText="Сломался холодильник",
            status="in_progress",
            assignedTo=master2.id
        )
        db.add_all([req1, req2, req3])
        db.commit()
    db.close()