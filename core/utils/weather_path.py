import enum


class WeatherPath(enum.Enum):
    """List all available path for WeatherOpenMap free tier."""

    CURRENT: str = "/data/2.5/weather"
    FORECAST: str = "data/2.5/forecast"
    AIR_POLLUTION: str = "/data/2.5/air_pollution"
    GEOCODING: str = "geo/1.0/zip"
