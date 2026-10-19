from fastapi import Depends, FastAPI, HTTPException
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Route

app = FastAPI(title="Patikanos API")


def route_to_feature(r: Route) -> dict:
    return {
        "type": "Feature",
        "properties": {
            "id": r.id,
            "name": r.name,
            "region": r.region,
            "activity": r.activity,
            "distance_km": r.distance_km,
            "elevation_gain_m": r.elevation_gain_m,
            "difficulty": r.difficulty,
            "est_duration_min": r.est_duration_min,
            "surface": r.surface,
            "start": [r.start_lon, r.start_lat],
            "warnings": r.warnings,
            "source_url": r.source_url,
        },
        "geometry": mapping(to_shape(r.geom)) if r.geom is not None else None,
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/routes")
def list_routes(activity: str | None = None, db: Session = Depends(get_db)):
    query = select(Route)
    if activity:
        query = query.where(Route.activity.any(activity))
    routes = db.scalars(query).all()
    return {
        "type": "FeatureCollection",
        "features": [route_to_feature(r) for r in routes],
    }


@app.get("/routes/{route_id}")
def get_route(route_id: str, db: Session = Depends(get_db)):
    route = db.get(Route, route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route_to_feature(route)