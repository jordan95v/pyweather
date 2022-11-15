from __future__ import annotations
from pydantic import BaseModel


class Coord(BaseModel):
    lon: float | None = None
    lat: float | None = None


class WeatherItem(BaseModel):
    id: int | None = None
    main: str | None = None
    description: str | None = None
    icon: str | None = None


class Wind(BaseModel):
    speed: float | None = None
    deg: int | None = None
    gust: float | None = None


class Clouds(BaseModel):
    all: int | None = None


class Main(BaseModel):
    temp: float | None = None
    feels_like: float | None = None
    temp_min: float | None = None
    temp_max: float | None = None
    pressure: int | None = None
    humidity: int | None = None
    sea_level: int | None = None
    grnd_level: int | None = None
