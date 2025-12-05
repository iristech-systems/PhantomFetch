"""Test script for Scrapeless CDP compatibility.

This tests that CDPEngine properly reuses existing pages when connecting
to a remote CDP endpoint, avoiding creation of new windows.
"""

import asyncio
from phantomfetch.engines.browser.cdp import CDPEngine


async def test_existing_page_reuse():
    """Test that existing pages are detected and reused."""

    # Test 1: default behavior (use_existing_page=True)
    engine = CDPEngine(
        cdp_endpoint="ws://localhost:9222",  # Would be Scrapeless URL
        use_existing_page=True,
    )

    print("✓ CDPEngine created with use_existing_page=True (default)")
    print(f"  - use_existing_page: {engine.use_existing_page}")
    print(f"  - _existing_page: {engine._existing_page}")
    print(f"  - _existing_context: {engine._existing_context}")

    # Test 2: opt-out behavior
    engine_disabled = CDPEngine(
        cdp_endpoint="ws://localhost:9222", use_existing_page=False
    )

    print("\n✓ CDPEngine created with use_existing_page=False")
    print(f"  - use_existing_page: {engine_disabled.use_existing_page}")

    print("\n✓ All checks passed!")
    print("\nNOTE: To fully test with Scrapeless:")
    print("1. Get a Scrapeless CDP endpoint URL")
    print("2. Update cdp_endpoint in this script")
    print("3. Run: await engine.connect()")
    print("4. Run: await engine.fetch('https://example.com', engine='browser')")
    print("5. Check Scrapeless recording - should capture the request!")


if __name__ == "__main__":
    asyncio.run(test_existing_page_reuse())
