from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel

__all__: list[str] = ["Main", "Components", "ListItem", "AirPollution"]


class Main(BaseModel):
    aqi: int | None = None


class Components(BaseModel):
    co: float | None = None
    no: float | None = None
    no2: float | None = None
    o3: float | None = None
    so2: float | None = None
    pm2_5: float | None = None
    pm10: float | None = None
    nh3: float | None = None


class ListItem(BaseModel):
    dt: datetime | None = None
    main: Main | None = None
    components: Components | None = None


class AirPollution(BaseModel):
    coord: list[int] | None = None
    list: list[ListItem] | None = None
