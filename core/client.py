from __future__ import annotations
from urllib.parse import urljoin
from dataclasses import dataclass
from types import TracebackType
from typing import Any
import httpx
from core.models import AirPollution, Current, Forecast, Geocoding
from core.utils.exceptions import WeatherError
from core.utils.weather_path import WeatherPath

__all__: list[str] = ["Client"]


@dataclass
class Client:
    """Wrapper for the OpenWeatherMap API free tier, some routes are not all used,
    they were less precise than the other."""

    app_id: str
    base_url: str = "https://api.openweathermap.org"
    _session: httpx.AsyncClient = httpx.AsyncClient()

    async def _call(self, url: str, params: dict[str, Any]) -> httpx.Response:
        """Make the requests.

        Args:
            url: The url to concat to the base url.
            params: The params to use for the request.

        Raises:
            WeatherError: Basically happen if the request don't succeed :)

        Return:
            httpx.Response: Response from the API.
        """

        params.update(dict(appid=self.app_id))
        res: httpx.Response = await self._session.get(
            url=urljoin(self.base_url, url), params=params
        )
        try:
            res.raise_for_status()
        except httpx.HTTPError:
            raise WeatherError()
        else:
            return res

    async def _get_location(self, params: dict[str, Any]) -> Geocoding:
        """Get the location for the given zipcode and country code.

        Args:
            params: Dict containing zipcode and country code.

        Return:
            Geocoding: Class representation of the API response.
        """

        ret: httpx.Response = await self._call(
            url=WeatherPath.GEOCODING.value, params=params
        )
        return Geocoding(**ret.json())

    async def get_current(
        self,
        country_code: str | None,
        zipcode: str | None,
    ) -> Current:
        """Get the current weather for a given city.

        Args:
            country_code: The country code.
            zipcode: The city zipcode.

        Return:
            Current: The current weather class representation for the given city.
        """

        geo: Geocoding = await self._get_location(dict(zip=f"{zipcode},{country_code}"))
        res: httpx.Response = await self._call(
            url=WeatherPath.CURRENT.value, params=dict(lat=geo.lat, lon=geo.lon)
        )
        return Current(**res.json())

    async def get_forecast(
        self, country_code: str | None, zipcode: str | None
    ) -> Forecast:
        """Get the forecast weather for a given city.

        Args:
            country_code: The country code.
            zipcode: The city zipcode.

        Return:
            Forecast: The forecast weather class representation for the given city.
        """

        geo: Geocoding = await self._get_location(dict(zip=f"{zipcode},{country_code}"))
        res: httpx.Response = await self._call(
            url=WeatherPath.FORECAST.value, params=dict(lat=geo.lat, lon=geo.lon)
        )
        return Forecast(**res.json())

    async def get_air_pollution(
        self, country_code: str | None, zipcode: str | None
    ) -> AirPollution:
        """Get the forecast weather for a given city.

        Args:
            country_code: The country code.
            zipcode: The city zipcode.

        Return:
            Forecast: The forecast weather class representation for the given city.
        """

        geo: Geocoding = await self._get_location(dict(zip=f"{zipcode},{country_code}"))
        res: httpx.Response = await self._call(
            url=WeatherPath.AIR_POLLUTION.value, params=dict(lat=geo.lat, lon=geo.lon)
        )
        return AirPollution(**res.json())

    async def close(self):
        await self._session.aclose()

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(
        self,
        err_type: type[Exception] | None,
        err_value: Exception | None,
        err_tb: TracebackType | None,
    ) -> None:
        await self.close()
        if err_type is not None:
            raise WeatherError(err_value)
