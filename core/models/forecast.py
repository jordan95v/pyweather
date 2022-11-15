from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from .common_fields import Coord, Main, WeatherItem, Clouds, Wind

__all__: list[str] = ["ForecastMain", "Sys", "Rain", "Cast", "City", "Forecast"]


class ForecastMain(Main):
    temp_kf: float | None = None


class Rain(BaseModel):
    field_3h: float | None = Field(None, alias="3h")


class Sys(BaseModel):
    pod: str | None = None


class Cast(BaseModel):
    dt: int | None = None
    main: ForecastMain | None = None
    weather: list[WeatherItem] | None = None
    clouds: Clouds | None = None
    wind: Wind | None = None
    visibility: int | None = None
    pop: float | None = None
    rain: Rain | None = None
    sys: Sys | None = None
    dt_txt: str | None = None


class City(BaseModel):
    id: int | None = None
    name: str | None = None
    coord: Coord | None = None
    country: str | None = None
    population: int | None = None
    timezone: int | None = None
    sunrise: datetime | None = None
    sunset: datetime | None = None


class Forecast(BaseModel):
    cod: str | None = None
    message: int | None = None
    cnt: int | None = None
    list: list[Cast] | None = None
    city: City | None = None
