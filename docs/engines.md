# Engine Reference

PhantomFetch supports two execution engines for different use cases.

## Engine Overview

| Engine | Speed | Features | Use Case |
|--------|-------|----------|----------|
| **curl** | ⚡⚡⚡ Fast | HTTP only | APIs, static pages, high throughput |
| **browser** | ⚡ Moderate | Full browser | JavaScript, interactions, screenshots |

## Curl Engine

The curl engine uses `curl-cffi` for high-performance HTTP requests.

### Features

- ✅ Extremely fast HTTP requests
- ✅ HTTP/2 and HTTP/3 support
- ✅ Automatic decompression
- ✅ Cookie handling
- ✅ Custom headers
- ✅ Proxy support
- ✅ Retry logic
- ❌ No JavaScript execution
- ❌ No DOM manipulation
- ❌ No screenshots

### Usage

```python
from phantomfetch import Fetcher

async with Fetcher() as fetcher:
    # Curl is the default engine
    response = await fetcher.fetch("https://api.example.com")

    # Explicit engine selection
    response = await fetcher.fetch(
        "https://api.example.com",
        engine="curl"
    )
```

### Configuration

```python
async with Fetcher(
    timeout=30,  # Request timeout
    max_redirects=10,  # Maximum redirects
    verify_ssl=True,  # SSL verification
) as fetcher:
    response = await fetcher.fetch("https://example.com")
```

### Advanced Options

```python
response = await fetcher.fetch(
    "https://api.example.com",
    method="POST",
    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer token123",
    },
    json={"key": "value"},
    cookies=[Cookie(name="session", value="abc", domain=".example.com")],
    retry_on=[500, 502, 503],
    retry_backoff=[1, 2, 4],
)
```

## Browser Engine

The browser engine uses Playwright for full browser automation.

### Features

- ✅ JavaScript execution
- ✅ DOM manipulation
- ✅ User interactions (click, input, scroll)
- ✅ Screenshots and PDFs
- ✅ Network monitoring
- ✅ Cookie persistence
- ✅ Multiple browser types
- ⚠️ Slower than curl
- ⚠️ Higher resource usage

### Usage

```python
from phantomfetch import Fetcher

async with Fetcher(browser_engine="cdp") as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

### Browser Types

PhantomFetch supports two browser engines:

#### CDP (Chrome DevTools Protocol)

Direct Chrome/Chromium control via CDP:

```python
async with Fetcher(browser_engine="cdp") as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

**Advantages:**
- Faster startup
- Lower memory usage
- Direct protocol access

**Limitations:**
- Chrome/Chromium only
- Requires Chrome installed

#### Playwright

Full Playwright integration with multiple browser support:

```python
async with Fetcher(browser_engine="playwright") as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

**Advantages:**
- Multiple browsers (Chrome, Firefox, WebKit)
- More features and APIs
- Better documented

**Limitations:**
- Slightly slower
- Higher memory usage

### Browser Configuration

```python
async with Fetcher(
    browser_engine="cdp",
    headless=True,  # Run without UI
    browser_type="chromium",  # Browser type
    viewport={"width": 1920, "height": 1080},  # Viewport size
    user_agent="Mozilla/5.0...",  # Custom user agent
) as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

### Browser Actions

Interact with pages using actions:

```python
actions = [
    # Wait for page load
    "wait_for_load",

    # Click elements
    "click:#submit-button",
    "click:button[type='submit']",

    # Type into inputs
    "input:#username:myuser",
    "input:[name='password']:mypass",

    # Hover over elements
    "hover:.dropdown",

    # Scroll to elements
    "scroll:footer",

    # Wait for elements
    "wait:#success-message",

    # Wait for time (milliseconds)
    "wait:2000",

    # Take screenshot
    "screenshot",

    # Execute JavaScript
    {"action": "evaluate", "value": "document.title"},
]

response = await fetcher.fetch(
    "https://example.com",
    engine="browser",
    actions=actions
)
```

### Network Monitoring

Capture network activity during page load:

```python
response = await fetcher.fetch(
    "https://example.com",
    engine="browser"
)

# Access network log
for exchange in response.network_log:
    print(f"{exchange.method} {exchange.url}")
    print(f"Status: {exchange.status}")
    print(f"Type: {exchange.resource_type}")

    # Filter XHR/Fetch requests
    if exchange.resource_type in ("xhr", "fetch"):
        print(f"Request: {exchange.request_body}")
        print(f"Response: {exchange.response_body}")
```

### Screenshots

Capture page screenshots:

```python
response = await fetcher.fetch(
    "https://example.com",
    engine="browser",
    actions=["screenshot"]
)

# Save screenshot
if response.screenshot:
    with open("page.png", "wb") as f:
        f.write(response.screenshot)
```

Full page screenshots:

```python
actions = [
    {"action": "screenshot", "full_page": True}
]

response = await fetcher.fetch(
    "https://example.com",
    engine="browser",
    actions=actions
)
```

### Remote Browsers

Connect to remote browser instances:

```python
# Browserless
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="wss://chrome.browserless.io?token=YOUR_TOKEN"
) as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )

# Custom remote Chrome
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="ws://localhost:9222"
) as fetcher:
    response = await fetcher.fetch(
        "https://example.com",
        engine="browser"
    )
```

## Engine Selection Guide

### Use Curl When:

- ✅ Fetching APIs or JSON data
- ✅ Scraping static HTML pages
- ✅ Maximum throughput is required
- ✅ Pages don't require JavaScript
- ✅ Simple cookie handling is sufficient

### Use Browser When:

- ✅ Pages require JavaScript execution
- ✅ Need to interact with elements (click, input)
- ✅ Capturing screenshots or PDFs
- ✅ Monitoring network activity
- ✅ Complex session management
- ✅ Anti-bot measures require real browser

## Performance Comparison

| Task | Curl | Browser |
|------|------|---------|
| Simple GET | ~50ms | ~500ms |
| With cookies | ~50ms | ~500ms |
| With JavaScript | ❌ N/A | ~1000ms |
| Screenshots | ❌ N/A | ~1200ms |
| Throughput | 100+ req/s | 5-10 req/s |

## Best Practices

1. **Start with curl**: Try the curl engine first for better performance
2. **Switch to browser**: Only use browser engine when curl fails or JavaScript is required
3. **Reuse contexts**: Keep the Fetcher instance alive to reuse browser contexts
4. **Headless mode**: Use headless=True in production for better performance
5. **Resource limits**: Limit concurrent browser instances (high memory usage)
6. **Action batching**: Combine multiple browser actions in a single request
7. **Network filtering**: Filter network log to reduce memory usage

## See Also

- [Quick Start](quickstart.md) - Getting started
- [Advanced Usage](advanced.md) - Advanced patterns
- [API Reference](api.md) - Complete API docs
