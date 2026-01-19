from unittest.mock import AsyncMock

import pytest

from phantomfetch.engines.browser.cdp import CDPEngine


@pytest.mark.asyncio
async def test_wait_for_url_failure_with_content_crash():
    """
    Verify that if wait_for_url fails AND page.content() fails (e.g. browser disconnected),
    we still get a graceful error response instead of a secondary exception.
    """
    engine = CDPEngine(headless=True)
    engine._browser = AsyncMock()
    mock_context = AsyncMock()
    engine._browser.new_context.return_value = mock_context
    mock_page = AsyncMock()
    mock_context.new_page.return_value = mock_page

    # Mock page.content() raising exception (simulating disconnected browser)
    mock_page.content.side_effect = Exception("Target closed")

    # Mock wait_for_url raising exception
    mock_page.wait_for_url.side_effect = Exception("Navigation Timeout")

    # Mock goto returning success initially (or irrelevant if we fail at wait_for_url)
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_page.goto.return_value = mock_response

    # Execute fetch with wait_for_url
    resp = await engine.fetch("http://example.com", wait_for_url="**/succes*")

    # Verify we got a response object back despite page.content crashing
    assert resp is not None
    assert resp.ok is False
    assert "Wait for URL failed" in resp.error
    # We expect the ORIGINAL error to be preserved in the message (Navigation Timeout)
    # The fix ensures we don't crash with "Target closed" from page.content

    # Body should be empty bytes since content capture failed
    assert resp.body == b""
