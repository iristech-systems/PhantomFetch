# Advanced Usage

Advanced patterns and best practices for PhantomFetch.

## Custom Cache Implementation

Implement your own cache backend:

```python
from phantomfetch import CacheBackend
from typing import Optional

class RedisCache(CacheBackend):
    """Custom Redis cache backend."""

    def __init__(self, redis_url: str):
        import redis
        self.client = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[bytes]:
        """Retrieve cached response."""
        return self.client.get(key)

    async def set(self, key: str, value: bytes, ttl: int = 3600) -> None:
        """Store response in cache."""
        self.client.setex(key, ttl, value)

    async def delete(self, key: str) -> None:
        """Remove cached response."""
        self.client.delete(key)

# Usage
cache = RedisCache("redis://localhost:6379/0")
async with Fetcher(cache=cache) as fetcher:
    response = await fetcher.fetch("https://example.com")
```

## Advanced Proxy Configuration

### Proxy Rotation

```python
from phantomfetch import Fetcher

proxies = [
    "http://user1:pass1@proxy1.example.com:8080",
    "http://user2:pass2@proxy2.example.com:8080",
    "http://user3:pass3@proxy3.example.com:8080",
]

async with Fetcher(proxies=proxies) as fetcher:
    # Proxies automatically rotate on each request
    for i in range(10):
        response = await fetcher.fetch(f"https://api.example.com/page/{i}")
```

### Per-Request Proxy

```python
# Override default proxy for specific requests
response = await fetcher.fetch(
    "https://example.com",
    proxy="http://special:proxy@custom.com:8080"
)
```

## Cookie Persistence

Save and load cookies across sessions:

```python
import json
from pathlib import Path
from phantomfetch import Fetcher, Cookie

async def save_cookies(cookies: list[Cookie], path: Path):
    """Save cookies to a JSON file."""
    cookie_data = [
        {
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "expires": c.expires,
            "httpOnly": c.http_only,
            "secure": c.secure,
            "sameSite": c.same_site,
        }
        for c in cookies
    ]
    path.write_text(json.dumps(cookie_data, indent=2))

async def load_cookies(path: Path) -> list[Cookie]:
    """Load cookies from a JSON file."""
    cookie_data = json.loads(path.read_text())
    return [Cookie(**data) for data in cookie_data]

# Usage
async with Fetcher() as fetcher:
    # Login and get cookies
    response = await fetcher.fetch(
        "https://example.com/login",
        method="POST",
        json={"username": "user", "password": "pass"}
    )

    # Save cookies
    await save_cookies(response.cookies, Path("cookies.json"))

# Later session
async with Fetcher() as fetcher:
    # Load cookies
    cookies = await load_cookies(Path("cookies.json"))

    # Use cookies in authenticated request
    response = await fetcher.fetch(
        "https://example.com/dashboard",
        cookies=cookies
    )
```

## Browser Context Management

Reuse browser contexts for better performance:

```python
from phantomfetch import Fetcher

async with Fetcher(browser_engine="cdp") as fetcher:
    # First request creates a new context
    response1 = await fetcher.fetch(
        "https://example.com/login",
        engine="browser"
    )

    # Subsequent requests reuse the context and session
    response2 = await fetcher.fetch(
        "https://example.com/dashboard",
        engine="browser"
    )
```

## Custom User Agents

Rotate user agents for better anti-detection:

```python
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...",
]

async with Fetcher() as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        headers={"User-Agent": random.choice(USER_AGENTS)}
    )
```

## Network Log Analysis

Capture and analyze network traffic:

```python
async with Fetcher() as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )

    # Analyze XHR requests
    xhr_requests = [
        exchange for exchange in response.network_log
        if exchange.resource_type == "xhr"
    ]

    for exchange in xhr_requests:
        print(f"XHR: {exchange.method} {exchange.url}")
        print(f"Status: {exchange.status}")
        if exchange.request_body:
            print(f"Request: {exchange.request_body}")
        if exchange.response_body:
            print(f"Response: {exchange.response_body}")
```

## Concurrent Requests

Fetch multiple pages concurrently:

```python
import asyncio
from phantomfetch import Fetcher

async def fetch_all(urls: list[str]):
    async with Fetcher() as fetcher:
        # Create tasks for all URLs
        tasks = [fetcher.fetch(url) for url in urls]

        # Wait for all to complete
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Process responses
        for url, response in zip(urls, responses):
            if isinstance(response, Exception):
                print(f"Error fetching {url}: {response}")
            else:
                print(f"{url}: {response.status} ({len(response.text)} bytes)")

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

asyncio.run(fetch_all(urls))
```

## Remote Browser Connections

Connect to remote browser instances:

```python
# Connect to Browserless
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="wss://chrome.browserless.io?token=YOUR_TOKEN"
) as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )

# Connect to BrightData
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="wss://brd.superproxy.io:9222"
) as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

## Conditional Requests

Use ETags and Last-Modified headers:

```python
# First request
response1 = await fetcher.fetch("https://example.com/data.json")
etag = response1.headers.get("etag")
last_modified = response1.headers.get("last-modified")

# Subsequent request with conditional headers
headers = {}
if etag:
    headers["If-None-Match"] = etag
if last_modified:
    headers["If-Modified-Since"] = last_modified

response2 = await fetcher.fetch(
    "https://example.com/data.json",
    headers=headers
)

if response2.status == 304:
    print("Content not modified, use cached version")
else:
    print("Content updated, process new version")
```


## Declarative Use Cases (v0.2.0+)

### Stealth & Humanization

Bypass antibot detection using stealth mode and human-like interactions:

```python
actions = [
    # Simulate human mouse movement and typing
    Action(action="click", selector="#btn-login", human_like=True),
    Action(action="input", selector="#username", value="user", human_like=True),
]

# Enable stealth mode (finicks navigator/chrome properties)
response = await fetcher.fetch(url, actions=actions, stealth=True)
```

### Declarative Flow Control

Handle dynamic UI states without writing custom Python logic:

```python
actions = [
    # Conditional Execution
    Action(
        action="if",
        selector=".modal-close",
        timeout=2000,
        then_actions=[
            Action(action="click", selector=".modal-close")
        ]
    ),

    # Error Handling
    Action(
        action="try",
        actions=[
            Action(action="click", selector="#unstable-btn", fail_on_error=True)
        ],
        else_actions=[
            Action(action="evaluate", value="console.log('Button missing, continuing...')")
        ]
    )
]
```

### Looping & Visibility-Aware Extraction

Scrape complex grids where elements might be hidden or nested loops are required (e.g., Variant Picking):

```python
Action(
    action="loop",
    selector=".product-card",
    actions=[
        Action(action="click", human_like=True), # Click variant
        Action(
            action="extract",
            selector="body", # Global scope extract
            schema={
                "price": {
                    "_selector": ".price-tag",
                    "_visible_only": True # Ignores hidden pre-rendered prices!
                }
            }
        )
    ]
)
```

### Interactive Selector Builder

Use the CLI tool to find robust selectors for target text:

```bash
# Find selectors for "Login" button on example.com
python -m phantomfetch.tools.selector_builder "https://example.com" "Login"
```

## See Also

- [Quick Start](quickstart.md) - Getting started guide
- [Cheatsheet](cheatsheet.md) - Common patterns and recipes
- [Telemetry](telemetry.md) - OpenTelemetry integration
