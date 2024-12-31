from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_table
from routers.shortener import shortenerRouter
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan,
              docs_url=None,
              redoc_url=None,
              openapi_url="/api/openapi.json"
              )
app.include_router(shortenerRouter)


if __name__ == "__main__":
    uvicorn.run("main:app", port=80)
