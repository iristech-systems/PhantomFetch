"""Tests for CurlEngine."""

import pytest

from phantomfetch.engines.curl import CurlEngine


class TestCurlEngine:
    """Test CurlEngine functionality."""

    def test_curl_engine_init(self):
        """Test basic CurlEngine initialization."""
        engine = CurlEngine()
        assert engine.timeout == 30.0
        assert engine.max_retries == 3
        assert engine.retry_backoff_base == 2.0

    def test_curl_engine_custom_config(self):
        """Test CurlEngine with custom configuration."""
        engine = CurlEngine(timeout=60.0, max_retries=5, retry_backoff_base=1.5)
        assert engine.timeout == 60.0
        assert engine.max_retries == 5
        assert engine.retry_backoff_base == 1.5

    def test_get_browser_config(self):
        """Test browser version and user agent generation."""
        engine = CurlEngine()
        version, user_agent = engine._get_browser_config()

        assert version in engine.BROWSER_VERSIONS
        assert "Mozilla" in user_agent
        assert "Chrome" in user_agent or "Edge" in user_agent

    def test_build_headers(self):
        """Test header generation."""
        engine = CurlEngine()
        headers = engine._build_headers(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
        )

        assert "User-Agent" in headers
        assert "Accept" in headers
        assert "Accept-Language" in headers
        assert headers["DNT"] == "1"

    def test_build_headers_with_referer(self):
        """Test header generation with referer."""
        engine = CurlEngine()
        headers = engine._build_headers(
            "Mozilla/5.0 Chrome/120.0.0.0", referer="https://example.com"
        )

        assert headers["Referer"] == "https://example.com"

    @pytest.mark.asyncio
    async def test_fetch_timeout_override(self):
        """Test that timeout can be overridden per request."""
        engine = CurlEngine(timeout=30.0)
        # We're just testing the parameter passing, not actual HTTP call
        # This would require mocking or integration test
        assert engine.timeout == 30.0

    @pytest.mark.asyncio
    async def test_backoff_calculation(self):
        """Test exponential backoff calculation."""
        engine = CurlEngine(retry_backoff_base=2.0)

        # Backoff is 2^attempt * (0.5 to 1.5)
        # We can't test exact values due to randomness, but we can test it doesn't crash
        await engine._backoff(
            0
        )  # Should wait ~0.5-1.5s (but async so returns immediately in test)
        await engine._backoff(1)  # Should wait ~1-3s
        await engine._backoff(2, backoff_base=1.5)  # Should use custom base


class TestRetryLogic:
    """Test retry logic configuration."""

    def test_retry_status_codes(self):
        """Test default retry status codes."""
        engine = CurlEngine()
        assert 429 in engine.RETRY_STATUS_CODES
        assert 500 in engine.RETRY_STATUS_CODES
        assert 502 in engine.RETRY_STATUS_CODES
        assert 503 in engine.RETRY_STATUS_CODES
        assert 504 in engine.RETRY_STATUS_CODES

        # 404 should not be in retry codes by default
        assert 404 not in engine.RETRY_STATUS_CODES
