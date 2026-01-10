import asyncio
import unittest
from unittest.mock import AsyncMock, Mock

from playwright.async_api import Page

from phantomfetch.engines.browser.actions import execute_actions
from phantomfetch.types import Action


class TestConditionalActions(unittest.TestCase):
    def test_conditional_action_skipped(self):
        """Test that an action is skipped when if_selector condition is not met."""

        async def run_test():
            mock_page = Mock(spec=Page)
            # But specific methods need care.
            # page.locator is sync, returns Locator. Locator.count is async.

            mock_locator = Mock()
            # method count is async
            mock_locator.count = AsyncMock(return_value=0)

            mock_page.locator.return_value = mock_locator
            # Other async methods on page needs to be AsyncMock if called.
            # execute_actions calls wait_for_timeout, which is async.
            mock_page.wait_for_timeout = AsyncMock()

            actions = [Action(action="wait", timeout=1000, if_selector="#non-existent")]

            results = await execute_actions(mock_page, actions)

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].success)
            self.assertEqual(results[0].data, "Skipped (condition not met)")
            # Verify wait_for_timeout was NOT called
            mock_page.wait_for_timeout.assert_not_called()

        asyncio.run(run_test())

    def test_conditional_action_executed(self):
        """Test that an action is executed when if_selector condition IS met."""

        async def run_test():
            mock_page = Mock(spec=Page)

            mock_locator = Mock()
            # method count is async, return 1
            mock_locator.count = AsyncMock(return_value=1)

            mock_page.locator.return_value = mock_locator
            mock_page.wait_for_timeout = AsyncMock()

            actions = [Action(action="wait", timeout=1000, if_selector="#exists")]

            results = await execute_actions(mock_page, actions)

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].success)
            self.assertIsNone(results[0].data)  # Standard result
            # Verify wait_for_timeout WAS called
            mock_page.wait_for_timeout.assert_called_once_with(1000)

        asyncio.run(run_test())

    def test_conditional_action_timeout_skipped(self):
        """Test skipping after waiting for timeout."""

        async def run_test():
            mock_page = Mock(spec=Page)
            mock_locator = Mock()
            mock_locator.wait_for = AsyncMock(side_effect=Exception("Timeout"))
            mock_page.locator.return_value = mock_locator

            actions = [
                Action(
                    action="wait",
                    timeout=1000,
                    if_selector="#async-el",
                    if_selector_timeout=500,
                )
            ]

            results = await execute_actions(mock_page, actions)

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].success)
            self.assertEqual(results[0].data, "Skipped (condition not met)")
            mock_locator.wait_for.assert_called_once_with(timeout=500, state="attached")

        asyncio.run(run_test())

    def test_conditional_action_timeout_executed(self):
        """Test executing after successful wait."""

        async def run_test():
            mock_page = Mock(spec=Page)
            mock_locator = Mock()
            mock_locator.wait_for = AsyncMock(return_value=None)
            mock_page.locator.return_value = mock_locator
            mock_page.wait_for_timeout = AsyncMock()

            actions = [
                Action(
                    action="wait",
                    timeout=1000,
                    if_selector="#async-el",
                    if_selector_timeout=500,
                )
            ]

            results = await execute_actions(mock_page, actions)

            self.assertEqual(len(results), 1)
            self.assertTrue(results[0].success)
            self.assertIsNone(results[0].data)
            mock_locator.wait_for.assert_called_once_with(timeout=500, state="attached")

        asyncio.run(run_test())


if __name__ == "__main__":
    unittest.main()
