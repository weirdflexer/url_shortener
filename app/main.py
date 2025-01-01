from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
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


@app.api_route("/{path_name:path}", methods=["GET", "POST",
                                             "PUT", "DELETE",
                                             "PATCH"])
async def catch_all(request: Request, path_name: str):
    return RedirectResponse(url="/api/openapi.json")


if __name__ == "__main__":
    uvicorn.run("main:app", port=80)
