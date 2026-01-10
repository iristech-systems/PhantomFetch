# PhantomFetch Cheatsheet

Master PhantomFetch with comprehensive, practical examples. Every pattern you need, organized for quick reference.

::::{grid} 2
:::{grid-item}
**Target Site:** [Books to Scrape](https://books.toscrape.com)
A practice scraping site with real data
:::

:::{grid-item}
**Quick Links:**
[Automation](#automation) | [Browser](#browser-actions) | [Network](#network-monitoring) | [Advanced](#advanced-patterns)
:::
::::

---

## Understanding Actions

PhantomFetch supports three ways to define browser actions:

### 1. Action Struct (Recommended)

```python
from phantomfetch import Action

actions = [
    Action(action="click", selector="#button", timeout=5000),
    Action(action="input", selector="#search", value="query"),
    Action(action="wait", selector="#results"),
    Action(action="screenshot"),
]
```

**Advantages:**
- Full type safety and IDE autocomplete
- All options available (`timeout`, `selector`, `value`)
- Best for complex actions

### 2. Dict Format

```python
actions = [
    {"action": "click", "selector": "#button", "timeout": 5000},
    {"action": "input", "selector": "#search", "value": "query"},
    {"action": "wait", "selector": "#results"},
    {"action": "screenshot"},
]
```

**Advantages:**
- Flexible for dynamic action generation
- Easy to serialize/deserialize
- Works well with configuration files

### 3. String Shortcuts

```python
actions = [
    "click:#button",
    "input:#search=query",  # Note: uses = for values
    "wait:#results",
    "screenshot",
]
```

**Advantages:**
- Concise for simple actions
- Quick prototyping
- Limited to basic use cases

**Available ActionTypes:**
- `wait` - Wait for selector or timeout
- `click` - Click an element
- `input` - Type into an element
- `scroll` - Scroll to an element
- `hover` - Hover over an element
- `screenshot` - Capture screenshot
- `wait_for_load` - Wait for page load event
- `evaluate` - Execute JavaScript
- `select` - Select dropdown option

---

## Automation Quick Start {#automation}

### One-Liner Fetch

```python
import asyncio
from phantomfetch import fetch

# Simplest possible fetch
response = await fetch("https://books.toscrape.com")
print(response.text[:200])
```

### Using the Fetcher Class

```python
from phantomfetch import Fetcher

async with Fetcher() as fetcher:
    response = await fetcher.fetch("https://books.toscrape.com")
    print(f"Status: {response.status}")
    print(f"Title: {response.soup.find('title').text}")
```

### Batch Fetching Multiple Pages

```python
import asyncio
from phantomfetch import Fetcher

async def scrape_books():
    urls = [
        "https://books.toscrape.com/catalogue/page-1.html",
        "https://books.toscrape.com/catalogue/page-2.html",
        "https://books.toscrape.com/catalogue/page-3.html",
    ]

    async with Fetcher() as fetcher:
        tasks = [fetcher.fetch(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        for response in responses:
            books = response.soup.select(".product_pod h3 a")
            print(f"Found {len(books)} books on {response.url}")

asyncio.run(scrape_books())
```

---

## Engine Selection {#engines}

### Curl Engine (Default)

Fast HTTP requests for static content:

```python
async with Fetcher() as fetcher:
    # Curl is default - fastest option
    response = await fetcher.fetch(
        "https://books.toscrape.com/catalogue/page-1.html",
        engine="curl"
    )
```

**When to use:**
- ✅ Static HTML pages
- ✅ REST APIs
- ✅ High throughput needed
- ✅ No JavaScript required

### Browser Engine

Full browser for JavaScript-heavy sites:

```python
async with Fetcher(browser_engine="cdp") as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        engine="browser",
        actions=["wait_for_load"]
    )
```

**When to use:**
- ✅ JavaScript rendering needed
- ✅ Complex interactions required
- ✅ Screenshots needed
- ✅ Network monitoring required

---

## Browser Configuration {#browser-config}

### Headless vs Headed

```python
# Headless (default, faster)
async with Fetcher(headless=True) as fetcher:
    response = await fetcher.fetch(url, engine="browser")

# Headed (visible browser, for debugging)
async with Fetcher(headless=False) as fetcher:
    response = await fetcher.fetch(url, engine="browser")
```

### Browser Type Selection

```python
# Use CDP (Chrome DevTools Protocol) - faster
async with Fetcher(browser_engine="cdp") as fetcher:
    pass

# Use Playwright - more features
async with Fetcher(browser_engine="playwright") as fetcher:
    pass
```

### Viewport Configuration

```python
async with Fetcher(
    browser_engine="cdp",
    viewport={"width": 1920, "height": 1080}
) as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        engine="browser"
    )
```

### Custom User Agent

```python
async with Fetcher(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
) as fetcher:
    response = await fetcher.fetch("https://books.toscrape.com")
```

---

## Browser Actions {#browser-actions}

### Navigation Actions

```python
from phantomfetch import Action

# String shortcuts for simple wait actions
actions = [
    "wait_for_load",      # Wait for page load event
    "wait:2000",          # Wait 2000ms (2 seconds)
    "wait:#content",      # Wait for selector to appear
]

# Using Action struct for more control
actions = [
    Action(action="wait_for_load"),
    Action(action="wait", timeout=2000),
    Action(action="wait", selector="#content", timeout=5000),
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions,
    wait_until="networkidle"  # Browser-level wait, not an action
)
```

:::{note}
The `wait_until` parameter controls when the page load is considered complete ("domcontentloaded", "load", or "networkidle"). Actions are executed after the page loads.
:::

### Click Actions

```python
from phantomfetch import Action

# String shortcut
actions = [
    "wait_for_load",
    "click:a[href='catalogue/category/books/travel_2/index.html']",
]

# Action struct (recommended)
actions = [
    Action(action="wait_for_load"),
    Action(
        action="click",
        selector="a[href='catalogue/category/books/travel_2/index.html']",
        timeout=5000  # Wait up to 5s for element
    ),
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions
)
```

### Input Actions

```python
from phantomfetch import Action

# Using Action struct (recommended for complex actions)
actions = [
    Action(action="wait_for_load"),
    Action(action="input", selector="#search-box", value="python programming"),
    Action(action="click", selector="button[type='submit']"),
    Action(action="wait_for_load"),
]

# Using dict format
actions = [
    {"action": "wait_for_load"},
    {"action": "input", "selector": "#search-box", "value": "python programming"},
    {"action": "click", "selector": "button[type='submit']"},
    {"action": "wait_for_load"},
]

# Using string shortcuts (simple, but limited)
actions = [
    "wait_for_load",
    "input:#search-box=python programming",  # Note: uses = for value
    "click:button[type='submit']",
    "wait_for_load",
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions
)
```

### Scroll Actions

```python
from phantomfetch import Action

# String shortcut
actions = [
    "wait_for_load",
    "scroll:footer",
    "wait:500",
]

# Action struct
actions = [
    Action(action="wait_for_load"),
    Action(action="scroll", selector="footer"),
    Action(action="wait", timeout=500),
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions
)
```

### Hover Actions

```python
from phantomfetch import Action

# String shortcut
actions = [
    "wait_for_load",
    "hover:.product_pod",
    "wait:1000",
]

# Action struct
actions = [
    Action(action="wait_for_load"),
    Action(action="hover", selector=".product_pod"),
    Action(action="wait", timeout=1000),
]
```

### Complex Action Sequences

```python
from phantomfetch import Action

# Navigate to a specific book and take screenshot
actions = [
    Action(action="wait_for_load"),
    Action(action="click", selector=".product_pod h3 a"),
    Action(action="wait_for_load"),
    Action(action="screenshot"),
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions
)

# Access screenshot from response
if response.screenshot:
    with open("book_details.png", "wb") as f:
        f.write(response.screenshot)
```

### JavaScript Evaluation

```python
from phantomfetch import Action

# Execute custom JavaScript to get data
actions = [
    Action(action="wait_for_load"),
    Action(
        action="evaluate",
        value="document.querySelectorAll('.product_pod').length"
    ),
]

response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=actions
)

# JavaScript results available in action_results
for result in response.action_results:
    if result.action.action == "evaluate":
        print(f"Found {result.data} products")
```

---

## Screenshots {#screenshots}

### Basic Screenshot

```python
from phantomfetch import Action

# String shortcut
response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=["screenshot"]
)

# Action struct
response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser",
    actions=[Action(action="screenshot")]
)

# Screenshot is in response.screenshot as bytes
if response.screenshot:
    with open("books_homepage.png", "wb") as f:
        f.write(response.screenshot)
```

### Full Page Screenshot

```python
from phantomfetch import Action

# For full page screenshots, you may need to scroll
# The screenshot action captures the current viewport
actions = [
    Action(action="wait_for_load"),
    Action(action="screenshot"),
]
```

### Element-Specific Screenshots

```python
from phantomfetch import Action

# Scroll to element first, then screenshot
actions = [
    Action(action="wait_for_load"),
    Action(action="scroll", selector=".product_pod"),
    Action(action="wait", timeout=500),
    Action(action="screenshot"),
]
```

---

## Cookie Management {#cookies}

### Setting Cookies

```python
from phantomfetch import Fetcher, Cookie

cookies = [
    Cookie(
        name="session_id",
        value="abc123xyz",
        domain=".toscrape.com",
        path="/",
        secure=True,
        http_only=True
    )
]

async with Fetcher() as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        cookies=cookies
    )
```

### Reading Cookies

```python
response = await fetcher.fetch("https://books.toscrape.com")

for cookie in response.cookies:
    print(f"{cookie.name} = {cookie.value}")
    print(f"  Domain: {cookie.domain}")
    print(f"  Secure: {cookie.secure}")
    print(f"  HttpOnly: {cookie.http_only}")
```

### Persistent Cookies

```python
import json
from pathlib import Path

# Save cookies
def save_cookies(cookies, path: Path):
    cookie_data = [
        {
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "expires": c.expires,
            "httpOnly": c.http_only,
            "secure": c.secure,
        }
        for c in cookies
    ]
    path.write_text(json.dumps(cookie_data, indent=2))

# Load cookies
def load_cookies(path: Path):
    cookie_data = json.loads(path.read_text())
    return [Cookie(**data) for data in cookie_data]

# Usage
async with Fetcher() as fetcher:
    # First visit
    response = await fetcher.fetch("https://books.toscrape.com")
    save_cookies(response.cookies, Path("cookies.json"))

# Later session
async with Fetcher() as fetcher:
    cookies = load_cookies(Path("cookies.json"))
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        cookies=cookies
    )
```

---

## Network Monitoring {#network-monitoring}

### Capture All Network Traffic

```python
response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser"
)

# View all network requests
for exchange in response.network_log:
    print(f"{exchange.method} {exchange.url}")
    print(f"  Status: {exchange.status}")
    print(f"  Type: {exchange.resource_type}")
```

### Filter XHR/Fetch Requests

```python
response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser"
)

# Find API calls
api_calls = [
    ex for ex in response.network_log
    if ex.resource_type in ("xhr", "fetch")
]

for call in api_calls:
    print(f"API: {call.url}")
    print(f"Request: {call.request_body}")
    print(f"Response: {call.response_body}")
```

### Monitor Specific Resources

```python
response = await fetcher.fetch(
    "https://books.toscrape.com",
    engine="browser"
)

# Find all images loaded
images = [
    ex for ex in response.network_log
    if ex.resource_type == "image"
]

print(f"Loaded {len(images)} images:")
for img in images:
    print(f"  {img.url}")
```

---

## Proxy Configuration {#proxies}

### Single Proxy

```python
async with Fetcher(
    proxies=["http://user:pass@proxy.example.com:8080"]
) as fetcher:
    response = await fetcher.fetch("https://books.toscrape.com")
```

### Proxy Rotation

```python
# Proxies rotate automatically on each request
proxies = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

async with Fetcher(proxies=proxies) as fetcher:
    # Each request uses a different proxy
    for i in range(5):
        response = await fetcher.fetch(
            f"https://books.toscrape.com/catalogue/page-{i+1}.html"
        )
        print(f"Page {i+1}: {response.status}")
```

### Per-Request Proxy Override

```python
async with Fetcher() as fetcher:
    # Use different proxy for specific request
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        proxy="http://special:proxy@custom.com:8080"
    )
```

---

## Caching {#caching}

### Enable File System Cache

```python
from phantomfetch import Fetcher, FileSystemCache

cache = FileSystemCache(
    cache_dir=".cache/books",
    ttl=3600  # 1 hour
)

async with Fetcher(cache=cache) as fetcher:
    # First request hits network
    response1 = await fetcher.fetch("https://books.toscrape.com")
    print("First request:", response1.elapsed)

    # Second request uses cache (much faster)
    response2 = await fetcher.fetch("https://books.toscrape.com")
    print("Cached request:", response2.elapsed)
```

### Cache Control

```python
cache = FileSystemCache(cache_dir=".cache/books")

async with Fetcher(cache=cache) as fetcher:
    # Skip cache for fresh data
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        cache_policy="no-cache"
    )

    # Clear expired cache entries
    await cache.clear_expired()
```

---

## Error Handling & Retries {#error-handling}

### Basic Retry Configuration

```python
response = await fetcher.fetch(
    "https://books.toscrape.com",
    retry_on=[500, 502, 503],           # Retry on these status codes
    retry_backoff=[1, 2, 4, 8],         # Exponential backoff
)
```

### Exception Handling

```python
try:
    response = await fetcher.fetch("https://books.toscrape.com")
except TimeoutError:
    print("Request timed out")
except ProxyError:
    print("Proxy connection failed")
except FetchError as e:
    print(f"Fetch failed: {e}")
```

### Custom Timeout

```python
async with Fetcher(timeout=60) as fetcher:
    response = await fetcher.fetch("https://books.toscrape.com")
```

---

## Advanced Patterns {#advanced-patterns}

### Pagination Scraping

```python
async def scrape_all_pages():
    async with Fetcher() as fetcher:
        page = 1
        all_books = []

        while True:
            url = f"https://books.toscrape.com/catalogue/page-{page}.html"
            response = await fetcher.fetch(url)

            # Check if page exists
            if response.status == 404:
                break

            # Extract books
            books = response.soup.select(".product_pod h3 a")
            if not books:
                break

            all_books.extend([b.get("title") for b in books])
            page += 1

        return all_books

books = await scrape_all_pages()
print(f"Found {len(books)} total books")
```

### Concurrent Pagination

```python
async def scrape_pages_concurrent():
    async with Fetcher() as fetcher:
        # Scrape first 10 pages concurrently
        tasks = [
            fetcher.fetch(f"https://books.toscrape.com/catalogue/page-{i}.html")
            for i in range(1, 11)
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        all_books = []
        for response in responses:
            if isinstance(response, Exception):
                continue
            books = response.soup.select(".product_pod h3 a")
            all_books.extend([b.get("title") for b in books])

        return all_books
```

### Extract Product Details

```python
async def scrape_book_details(url: str):
    async with Fetcher() as fetcher:
        response = await fetcher.fetch(url)
        soup = response.soup

        return {
            "title": soup.select_one("h1").text,
            "price": soup.select_one(".price_color").text,
            "availability": soup.select_one(".availability").text.strip(),
            "rating": soup.select_one(".star-rating")["class"][1],
            "description": soup.select_one("#product_description ~ p").text if soup.select_one("#product_description ~ p") else None,
        }

# Scrape first book details
book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
details = await scrape_book_details(book_url)
print(details)
```

### Category Scraping

```python
async def scrape_category(category_url: str):
    async with Fetcher() as fetcher:
        response = await fetcher.fetch(category_url)
        soup = response.soup

        category_name = soup.select_one(".page-header h1").text
        books = []

        for product in soup.select(".product_pod"):
            books.append({
                "title": product.select_one("h3 a")["title"],
                "price": product.select_one(".price_color").text,
                "availability": product.select_one(".availability").text.strip(),
                "url": product.select_one("h3 a")["href"],
            })

        return {
            "category": category_name,
            "books": books,
            "count": len(books)
        }

# Scrape travel category
result = await scrape_category(
    "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
)
print(f"{result['category']}: {result['count']} books")
```

### Rate Limiting

```python
import asyncio

async def rate_limited_scraping():
    async with Fetcher() as fetcher:
        for i in range(1, 11):
            url = f"https://books.toscrape.com/catalogue/page-{i}.html"
            response = await fetcher.fetch(url)

            # Process response
            books = response.soup.select(".product_pod")
            print(f"Page {i}: {len(books)} books")

            # Wait between requests
            await asyncio.sleep(1)  # 1 second delay
```

---

## Data Extraction {#extraction}

### Using Beautiful Soup (Built-in)

```python
response = await fetcher.fetch("https://books.toscrape.com")

# response.soup is automatically available
books = response.soup.select(".product_pod")
for book in books:
    title = book.select_one("h3 a")["title"]
    price = book.select_one(".price_color").text
    print(f"{title}: {price}")
```

### JSON Responses

```python
# For API endpoints
response = await fetcher.fetch("https://api.example.com/books")

data = response.json()  # Parse JSON automatically
print(data)
```

### Custom Parsing

```python
response = await fetcher.fetch("https://books.toscrape.com")

# Raw HTML
html = response.text

# Raw bytes
raw_data = response.content

# Headers
headers = response.headers
print(f"Content-Type: {headers.get('content-type')}")
```

---

## Remote Browsers {#remote-browsers}

### Browserless Integration

```python
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="wss://chrome.browserless.io?token=YOUR_TOKEN"
) as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        engine="browser"
    )
```

### BrightData Integration

```python
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="wss://brd.superproxy.io:9222"
) as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        engine="browser"
    )
```

### Custom Chrome Instance

```python
# Connect to locally running Chrome
async with Fetcher(
    browser_engine="cdp",
    cdp_endpoint="ws://localhost:9222"
) as fetcher:
    response = await fetcher.fetch(
        "https://books.toscrape.com",
        engine="browser"
    )
```

---

## Best Practices {#best-practices}

### 1. Start with Curl, Upgrade to Browser

```python
async with Fetcher() as fetcher:
    # Try curl first (faster)
    response = await fetcher.fetch("https://books.toscrape.com")

    # If you need JavaScript, switch to browser
    if "<noscript>" in response.text:
        response = await fetcher.fetch(
            "https://books.toscrape.com",
            engine="browser"
        )
```

### 2. Reuse Fetcher Instances

```python
# Good: Reuse fetcher for multiple requests
async with Fetcher() as fetcher:
    for i in range(10):
        response = await fetcher.fetch(f"https://books.toscrape.com/page-{i}.html")

# Bad: Create new fetcher for each request
for i in range(10):
    async with Fetcher() as fetcher:  # Expensive!
        response = await fetcher.fetch(f"https://books.toscrape.com/page-{i}.html")
```

### 3. Use Caching for Development

```python
# Speed up development with caching
cache = FileSystemCache(cache_dir=".cache/dev")

async with Fetcher(cache=cache) as fetcher:
    # First run: hits network
    # Subsequent runs: instant from cache
    response = await fetcher.fetch("https://books.toscrape.com")
```

### 4. Handle Errors Gracefully

```python
async def safe_fetch(url: str):
    try:
        async with Fetcher() as fetcher:
            return await fetcher.fetch(url, retry_on=[500, 502, 503])
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None
```

### 5. Respect robots.txt

```python
import urllib.robotparser

rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://books.toscrape.com/robots.txt")
rp.read()

url = "https://books.toscrape.com/catalogue/page-1.html"
if rp.can_fetch("*", url):
    response = await fetcher.fetch(url)
else:
    print("Blocked by robots.txt")
```

---

## See Also

- [Quick Start](quickstart.md) - Getting started guide
- [API Reference](api.md) - Complete API documentation
- [Engine Reference](engines.md) - Detailed engine documentation
- [Advanced Usage](advanced.md) - Advanced patterns
- [Telemetry](telemetry.md) - OpenTelemetry integration
