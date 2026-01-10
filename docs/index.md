# PhantomFetch Documentation

**PhantomFetch** is a high-performance, async-first web scraping library for Python that combines the speed of `curl-cffi` with the power of Playwright browser automation.

::::{grid} 2
:::{grid-item-card} 🚀 Quick Start
:link: quickstart
:link-type: doc

Get up and running with PhantomFetch in minutes
:::

:::{grid-item-card} 📚 API Reference
:link: api
:link-type: doc

Complete API documentation for all classes and functions
:::

:::{grid-item-card} 📖 Cheatsheet
:link: cheatsheet
:link-type: doc

Practical examples and recipes for common tasks
:::

:::{grid-item-card} 🔧 Advanced Usage
:link: advanced
:link-type: doc

Advanced patterns, telemetry, and optimization
:::
::::

## Features

- **🚀 Unified API**: Switch between `curl` and `browser` engines with one parameter
- **⚡ High Performance**: Built on `curl-cffi` and Playwright for optimal speed
- **🕵️ Stealth Mode**: Built-in anti-detection and proxy rotation
- **🍪 Cookie Management**: Full cookie support with persistence
- **📊 OpenTelemetry**: Built-in observability and tracing
- **📦 Developer Experience**: Fully typed, documented, and Pythonic
- **🔄 Smart Retries**: Configurable retry logic with exponential backoff
- **💾 Caching**: Filesystem caching for faster development

## Installation

```bash
pip install phantomfetch
```

## Quick Example

```python
import asyncio
from phantomfetch import Fetcher

async def main():
    async with Fetcher() as fetcher:
        # Fast curl-based fetch
        response = await fetcher.fetch("https://example.com")
        print(response.text)

        # Browser-based fetch with actions
        response = await fetcher.fetch(
            "https://example.com",
            engine="browser",
            actions=["wait_for_load", "screenshot"]
        )

        # Access cookies
        for cookie in response.cookies:
            print(f"{cookie.name}: {cookie.value}")

asyncio.run(main())
```

## Documentation Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

quickstart
cheatsheet
advanced
agentic
debugging
telemetry
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api
types
engines
```

```{toctree}
:caption: Links

GitHub <https://github.com/iristech-systems/PhantomFetch>
Issues <https://github.com/iristech-systems/PhantomFetch/issues>
Changelog <https://github.com/iristech-systems/PhantomFetch/blob/main/CHANGELOG.md>
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
