import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from db import get_db, Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_generate_script(client):
    response = client.post(
        "/scripts/generate-script",
        json={"input_text": "Create a hello world function"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["input_text"] == "Create a hello world function"
    assert "generated_code" in data
    assert "def main():" in data["generated_code"]

def test_generate_script_empty_input(client):
    response = client.post(
        "/scripts/generate-script",
        json={"input_text": ""}
    )
    assert response.status_code == 200  # Should still work with empty input