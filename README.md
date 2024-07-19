# Meme Collection API

## Описание
Веб-приложение для работы с коллекцией мемов. Приложение позволяет загружать, обновлять, удалять и просматривать мемы.

## Функциональность

- **GET /memes**: Получить список всех мемов (с пагинацией).
- **GET /memes/{id}**: Получить конкретный мем по его ID.
- **POST /memes**: Добавить новый мем (с картинкой и текстом).
- **PUT /memes/{id}**: Обновить существующий мем.
- **DELETE /memes/{id}**: Удалить мем.

## Запуск проекта

Установите зависимости:

```bash
pip install -r requirements.txt
```

Настройте переменные окружения:
Создайте файл .env в корневой директории проекта и добавьте необходимые переменные окружения. Пример:

```bash
DATABASE_URL=sqlite:///./test.db
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
``````

активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

запустите приложение:

```bash
cd /home/troll/disk/work/testpython1
uvicorn app.main:app --reload
```

--reload - позволяет применять изменения в проекте без перезагрузки

### Локальный запуск

1. Клонируйте репозиторий.
2. Настройте переменные окружения для базы данных и S3.
3. Запустите Docker Compose:

```bash
docker-compose up --build
```
***

Для тестирования вашего FastAPI приложения можно использовать модуль `pytest` вместе с клиентом тестирования, который предоставляет FastAPI. Вот как можно написать тесты для вашего приложения:

1. **Установите необходимые зависимости:**

   Убедитесь, что у вас установлены `pytest` и `httpx`:

   ```
   pip install pytest httpx
   ```

2. **Создайте файл тестов, например, `test_main.py`:**

   ```
   fastapi.testclient import TestClient
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   from .main import app, get_db
   from . import models, schemas
   
   # Установите базу данных для тестирования (в памяти)
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
   ```

3. **Запустите тесты:**

   Используйте команду `pytest`, чтобы запустить тесты:

   ```
   pytest
   ```

Этот набор тестов покрывает основные операции CRUD для вашего приложения. Мы используем `TestClient` из FastAPI для отправки HTTP-запросов к вашему приложению и проверяем ответы. Также мы используем SQLite базу данных в памяти для тестирования, чтобы не затрагивать основную базу данных.