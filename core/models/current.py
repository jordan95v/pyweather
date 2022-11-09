from __future__ import annotations
from pydantic import BaseModel, Field
from common_fields import Coord, Main, WeatherItem, Clouds, Wind


class Rain(BaseModel):
    field_1h: float | None = Field(None, alias="1h")


class Sys(BaseModel):
    type: int | None = None
    id: int | None = None
    country: str | None = None
    sunrise: int | None = None
    sunset: int | None = None


class Current(BaseModel):
    coord: Coord | None = None
    weather: list[WeatherItem] | None = None
    base: str | None = None
    main: Main | None = None
    visibility: int | None = None
    wind: Wind | None = None
    rain: Rain | None = None
    clouds: Clouds | None = None
    dt: int | None = None
    sys: Sys | None = None
    timezone: int | None = None
    id: int | None = None
    name: str | None = None
    cod: int | None = None
