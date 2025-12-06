"""
Example demonstrating advanced retry configuration in PhantomFetch.

This shows how to customize retry behavior for specific scenarios:
- Custom retry status codes
- Custom backoff timing
- Per-request configuration
"""

import asyncio

from phantomfetch import Fetcher


async def basic_retry_example():
    """Basic example with default retry behavior."""
    print("=== Basic Retry Example ===")
    async with Fetcher() as f:
        # Default: retries on {429, 500, 502, 503, 504} with exponential backoff
        resp = await f.fetch("https://httpbin.org/status/503")
        print(f"Status: {resp.status}, Error: {resp.error}")


async def custom_retry_codes():
    """Retry on custom status codes (e.g., also retry on 404)."""
    print("\n=== Custom Retry Codes ===")
    async with Fetcher() as f:
        # Retry on custom status codes
        resp = await f.fetch(
            "https://httpbin.org/status/404",
            max_retries=3,
            retry_on={404, 429, 500, 502, 503, 504},  # Also retry on 404
        )
        print(f"Status: {resp.status}, Error: {resp.error}")


async def faster_backoff():
    """Use faster backoff for time-sensitive requests."""
    print("\n=== Faster Backoff ===")
    async with Fetcher() as f:
        # Faster backoff: 1.5^attempt instead of 2^attempt
        # Attempt 0: ~0.75-1.5s, Attempt 1: ~1.125-2.25s
        resp = await f.fetch(
            "https://httpbin.org/delay/5",
            max_retries=2,
            retry_backoff=1.5,  # Faster than default 2.0
            timeout=3.0,  # Will timeout and retry
        )
        print(f"Status: {resp.status}, Elapsed: {resp.elapsed:.2f}s")


async def aggressive_retry():
    """Aggressive retry for critical endpoints."""
    print("\n=== Aggressive Retry ===")
    async with Fetcher() as f:
        # Retry 10 times with slower backoff for flaky APIs
        resp = await f.fetch(
            "https://httpbin.org/status/503",
            max_retries=10,
            retry_on={429, 500, 502, 503, 504},
            retry_backoff=1.2,  # Slower backoff to be gentle
            timeout=5.0,
        )
        print(
            f"Status: {resp.status}, Elapsed: {resp.elapsed:.2f}s, Error: {resp.error}"
        )


async def no_retry():
    """Disable retries entirely."""
    print("\n=== No Retry ===")
    async with Fetcher() as f:
        # No retries - fail fast
        resp = await f.fetch(
            "https://httpbin.org/status/503",
            max_retries=1,  # Only 1 attempt (no retries)
        )
        print(f"Status: {resp.status}, Error: {resp.error}")


async def main():
    """Run all examples."""
    await basic_retry_example()
    await custom_retry_codes()
    await faster_backoff()
    await aggressive_retry()
    await no_retry()


if __name__ == "__main__":
    asyncio.run(main())
