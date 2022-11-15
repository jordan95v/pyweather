from unittest.mock import MagicMock
import httpx
import pytest
from pytest_mock import MockerFixture
from conftest import MockResponse
from core import Client
from core.models import Current, Geocoding, Forecast
from core.utils.exceptions import WeatherError


@pytest.fixture()
def client() -> Client:
    return Client(app_id="hola chica :)")


@pytest.mark.asyncio
class TestClient:
    async def test_init(self, client: Client):
        assert client.app_id == "hola chica :)"
        assert client.base_url == "https://api.openweathermap.org"

    @pytest.mark.parametrize(
        "status_code, throwable",
        [
            (200, None),
            (404, WeatherError),
        ],
    )
    async def test_call(
        self,
        client: Client,
        status_code: int,
        throwable: Exception | None,
        mocker: MockerFixture,
    ):
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(
                status_code=status_code, sample_name="hola chica"
            ),
        )
        if throwable:
            with pytest.raises(WeatherError):
                await client._call(url="/hello/you", params=dict())
        else:
            ret: httpx.Response = await client._call(url="/hello/you", params=dict())
            assert ret.status_code == 200

    async def test_geo(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(status_code=200, sample_name="geocoding"),
        )
        res: Geocoding = await client._get_location(params=dict())
        assert res.name == "Beverly Hills"

    async def test_get_current(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch.object(client, "_get_location")
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(status_code=200, sample_name="current"),
        )
        current: Current = await client.get_current(country_code="FR", zipcode=75000)
        assert current.name == "Zocca"

    async def test_get_forecast(self, client: Client, mocker: MockerFixture) -> None:
        mocker.patch.object(client, "_get_location")
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(status_code=200, sample_name="forecast"),
        )
        current: Forecast = await client.get_forecast(country_code="FR", zipcode=75000)
        assert current.city.name == "Zocca"

    async def test__aenter__(
        self,
        client: Client,
    ) -> None:
        assert isinstance(await client.__aenter__(), Client)

    @pytest.mark.parametrize("throwable", [(None), (TypeError)])
    async def test__aexit__(
        self, client: Client, mocker: MockerFixture, throwable: Exception | None
    ) -> None:
        spy: MagicMock = mocker.spy(client, "close")
        if throwable:
            with pytest.raises(WeatherError):
                await client.__aexit__(TypeError, None, None)
        else:
            await client.__aexit__(None, None, None)
            assert spy.call_count == 1
