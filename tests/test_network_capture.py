import pytest

from phantomfetch import Action, Fetcher


@pytest.mark.asyncio
async def test_network_capture():
    # We trigger a fetch inside the browser page
    actions = [
        Action(
            action="evaluate",
            value="fetch('https://httpbin.org/json').then(r => r.json())",
        ),
        Action(action="wait", timeout=2000),  # Give it time to complete
    ]

    async with Fetcher(browser_engine="cdp") as f:
        # Navigate to same origin to avoid CORS/CSP issues
        resp = await f.fetch(
            "https://httpbin.org/html", engine="browser", actions=actions
        )

    assert resp.ok
    assert resp.network_log is not None

    # Check if we captured the fetch to httpbin
    captured = [entry for entry in resp.network_log if "httpbin.org/json" in entry.url]

    assert len(captured) > 0
    exchange = captured[0]
    assert exchange.resource_type == "fetch"
    assert exchange.method == "GET"
    assert exchange.status == 200
