from unittest.mock import AsyncMock, Mock, patch

import pytest
from playwright.async_api import Page

from phantomfetch.engines.browser.actions import execute_actions
from phantomfetch.types import Action


@pytest.mark.asyncio
async def test_solve_captcha_action():
    # Mock page
    mock_page = Mock(spec=Page)
    mock_page.url = "http://example.com"

    # Mock solver
    with patch("phantomfetch.captcha.TwoCaptchaSolver") as MockSolver:
        mock_instance = MockSolver.return_value
        mock_instance.solve = AsyncMock(return_value="solved_token")

        actions = [Action(action="solve_captcha", api_key="12345", provider="2captcha")]

        results = await execute_actions(mock_page, actions)

        assert len(results) == 1
        assert results[0].success is True
        assert results[0].data == "solved_token"

        # Verify solver called correctly
        mock_instance.solve.assert_called_once()
        call_args = mock_instance.solve.call_args
        assert call_args[0][0] == mock_page  # page
        assert call_args[0][1].api_key == "12345"  # action


@pytest.mark.asyncio
async def test_solve_captcha_failure():
    mock_page = AsyncMock()

    with patch("phantomfetch.captcha.TwoCaptchaSolver") as MockSolver:
        mock_instance = MockSolver.return_value
        mock_instance.solve = AsyncMock(return_value=None)

        actions = [Action(action="solve_captcha", api_key="12345")]
        results = await execute_actions(mock_page, actions)

        assert len(results) == 1
        assert results[0].success is False
        assert results[0].error == "Failed to solve CAPTCHA"
