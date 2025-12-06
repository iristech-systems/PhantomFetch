"""Tests for Response type and basic functionality."""

from phantomfetch import Cookie, Response
from phantomfetch.types import Action, NetworkExchange


class TestResponse:
    """Test Response object functionality."""

    def test_response_ok_property(self):
        """Test ok property for successful responses."""
        resp = Response(url="https://example.com", status=200, body=b"test")
        assert resp.ok is True

        resp_error = Response(
            url="https://example.com", status=500, body=b"error", error="Server error"
        )
        assert resp_error.ok is False

    def test_response_text_property(self):
        """Test text property decodes body."""
        resp = Response(url="https://example.com", status=200, body=b"Hello World")
        assert resp.text == "Hello World"

    def test_response_json(self):
        """Test json method parses JSON body."""
        json_body = b'{"key": "value", "number": 42}'
        resp = Response(url="https://example.com", status=200, body=json_body)
        data = resp.json()
        assert data["key"] == "value"
        assert data["number"] == 42

    def test_response_json_empty_body(self):
        """Test json method with empty body returns None."""
        resp = Response(url="https://example.com", status=200, body=b"")
        assert resp.json() is None

    def test_response_json_with_null_bytes(self):
        """Test json method strips null bytes."""
        json_body = b'{"key": "value\x00"}'
        resp = Response(url="https://example.com", status=200, body=json_body)
        data = resp.json()
        assert data["key"] == "value"

    def test_response_from_cache_flag(self):
        """Test from_cache flag."""
        resp = Response(url="https://example.com", status=200, body=b"test")
        assert resp.from_cache is False

        resp.from_cache = True
        assert resp.from_cache is True


class TestCookie:
    """Test Cookie type."""

    def test_cookie_creation(self):
        """Test basic cookie creation."""
        cookie = Cookie(name="session", value="abc123")
        assert cookie.name == "session"
        assert cookie.value == "abc123"
        assert cookie.domain is None

    def test_cookie_with_all_fields(self):
        """Test cookie with all optional fields."""
        cookie = Cookie(
            name="session",
            value="abc123",
            domain="example.com",
            path="/",
            expires=1234567890.0,
            http_only=True,
            secure=True,
            same_site="Strict",
        )
        assert cookie.name == "session"
        assert cookie.value == "abc123"
        assert cookie.domain == "example.com"
        assert cookie.path == "/"
        assert cookie.expires == 1234567890.0
        assert cookie.http_only is True
        assert cookie.secure is True
        assert cookie.same_site == "Strict"


class TestAction:
    """Test Action type."""

    def test_action_click(self):
        """Test click action creation."""
        action = Action(action="click", selector="#button")
        assert action.action == "click"
        assert action.selector == "#button"
        assert action.timeout == 30000  # default

    def test_action_input(self):
        """Test input action creation."""
        action = Action(action="input", selector="#name", value="John")
        assert action.action == "input"
        assert action.selector == "#name"
        assert action.value == "John"


class TestNetworkExchange:
    """Test NetworkExchange type."""

    def test_network_exchange(self):
        """Test network exchange creation."""
        exchange = NetworkExchange(
            url="https://api.example.com/data",
            method="GET",
            status=200,
            resource_type="xhr",
            request_headers={"Accept": "application/json"},
            response_headers={"Content-Type": "application/json"},
            response_body='{"result": "success"}',
            duration=0.5,
        )
        assert exchange.url == "https://api.example.com/data"
        assert exchange.method == "GET"
        assert exchange.status == 200
        assert exchange.resource_type == "xhr"
        assert exchange.duration == 0.5
