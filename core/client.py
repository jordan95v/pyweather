from dataclasses import dataclass
from typing import Any
import httpx
from core.models import Current, Geocoding
from core.utils.exceptions import WeatherError
from core.utils.weather_path import WeatherPath


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

        params.update(dict(app_id=self.app_id))
        res: httpx.Response = await self._session.get(
            url=f"{self.base_url}{url}", params=params
        )
        try:
            res.raise_for_status()
        except httpx.HTTPError:
            raise WeatherError()
        else:
            return res

    async def _get_location(self, params: dict[str, Any]) -> Geocoding:
        ret: httpx.Response = await self._call(
            url=WeatherPath.GEOCODING.value, params=params
        )
        return Geocoding(**ret.json())

    async def get_current(
        self,
        country_code: str | None,
        zipcode: int | None,
    ) -> Current:
        """Get the current weather for a given city.

        Args:
            country_code: The country code.
            zipcode: The city zipcode.

        Return:
            Current: The current weather for the given city.
        """

        geo: Geocoding = await self._get_location(
            dict(zip=f"{zipcode}, {country_code}")
        )
        res: httpx.Response = await self._call(
            url=WeatherPath.CURRENT.value, params=dict(lat=geo.lat, lon=geo.lon)
        )
        return Current(**res.json())
