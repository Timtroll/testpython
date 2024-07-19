from .dependencies import Base, engine
from . import models

# Создание всех таблиц
Base.metadata.create_all(bind=engine)
