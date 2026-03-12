import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture
def client():
    # Создаём таблицы перед тестом
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)