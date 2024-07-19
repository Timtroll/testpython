# Meme Collection API

## ��������
���-���������� ��� ������ � ���������� �����. ���������� ��������� ���������, ���������, ������� � ������������� ����.

## ����������������

- **GET /memes**: �������� ������ ���� ����� (� ����������).
- **GET /memes/{id}**: �������� ���������� ��� �� ��� ID.
- **POST /memes**: �������� ����� ��� (� ��������� � �������).
- **PUT /memes/{id}**: �������� ������������ ���.
- **DELETE /memes/{id}**: ������� ���.

## ������ �������

���������� �����������:

```bash
pip install -r requirements.txt
```

��������� ���������� ���������:
�������� ���� .env � �������� ���������� ������� � �������� ����������� ���������� ���������. ������:

```bash
DATABASE_URL=sqlite:///./test.db
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
``````

����������� ����������� ���������:

```bash
python -m venv venv
source venv/bin/activate
```

��������� ����������:

```bash
cd /home/troll/disk/work/testpython1
uvicorn app.main:app --reload
```

--reload - ��������� ��������� ��������� � ������� ��� ������������

### ��������� ������

1. ���������� �����������.
2. ��������� ���������� ��������� ��� ���� ������ � S3.
3. ��������� Docker Compose:

```bash
docker-compose up --build
```
***

��� ������������ ������ FastAPI ���������� ����� ������������ ������ `pytest` ������ � �������� ������������, ������� ������������� FastAPI. ��� ��� ����� �������� ����� ��� ������ ����������:

1. **���������� ����������� �����������:**

   ���������, ��� � ��� ����������� `pytest` � `httpx`:

   ```
   pip install pytest httpx
   ```

2. **�������� ���� ������, ��������, `test_main.py`:**

   ```
   fastapi.testclient import TestClient
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   from .main import app, get_db
   from . import models, schemas
   
   # ���������� ���� ������ ��� ������������ (� ������)
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
       # ������� �������� ��� ��� ������������
       response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
       meme_id = response.json()["id"]
       response = client.get(f"/memes/{meme_id}")
       assert response.status_code == 200
       assert response.json()["title"] == "Test Meme"
       assert response.json()["description"] == "Test Description"
       assert response.json()["image_url"] == "http://test.com/image.jpg"
   
   def test_update_meme():
       # ������� �������� ��� ��� ������������
       response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
       meme_id = response.json()["id"]
       response = client.put(f"/memes/{meme_id}", json={"title": "Updated Meme", "description": "Updated Description", "image_url": "http://test.com/updated_image.jpg"})
       assert response.status_code == 200
       assert response.json()["title"] == "Updated Meme"
       assert response.json()["description"] == "Updated Description"
       assert response.json()["image_url"] == "http://test.com/updated_image.jpg"
   
   def test_delete_meme():
       # ������� �������� ��� ��� ������������
       response = client.post("/memes/", json={"title": "Test Meme", "description": "Test Description", "image_url": "http://test.com/image.jpg"})
       meme_id = response.json()["id"]
       response = client.delete(f"/memes/{meme_id}")
       assert response.status_code == 200
       response = client.get(f"/memes/{meme_id}")
       assert response.status_code == 404
   ```

3. **��������� �����:**

   ����������� ������� `pytest`, ����� ��������� �����:

   ```
   pytest
   ```

���� ����� ������ ��������� �������� �������� CRUD ��� ������ ����������. �� ���������� `TestClient` �� FastAPI ��� �������� HTTP-�������� � ������ ���������� � ��������� ������. ����� �� ���������� SQLite ���� ������ � ������ ��� ������������, ����� �� ����������� �������� ���� ������.