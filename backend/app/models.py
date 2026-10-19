from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import (
    ARRAY, JSON, DateTime, Float, ForeignKey, Integer, String, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Route(Base):
    __tablename__ = "routes"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)  # "R07"
    name: Mapped[str] = mapped_column(String(200))
    region: Mapped[str] = mapped_column(String(100))
    activity: Mapped[list[str]] = mapped_column(ARRAY(String))  # walking, cycling
    distance_km: Mapped[float] = mapped_column(Float)
    elevation_gain_m: Mapped[int] = mapped_column(Integer)
    difficulty: Mapped[int] = mapped_column(Integer)  # 1 kolay, 2 orta, 3 zor
    est_duration_min: Mapped[int | None] = mapped_column(Integer)
    surface: Mapped[str | None] = mapped_column(String(50))
    start_lat: Mapped[float] = mapped_column(Float)
    start_lon: Mapped[float] = mapped_column(Float)
    warnings: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    source_url: Mapped[str | None] = mapped_column(String(500))
    geom = mapped_column(Geometry("LINESTRING", srid=4326))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(200), unique=True)
    preferences: Mapped[dict] = mapped_column(JSON, default=dict)


class Favorite(Base):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())