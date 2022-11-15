import httpx
import pytest
from pytest_mock import MockerFixture
from conftest import MockResponse
from core import Client
from core.models import Current, Geocoding
from core.utils.exceptions import WeatherError


@pytest.mark.asyncio
class TestClient:
    async def test_init(self):
        client: Client = Client(app_id="hello you :)")
        assert client.app_id == "hello you :)"
        assert client.base_url == "https://api.openweathermap.org"

    @pytest.mark.parametrize(
        "status_code, throwable",
        [
            (200, None),
            (404, WeatherError),
        ],
    )
    async def test_call(
        self, status_code: int, throwable: Exception | None, mocker: MockerFixture
    ):
        client: Client = Client(app_id="hello you :)")
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

    async def test_geo(self, mocker: MockerFixture) -> None:
        client: Client = Client(app_id="hola gringo")
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(status_code=200, sample_name="geocoding"),
        )
        res: Geocoding = await client._get_location(params=dict())
        assert res.name == "Beverly Hills"

    async def test_get_current(self, mocker: MockerFixture) -> None:
        client: Client = Client(app_id="hola gringo")
        mocker.patch.object(client, "_get_location")
        mocker.patch.object(
            httpx.AsyncClient,
            "get",
            return_value=MockResponse(status_code=200, sample_name="current"),
        )
        current: Current = await client.get_current(country_code="FR", zipcode=75000)
        assert current.name == "Zocca"
