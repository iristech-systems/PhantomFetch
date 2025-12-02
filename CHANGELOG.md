# Changelog

All notable changes to PhantomFetch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-02

### Added
- **Unified API** for switching between curl-cffi (fast) and Playwright (browser) engines
- **Smart Caching** with configurable strategies (`all`, `resources`, `conservative`)
- **Proxy Rotation** with multiple strategies (round-robin, random, sticky, geo-match)
- **Browser Actions** - Declarative browser automation (click, input, scroll, screenshot, etc.)
- **Cookie Management** - Automatic cookie handling across both engines
- **Retry Configuration** - Configurable `max_retries`, `retry_on` status codes, and `retry_backoff`
- **OpenTelemetry Integration** - Built-in observability with tracing support
- **Anti-Detection Features** - Browser fingerprint rotation via curl-cffi
- **Network Capture** - Capture XHR/fetch requests in browser mode
- Pre-commit hooks with Ruff formatter and linter
- Comprehensive project metadata for PyPI
- Enhanced README with comparison table and troubleshooting guide
- Example code for retry configuration

### Features

#### Core Engines
- `CurlEngine`: High-performance HTTP client using curl-cffi with TLS fingerprinting
- `CDPEngine`: Playwright-based browser automation via Chrome DevTools Protocol
- `BaaSEngine`: Browser-as-a-Service support for remote browser endpoints

#### Caching
- `FileSystemCache`: Local disk-based caching with TTL support
- Smart cache key generation based on URL
- Resource type filtering (images, fonts, scripts, etc.)
- Blocked domain list for tracking/analytics URLs

#### Proxy Management
- `ProxyPool`: Automatic proxy rotation with failure tracking
- Multiple selection strategies
- Geo-location based proxy matching
- Per-request proxy override

#### Response Object
- Unified `Response` type for both engines
- Helper methods: `.ok`, `.text`, `.json()`, `.to_page()`
- Cookie support with full metadata
- Network log capture
- Screenshot support (browser only)

### Configuration
- Default timeout: 30s (curl), 60s (browser)
- Default retries: 3 with exponential backoff (base 2.0)
- Default retry status codes: {429, 500, 502, 503, 504}
- Configurable concurrency limits

### Documentation
- Comprehensive README with examples
- "Why PhantomFetch?" comparison section
- Troubleshooting guide
- API documentation in docstrings
- Retry configuration examples

### Development
- Pre-commit hooks for code quality
- Pytest test suite with async support
- Development dependencies for docs, testing, and linting

[0.1.0]: https://github.com/iristech-systems/PhantomFetch/releases/tag/v0.1.0
