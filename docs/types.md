# Type Reference

PhantomFetch type definitions and data structures.

## Response

The `Response` object contains the result of a fetch operation.

```{eval-rst}
.. autoclass:: phantomfetch.Response
   :members:
   :undoc-members:

   .. attribute:: url
      :type: str

      Final URL after redirects

   .. attribute:: status
      :type: int

      HTTP status code

   .. attribute:: headers
      :type: dict[str, str]

      Response headers

   .. attribute:: content
      :type: bytes

      Raw response body

   .. attribute:: text
      :type: str

      Decoded response body

   .. attribute:: cookies
      :type: list[Cookie]

      Cookies from response

   .. attribute:: network_log
      :type: list[NetworkExchange]

      Network activity (browser engine only)

   .. attribute:: screenshot
      :type: bytes | None

      Screenshot data (if requested)

   .. attribute:: elapsed
      :type: float | None

      Request duration in seconds
```

## Cookie

Cookie data structure.

```{eval-rst}
.. autoclass:: phantomfetch.Cookie
   :members:
   :undoc-members:

   .. attribute:: name
      :type: str

      Cookie name

   .. attribute:: value
      :type: str

      Cookie value

   .. attribute:: domain
      :type: str

      Cookie domain

   .. attribute:: path
      :type: str

      Cookie path (default: "/")

   .. attribute:: expires
      :type: int | None

      Expiration timestamp

   .. attribute:: http_only
      :type: bool

      HTTPOnly flag

   .. attribute:: secure
      :type: bool

      Secure flag

   .. attribute:: same_site
      :type: str | None

      SameSite attribute ("Strict", "Lax", or "None")
```

## Action

Browser action definition.

```{eval-rst}
.. autoclass:: phantomfetch.Action
   :members:
   :undoc-members:
```

### Action Types

Actions can be specified as strings or dictionaries:

**String Format:**
- `"wait_for_load"` - Wait for page load
- `"screenshot"` - Take a screenshot
- `"click:selector"` - Click an element
- `"input:selector:value"` - Type into an input
- `"hover:selector"` - Hover over an element
- `"scroll:selector"` - Scroll to an element
- `"wait:selector"` - Wait for an element
- `"wait:milliseconds"` - Wait for time (e.g., "wait:2000")

**Dictionary Format:**
```python
{
    "action": "evaluate",
    "value": "document.title"
}
```

## NetworkExchange

Network request/response pair captured during browser execution.

```{eval-rst}
.. autoclass:: phantomfetch.NetworkExchange
   :members:
   :undoc-members:

   .. attribute:: url
      :type: str

      Request URL

   .. attribute:: method
      :type: str

      HTTP method

   .. attribute:: status
      :type: int

      Response status code

   .. attribute:: resource_type
      :type: str

      Resource type (xhr, fetch, document, script, etc.)

   .. attribute:: request_headers
      :type: dict[str, str]

      Request headers

   .. attribute:: response_headers
      :type: dict[str, str]

      Response headers

   .. attribute:: request_body
      :type: str | None

      Request body (if available)

   .. attribute:: response_body
      :type: str | None

      Response body (if available)
```

## Proxy

Proxy configuration.

```{eval-rst}
.. autoclass:: phantomfetch.Proxy
   :members:
   :undoc-members:

   .. attribute:: server
      :type: str

      Proxy server URL

   .. attribute:: username
      :type: str | None

      Proxy authentication username

   .. attribute:: password
      :type: str | None

      Proxy authentication password
```

### Proxy URL Format

Proxies can be specified as strings in the format:

```
scheme://[username:password@]host:port
```

Examples:
- `http://proxy.example.com:8080`
- `http://user:pass@proxy.example.com:8080`
- `socks5://proxy.example.com:1080`

## FileSystemCache

File-based cache implementation.

```{eval-rst}
.. autoclass:: phantomfetch.FileSystemCache
   :members:
   :undoc-members:

   .. attribute:: cache_dir
      :type: str | Path

      Directory for cache storage

   .. attribute:: ttl
      :type: int

      Time-to-live in seconds (default: 3600)
```

## Type Aliases

Common type aliases used throughout the library:

```python
from typing import TypeAlias

# HTTP headers
Headers: TypeAlias = dict[str, str]

# Cookie list
Cookies: TypeAlias = list[Cookie]

# Actions can be strings or dicts
ActionSpec: TypeAlias = str | dict[str, str]
Actions: TypeAlias = list[ActionSpec]

# Proxy can be string or Proxy object
ProxySpec: TypeAlias = str | Proxy
```

## See Also

- [API Reference](api.md) - Function and class documentation
- [Quick Start](quickstart.md) - Usage examples
