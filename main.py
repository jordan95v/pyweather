import asyncio
from core import Client
from core.models import Current


async def main():
    async with Client(app_id="13e4aa568487945f2f8b7e760bc561da") as client:
        res: Current = await client.get_current("FR", "75001")
        print(res)


if __name__ == "__main__":
    asyncio.run(main())
