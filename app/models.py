
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class URL(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    interval: int = Field(default=60, description="Polling interval in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    checks: List["Check"] = Relationship(back_populates="url")


class Check(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="url.id")
    status_code: Optional[int] = None
    latency_ms:  Optional[int] = None
    success: bool = False
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    url: Optional[URL] = Relationship(back_populates="checks")
