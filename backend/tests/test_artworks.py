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

def test_generate_artwork_english(client):
    response = client.post(
        "/artworks/generate-art",
        json={
            "input_spec": "Create a blue circle with white text",
            "spec_type": "english"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["input_spec"] == "Create a blue circle with white text"
    assert data["spec_type"] == "english"
    assert "React" in data["generated_code"]

def test_generate_artwork_yaml(client):
    yaml_spec = """
shape: circle
color: blue
text: Hello World
"""
    response = client.post(
        "/artworks/generate-art",
        json={
            "input_spec": yaml_spec,
            "spec_type": "yaml"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["spec_type"] == "yaml"
    assert "canvas" in data["generated_code"].lower()