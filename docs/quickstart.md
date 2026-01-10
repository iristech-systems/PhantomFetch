# Quick Start

Get started with PhantomFetch in just a few minutes.

## Installation

Install PhantomFetch using pip:

```bash
pip install phantomfetch
```

For development, install with dev dependencies:

```bash
pip install phantomfetch[dev]
```

## Basic Usage

### Simple Fetch

The simplest way to fetch a webpage:

```python
import asyncio
from phantomfetch import fetch

async def main():
    response = await fetch("https://example.com")
    print(response.text)
    print(f"Status: {response.status}")

asyncio.run(main())
```

### Using the Fetcher Class

For more control, use the `Fetcher` class:

```python
import asyncio
from phantomfetch import Fetcher

async def main():
    async with Fetcher() as fetcher:
        response = await fetcher.fetch("https://example.com")
        print(response.text)

asyncio.run(main())
```

## Engine Selection

PhantomFetch supports two engines:

### Curl Engine (Default)

Fast, lightweight HTTP client using `curl-cffi`:

```python
response = await fetcher.fetch(
    "https://api.example.com/data",
    engine="curl"
)
```

### Browser Engine

Full browser automation using Playwright:

```python
response = await fetcher.fetch(
    "https://example.com",
    engine="browser",
    actions=["wait_for_load"]
)
```

## Working with Cookies

PhantomFetch provides full cookie support:

```python
from phantomfetch import Fetcher, Cookie

async with Fetcher() as fetcher:
    # Set cookies before request
    cookies = [
        Cookie(name="session_id", value="abc123", domain=".example.com")
    ]

    response = await fetcher.fetch(
        "https://example.com",
        cookies=cookies
    )

    # Access response cookies
    for cookie in response.cookies:
        print(f"{cookie.name}: {cookie.value}")
```

## Browser Actions

Interact with web pages using actions:

```python
actions = [
    "wait_for_load",
    "click:#submit-button",
    "input:#search:phantomfetch",
    "screenshot",
]

response = await fetcher.fetch(
    "https://example.com",
    engine="browser",
    actions=actions
)

# Save screenshot
if response.screenshot:
    with open("screenshot.png", "wb") as f:
        f.write(response.screenshot)
```

## Error Handling and Retries

Configure retry behavior:

```python
response = await fetcher.fetch(
    "https://flaky-api.example.com",
    retry_on=[500, 502, 503],
    retry_backoff=[1, 2, 4],  # Exponential backoff in seconds
)
```

## Proxy Configuration

Use proxies for requests:

```python
async with Fetcher(proxies=["http://user:pass@proxy.com:8080"]) as fetcher:
    response = await fetcher.fetch("https://example.com")
```

## Caching

Enable caching for faster development:

```python
from phantomfetch import Fetcher, FileSystemCache

cache = FileSystemCache(cache_dir=".cache/phantomfetch")

async with Fetcher(cache=cache) as fetcher:
    # First request hits the network
    response1 = await fetcher.fetch("https://example.com")

    # Second request uses cache
    response2 = await fetcher.fetch("https://example.com")
```

## Next Steps

- Check out the [Cheatsheet](cheatsheet.md) for more examples
- Read the [API Reference](api.md) for detailed documentation
- Learn about [Advanced Usage](advanced.md) and telemetry
