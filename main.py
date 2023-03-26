from fastapi import FastAPI

from src.db.base import engine
from src.api.api import api_router
from src.core.config import settings
from src.models import models
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

gunicorn_logger = logging.getLogger('gunicorn.error')

models.Base.metadata.create_all(engine)

app = FastAPI(
    title=settings.MESSENGER_BOT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_STR)

if __name__ == '__main__':
    import uvicorn
    logger.info("Application started....")

    uvicorn.run("main:app",
                host=settings.SERVER_HOST,
                port=settings.SERVER_PORT,
                log_level="debug",
                reload=True)
else:
    logger.setLevel(gunicorn_logger.level)
