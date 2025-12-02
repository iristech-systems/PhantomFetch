import pytest
from phantomfetch import Fetcher


@pytest.mark.asyncio
async def test_fetcher_init():
    f = Fetcher()
    assert f is not None


@pytest.mark.asyncio
async def test_curl_fetch_mock():
    # This is a very basic test just to ensure imports work and object creation is fine
    # Real network tests should probably be mocked or marked as integration tests
    async with Fetcher() as f:
        assert isinstance(f, Fetcher)
