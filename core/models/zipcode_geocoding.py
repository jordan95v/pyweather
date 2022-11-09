from __future__ import annotations
from pydantic import BaseModel


class ZipGeocoding(BaseModel):
    zip: str | None = None
    name: str | None = None
    lat: float | None = None
    lon: float | None = None
    country: str | None = None
