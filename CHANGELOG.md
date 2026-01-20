# Changelog

All notable changes to PhantomFetch will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2026-01-20

### Fixed
- **Cookie Injection**: Fixed an issue in `CDPEngine` where providing both `url` and `domain` for a cookie caused Playwright to error. The engine now prioritizes `domain` if present, ensuring successful cookie injection for store manipulation and session management.
## [0.2.2] - 2026-01-19

### Fixed
- **CDP Stability**: Enhanced error handling in `CDPEngine` to prevent "Target page, context or browser has been closed" errors from concealing true connection failures (e.g., timeouts, disconnects). If the browser disconnects during `wait_for_url` or action execution, the engine now returns the original error and an empty body instead of crashing during error reporting.

## [0.2.1] - 2026-01-13

### Added
- **Advanced CAPTCHA Solving**: Added `CDPSolver` for event-driven CAPTCHA solving support (specifically for Scraping Browser), featuring automatic detection and navigation waiting.
- **Full Page Screenshots**: Added `full_page=True` support to `screenshot` action.
- **Action Options**: Added `options` dictionary to `Action` struct for passing granular configuration to solvers and screenshot actions.

### Fixed
- **CAPTCHA Stability**: Fixed a race condition in `CDPSolver` where rapid page navigation after a solution could cause execution context errors. Added robust navigation waiting logic.

## [0.2.0] - 2026-01-10

### Added
- **Declarative Flow Control**: `ActionType.IF` for conditional logic and `ActionType.TRY` for error handling/catch blocks.
- **Interactive Selector Builder**: New CLI tool `phantomfetch.tools.selector_builder` to generate robust selectors for target text.
- **Stealth Mode**: `stealth` parameter in `fetch` (and `Fetcher.fetch`). Automatically injects stealth scripts to evade bot detection.
- **Humanized Interactions**: `Action(human_like=True)` for `click` and `input`. Simulates human mouse movement (Bezier curves) and typing delays.
- **Fail Fast**: `Action(fail_on_error=True)` allows individual actions to bubble up exceptions instead of just logging them.
- **Declarative Looping**: `ActionType.LOOP` allows iterating over elements and executing child actions for each.
- **Visibility-Aware Extraction**: `_visible_only` flag in `extract` schema to automatically filter for visible elements (solving hidden price issues).
- **Action Scope**: `Action(scope="page")` allows breaking out of loop element context to interact with global page elements.
- **Session Persistence**: `save_session(page, path)` and `load_session(context, path)` helpers.

### Changed
- **API Refactor**: Removed redundant `wait_for_url` parameter from `_fetch_browser` and `CDPEngine.fetch` signatures (it is handled via `Action` or `Page` properties explicitly).

## [0.1.5] - 2026-01-09

### Added
- **Strict Validation**: Added `ActionType.VALIDATE` action to ensure specific elements exist on the page. If validation fails, the request is marked as a failure.
- **Strict Waiting**: `wait_for_url` now returns an error response if the target URL is not reached within the timeout, allowing for easier retry logic.
- **Advanced Navigation**: Updated `wait_for_url` to enforce strict URL checks.

### Fixed
- Fixed `UnicodeDecodeError` in `CDPEngine` network capture when handling binary or compressed request bodies (gzip, images, etc.) by safely decoding/replacing errors.

## [0.1.4] - 2026-01-09

### Added
- **Session Persistence**: Added `save_session` and `load_session` to `Fetcher` to save/restore browser state (cookies, localStorage).
- **HAR Export**: Added `save_har` method to `Response` for exporting network logs to HAR format for debugging using Chrome DevTools.
- **Advanced Navigation**: Added `wait_for_url` parameter to `fetch` to wait for specific URL patterns (e.g., post-login redirects).
- **Extraction Action**: Added `extract` action type to performing structured data extraction using in-browser JavaScript.

### Changed
- **Type Safety**: Converted `ActionType` to `StrEnum` and added strict `msgspec` validators for `Action` fields (non-negative `timeout`).
- **Network Insights**: `NetworkExchange` now includes request `duration` calculated from Playwright timing metrics.

### Fixed
- Fixed `AttributeError` in `CDPEngine` when `user_agent` was not initialized.
- Restored `_fetch_curl` implementation which was accidentally removed.
- Improved `CDPEngine` lifecycle management for page creation and context reuse.

## [0.1.2] - 2025-12-05

### Fixed
- **Telemetry Context Propagation**: Fixed disconnected OpenTelemetry spans in `CDPEngine`. Spans generated during request interception (e.g., cache hits) are now correctly nested under the parent fetch span.

### Added
- **Browser Action Telemetry**: Added child spans for individual browser actions (click, wait, etc.).
- **Telemetry Enrichment**:
    - Added `phantomfetch.cache.size_bytes` and `phantomfetch.cache.resource_type` to cache spans.
    - Added detailed execution metrics (duration, success, input length) to action spans.

## [0.1.1] - 2025-12-05

### Added
- **Scrapeless CDP Recording Support** - PhantomFetch now automatically detects and reuses existing browser pages when connecting to remote CDP endpoints (e.g., Scrapeless)
- New `use_existing_page` parameter in `CDPEngine` (defaults to `True`) for session recording compatibility
- Example code for Scrapeless CDP integration ([`examples/scrapeless_cdp_recording.py`](examples/scrapeless_cdp_recording.py))
- Documentation section in README for Scrapeless session recording

### Changed
- `CDPEngine.connect()` now detects existing contexts and pages from remote CDP connections
- `CDPEngine.fetch()` reuses existing pages instead of creating new windows when available
- Existing pages are no longer closed in the finally block when reusing

### Fixed
- Session recording compatibility with services that only support single-window recording (Scrapeless, etc.)


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

[0.1.1]: https://github.com/iristech-systems/PhantomFetch/releases/tag/v0.1.1
[0.1.2]: https://github.com/iristech-systems/PhantomFetch/releases/tag/v0.1.2
