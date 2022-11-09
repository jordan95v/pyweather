from __future__ import annotations
from pydantic import BaseModel


class LocalNames(BaseModel):
    af: str | None = None
    ar: str | None = None
    ascii: str
    az: str | None = None
    bg: str | None = None
    ca: str | None = None
    da: str | None = None
    de: str | None = None
    el: str | None = None
    en: str
    eu: str | None = None
    fa: str | None = None
    feature_name: str
    fi: str | None = None
    fr: str | None = None
    gl: str | None = None
    he: str | None = None
    hi: str | None = None
    hr: str | None = None
    hu: str | None = None
    id: str | None = None
    it: str | None = None
    ja: str | None = None
    la: str | None = None
    lt: str | None = None
    mk: str | None = None
    nl: str | None = None
    no: str | None = None
    pl: str | None = None
    pt: str | None = None
    ro: str | None = None
    ru: str | None = None
    sk: str | None = None
    sl: str | None = None
    sr: str | None = None
    th: str | None = None
    tr: str | None = None
    vi: str | None = None
    zu: str | None = None


class Geocoding(BaseModel):
    name: str
    local_names: LocalNames
    lat: float
    lon: float
    country: str
    state: str | None = None
