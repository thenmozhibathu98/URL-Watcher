import asyncio
import logging
from typing import Dict
import httpx
from sqlmodel import Session, select
from . models import URL, Check
from .db import engine

logger = logging.getLogger("watcher")
logger.setLevel(logging.INFO)


class Watcher:
    def __init__(self):
        self._tasks: Dict[int, asyncio.Task] = {}
        self._stop = False
        self._client = httpx.AsyncClient(timeout=10.0, follow_redirects=True)

    async def start(self):
        """
        Spawn monitoring tasks for all URLs in DB at startup. 
        """
        with Session(engine) as session:
            urls = session.exec(select(URL)).all()
            for u in urls:
                self. add(url_id=u.id)
        logger.info("Watcher started with %d tasks", len(self._tasks))

    def add(self, url_id: int):
        if url_id in self._tasks:
            return
        task = asyncio.create_task(self._monitor_loop(url_id))
        self._tasks[url_id] = task
        logger.info("Started monitor for url_id=%s", url_id)

    def remove(self, url_id:  int):
        task = self._tasks.pop(url_id, None)
        if task:
            task.cancel()
            logger.info("Cancelled monitor for url_id=%s", url_id)

    async def _monitor_loop(self, url_id: int):
        try:
            while True:
                with Session(engine) as session:
                    url_obj = session.get(URL, url_id)
                    if not url_obj:
                        return
                    interval = max(1, url_obj.interval)
                    target = url_obj.url

                await self._do_check_and_persist(url_id, target)
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            logger.info("Monitor cancelled for url_id=%s", url_id)

    async def _do_check_and_persist(self, url_id: int, target: str):
        status_code = None
        latency_ms = None
        success = False
        error = None
        try:
            started = httpx._models.get_current_time()
            resp = await self._client.get(target)
            latency_ms = int((httpx._models.get_current_time() - started) * 1000)
            status_code = resp.status_code
            success = 200 <= status_code < 400
        except Exception as exc:
            error = str(exc)

        with Session(engine) as session:
            chk = Check(
                url_id=url_id,
                status_code=status_code,
                latency_ms=latency_ms,
                success=success,
                error=error,
            )
            session.add(chk)
            session.commit()
        logger.debug("Recorded check for %s:  %s %s", target, status_code, error)

    async def stop(self):
        for t in list(self._tasks.values()):
            t.cancel()
        self._tasks.clear()
        await self._client.aclose()