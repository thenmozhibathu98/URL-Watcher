import asyncio
import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlmodel import Session, select
from .db import init_db, get_session
from .models import URL, Check
from .watcher import Watcher

app = FastAPI(title="URL Watcher")
watcher = Watcher()


class URLCreate(BaseModel):
    url: HttpUrl
    interval: Optional[int] = 60


class URLRead(BaseModel):
    id: int
    url: str
    interval: int


class CheckRead(BaseModel):
    id: int
    status_code: Optional[int]
    latency_ms: Optional[int]
    success: bool
    error: Optional[str]
    timestamp: str


@app.on_event("startup")
async def on_startup():
    init_db()
    if os.getenv("DISABLE_WATCHER") == "1":
        return
    asyncio.create_task(watcher.start())


@app.on_event("shutdown")
async def on_shutdown():
    await watcher.stop()


@app.post("/urls", response_model=URLRead, status_code=201)
async def create_url(payload: URLCreate, session: Session = Depends(get_session)):
    url = URL(url=str(payload.url), interval=payload.interval or 60)
    session.add(url)
    session.commit()
    session.refresh(url)
    watcher.add(url.id)
    return URLRead(id=url.id, url=url.url, interval=url.interval)


@app.get("/urls", response_model=List[URLRead])
def list_urls(session: Session = Depends(get_session)):
    urls = session.exec(select(URL)).all()
    return [URLRead(id=u.id, url=u.url, interval=u.interval) for u in urls]


@app.get("/urls/{url_id}/checks", response_model=List[CheckRead])
def get_checks(url_id: int, limit: int = 50, session: Session = Depends(get_session)):
    url_obj = session.get(URL, url_id)
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    checks = session.exec(
        select(Check).where(Check.url_id == url_id).order_by(Check.timestamp.desc()).limit(limit)
    ).all()
    return [
        CheckRead(
            id=c.id,
            status_code=c.status_code,
            latency_ms=c.latency_ms,
            success=c.success,
            error=c.error,
            timestamp=c.timestamp.isoformat(),
        )
        for c in checks
    ]


@app.post("/urls/{url_id}/trigger", status_code=202)
async def trigger_url(url_id: int):
    if os.getenv("DISABLE_WATCHER") == "1":
        return {"status": "trigger skipped (watcher disabled)"}

    watcher.trigger(url_id)
    return {"status": "triggered"}

