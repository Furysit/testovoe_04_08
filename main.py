from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.models import Base, db_helper

from app.api_v1 import router as router_v1



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=router_v1, prefix="/api_v1")

def run():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    run()