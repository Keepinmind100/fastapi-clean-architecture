import os

import pytest


os.environ["ENV"] = "test"

if os.getenv("ENV") not in ["test"]:
    msg = f"ENV is not test, it is {os.getenv('ENV')}"
    pytest.exit(msg)

from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
from sqlmodel import create_engine, SQLModel
from loguru import logger


@pytest.fixture(scope="session")
async def reset_db():
    engine = create_engine(settings.DATABASE_URI_MAPPER["test"])
    logger.info(engine)
    with engine.begin() as conn:
        await SQLModel.metadata.drop_all(conn)
        await SQLModel.metadata.create_all(conn)
    return engine


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
