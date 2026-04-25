from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    top_disease: Mapped[str] = mapped_column(String(128), default="unknown")
    symptom_count: Mapped[int] = mapped_column(Integer, default=0)
    retrieval_latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    execution_time_ms: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_blob: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
