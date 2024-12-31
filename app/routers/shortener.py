from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from database import get_session
from schemas import URLCreate
from models import UrlModel
from utils.shortener_util import generate_short_url


shortenerRouter = APIRouter(prefix="/api")
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@shortenerRouter.post("/shorten/")
async def create_short_url(url: URLCreate, session: SessionDep):
    urlResponse = await session.execute(select(UrlModel).where(
        UrlModel.original_url == url.original_url.__str__()
        ))
    urlFromBase = urlResponse.scalars().first()
    if (urlFromBase):
        short_url = urlFromBase.short_url
        return {"status": "200",
                "short_url": f"http://localhost:8000/api/{short_url}"
                }
    else:
        short_url = generate_short_url(url.original_url.__str__())
        urlM = UrlModel(original_url=url.original_url.__str__(),
                        short_url=short_url)
        session.add(urlM)
        await session.commit()
        return {"status": "200",
                "short_url": f"http://localhost:8000/api/{short_url}"
                }


@shortenerRouter.get("/{short_url}")
async def redirect(short_url: str,
                   session: SessionDep) -> Response:
    urlResponse = await session.execute(select(UrlModel).where(
        UrlModel.short_url == short_url
        ))
    urlFromBase = urlResponse.scalars().first()
    if (urlFromBase):
        urlFromBase.clicks += 1
        await session.commit()
        return RedirectResponse(url=urlFromBase.original_url, status_code=301)
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")
