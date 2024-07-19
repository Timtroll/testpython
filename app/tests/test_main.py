import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app import models, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_meme():
    response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"
    assert response.json()["description"] == "Test Description"
    assert response.json()["image_url"] == "http://test.com/image.jpg"

def test_read_memes():
    response = client.get("/memes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_meme():
    # Сначала создадим мем для тестирования
    response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
    meme_id = response.json()["id"]
    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Meme"
    assert response.json()["description"] == "Test Description"
    assert response.json()["image_url"] == "http://test.com/image.jpg"

def test_update_meme():
    # Сначала создадим мем для тестирования
    response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
    meme_id = response.json()["id"]
    response = client.put(f"/memes/{meme_id}", json={"title": "Updated Meme", "description": "Updated Description", "image_url": "http://test.com/updated_image.jpg"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Meme"
    assert response.json()["description"] == "Updated Description"
    assert response.json()["image_url"] == "http://test.com/updated_image.jpg"

def test_delete_meme():
    # Сначала создадим мем для тестирования
    response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
    meme_id = response.json()["id"]
    response = client.delete(f"/memes/{meme_id}")
    assert response.status_code == 200
    response = client.get(f"/memes/{meme_id}")
    assert response.status_code == 404
