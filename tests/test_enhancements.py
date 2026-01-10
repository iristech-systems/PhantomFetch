import os
from unittest.mock import AsyncMock, Mock

import pytest
from playwright.async_api import Page

from phantomfetch.engines.browser.actions import execute_actions
from phantomfetch.types import Action, ActionType, NetworkExchange, Response


# === Typing Tests ===
def test_action_type_enum():
    assert ActionType.WAIT == "wait"
    assert ActionType.CLICK == "click"


def test_timeout_validation():
    # msgspec structs are fast and don't validate fields by default in the constructor
    # unless using msgspec.json.decode or specialized validation.
    # However, Python's runtime type hints are just hints.
    # But let's check if msgspec enforces validation if we use it to decode
    # or if we rely on static analysis.
    # The user asked for "msgspec validators".
    # With msgspec 0.18+, `msgspec.Struct` validates on `msgspec.json.decode`.
    # Let's try to decode invalid JSON.
    import msgspec

    invalid_json = b'{"action": "wait", "timeout": -1}'
    try:
        msgspec.json.decode(invalid_json, type=Action)
        raise AssertionError("Should have raised ValidationError")
    except msgspec.ValidationError:
        pass


# === Action Tests ===
@pytest.mark.asyncio
async def test_wait_state():
    mock_page = Mock(spec=Page)
    mock_page.wait_for_selector = AsyncMock()

    action = Action(action="wait", selector="#el", state="hidden")
    await execute_actions(mock_page, [action])

    mock_page.wait_for_selector.assert_called_once_with(
        "#el", timeout=30000, state="hidden"
    )


@pytest.mark.asyncio
async def test_scroll_xy():
    mock_page = Mock(spec=Page)
    mock_page.evaluate = AsyncMock()

    action = Action(action="scroll", x=100, y=200)
    await execute_actions(mock_page, [action])

    mock_page.evaluate.assert_called_once_with("window.scrollTo(100, 200)")


@pytest.mark.asyncio
async def test_scroll_top():
    mock_page = Mock(spec=Page)
    mock_page.evaluate = AsyncMock()

    action = Action(action="scroll", selector="top")
    await execute_actions(mock_page, [action])

    mock_page.evaluate.assert_called_once_with("window.scrollTo(0, 0)")


# === Networking Tests ===
@pytest.mark.asyncio
async def test_block_resources():
    # We need to test the logic inside CDPEngine._handle_route or similar.
    # But that logic is nested inside fetch().
    # We can inspect if page.route is called.
    from phantomfetch.engines.browser.cdp import CDPEngine

    engine = CDPEngine(headless=True)
    engine._browser = AsyncMock()
    mock_context = AsyncMock()
    engine._browser.new_context.return_value = mock_context
    mock_page = AsyncMock()
    # AsyncMock return_value means when awaited, it returns this.
    mock_context.new_page.return_value = mock_page

    # Configure synchronous methods on the mock to avoid "coroutine never awaited" warnings
    mock_page.set_default_timeout = Mock()
    mock_page.on = Mock()

    # We want to verify that page.route is called when block_resources is passed.
    # We also need to ensure response.status is an int to satisfy msgspec if it reaches response creation
    # But usually we return earlier or response mocks need setup.
    # CDPEngine.fetch calls page.goto which returns response.
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {}
    mock_page.goto.return_value = mock_response
    mock_page.content.return_value = "<html></html>"
    mock_context.cookies.return_value = []  # for cookie capture

    await engine.fetch("http://example.com", block_resources=["image"])

    # Check if page.route was called
    # It should be called with "**/*" and a handler
    mock_page.route.assert_called()
    args = mock_page.route.call_args
    assert args[0][0] == "**/*"
    # The handler is a local function, hard to call directly without capturing it.

    # Let's extract the handler and test it against a mock route
    handler = args[0][1]

    mock_route = AsyncMock()
    mock_route.request.resource_type = "image"

    # Execute handler
    await handler(mock_route)

    # Verify abort was called
    mock_route.abort.assert_called_once()

    # Test non-blocked resource
    mock_route_script = AsyncMock()
    mock_route_script.request.resource_type = "script"
    # engine.cache is None, so _handle_route just continues

    await handler(mock_route_script)
    mock_route_script.continue_.assert_called()


# === Navigation Tests ===
@pytest.mark.asyncio
async def test_wait_for_url():
    from phantomfetch.engines.browser.cdp import CDPEngine

    engine = CDPEngine(headless=True)
    engine._browser = AsyncMock()
    mock_context = AsyncMock()
    engine._browser.new_context.return_value = mock_context
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page

    # Mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {}
    mock_page.goto.return_value = mock_response
    mock_page.content.return_value = "<html></html>"
    mock_context.cookies.return_value = []

    await engine.fetch("http://example.com", wait_for_url="**/succes*")

    # Verify wait_for_url called
    mock_page.wait_for_url.assert_called_once_with(
        "**/succes*", timeout=30000, wait_until="domcontentloaded"
    )


@pytest.mark.asyncio
async def test_wait_for_url_failure():
    from phantomfetch.engines.browser.cdp import CDPEngine

    engine = CDPEngine(headless=True)
    engine._browser = AsyncMock()
    mock_context = AsyncMock()
    engine._browser.new_context.return_value = mock_context
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page

    # Mock response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_page.goto.return_value = mock_response
    mock_page.url = "http://wrong-url.com"
    mock_page.content.return_value = "<html>Wrong</html>"

    # Make wait_for_url raise exception
    mock_page.wait_for_url.side_effect = Exception("Timeout")

    resp = await engine.fetch("http://example.com", wait_for_url="**/succes*")

    assert resp.ok is False
    assert "Wait for URL failed" in resp.error
    assert resp.url == "http://wrong-url.com"


# === Extraction Tests ===
@pytest.mark.asyncio
async def test_extract_action():
    mock_page = Mock(spec=Page)
    mock_page.evaluate = AsyncMock()
    mock_page.evaluate.return_value = {"title": "Test Product"}

    action = Action(
        action=ActionType.EXTRACT,
        selector=".product",
        schema={"title": ".title :: text"},
    )

    results = await execute_actions(mock_page, [action])

    assert len(results) == 1
    assert results[0].success is True
    assert results[0].data == {"title": "Test Product"}

    # Verify JS injection was called
    mock_page.evaluate.assert_called_once()
    call_args = mock_page.evaluate.call_args
    # Check if schema passed in args
    assert call_args[0][1]["schema"] == {"title": ".title :: text"}


# === Session & HAR Tests ===
def test_har_export_generation(tmp_path):
    # Test HAR generation logic in Response
    resp = Response(
        url="https://example.com/api",
        status=200,
        body=b"{}",
        network_log=[
            NetworkExchange(
                url="https://example.com/api",
                method="GET",
                status=200,
                resource_type="xhr",
                request_headers={"user-agent": "test"},
                response_headers={"content-type": "application/json"},
                duration=0.5,
                response_body="{}",
            )
        ],
    )

    # Save to temp file
    har_path = tmp_path / "test.har"
    saved_path = resp.save_har(str(har_path))

    assert saved_path == str(har_path)
    assert os.path.exists(har_path)

    # Verify content
    import json

    with open(har_path) as f:
        har_data = json.load(f)

    assert har_data["log"]["creator"]["name"] == "PhantomFetch"
    assert len(har_data["log"]["entries"]) == 1
    entry = har_data["log"]["entries"][0]
    assert entry["request"]["url"] == "https://example.com/api"
    assert entry["time"] == 500.0  # 0.5s * 1000


@pytest.mark.asyncio
async def test_session_persistence_logic():
    from phantomfetch.fetch import Fetcher

    # Mock engine
    mock_engine = AsyncMock()
    # Mock response with storage state
    mock_response = Response(
        url="http://example.com",
        status=200,
        body=b"",
        storage_state={
            "cookies": [
                {
                    "name": "session",
                    "value": "123",
                    "domain": "example.com",
                    "path": "/",
                }
            ]
        },
    )
    mock_engine.fetch.return_value = mock_response

    fetcher = Fetcher(headless=True)
    fetcher._browser = mock_engine
    fetcher._browser_engine_type = "cdp"

    # 1. Fetch triggers session update
    await fetcher.fetch("http://example.com", engine="browser")

    assert fetcher.session_data == mock_response.storage_state

    # 2. Next fetch uses session data
    await fetcher.fetch("http://example.com/2", engine="browser")

    # Check if storage_state was passed to engine.fetch
    call_args = mock_engine.fetch.call_args[1]
    assert call_args["storage_state"] == mock_response.storage_state
