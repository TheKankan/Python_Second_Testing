import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import get_db
from main import app
from model import Base

# 1. Base SQLite en mémoire dédiée exclusivement aux tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Garde la même connexion en mémoire pour toute la durée du test
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# 2. Fixture pour préparer les tables avant chaque test et nettoyer après
@pytest.fixture()
def session():
    Base.metadata.create_all(bind=engine)  # Crée les tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Nettoie la BDD après le test


# 3. Fixture pour surcharger get_db() dans FastAPI avec notre BDD de test
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    # Remplace get_db par notre session de test SQLite
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    # Réinitialise la surcharge après le test
    app.dependency_overrides.clear()