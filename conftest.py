import json
import pathlib
from dataclasses import dataclass
from typing import Any
import httpx


@dataclass
class MockResponse:
    status_code: int
    sample_name: str

    def raise_for_status(self):
        if self.status_code != 200:
            raise httpx.HTTPError("hello")

    def json(self) -> dict[str, Any]:
        return json.loads(
            pathlib.Path(f"tests/samples/{self.sample_name}.json").read_bytes()
        )
