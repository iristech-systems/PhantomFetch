"""Example: Using PhantomFetch with Scrapeless CDP for session recording.

This example shows how to use PhantomFetch with Scrapeless's CDP endpoint
to ensure proper session recording compatibility (single window).
"""

import asyncio

from phantomfetch import Fetcher


async def main():
    # Your Scrapeless CDP endpoint URL (includes session identifier)
    scrapeless_cdp = "wss://YOUR_SESSION_ID.scrapeless.com/chrome/cdp"

    # PhantomFetch automatically reuses existing pages when connecting to remote CDP
    async with Fetcher(
        browser_engine="cdp",
        browser_engine_config={
            "cdp_endpoint": scrapeless_cdp,
            # use_existing_page=True is the default for CDP endpoints
        },
    ) as f:
        # This will use the existing window in your Scrapeless session
        # Scrapeless can now record this request!
        response = await f.fetch("https://example.com", engine="browser")

        print(f"Status: {response.status}")
        print(f"Title: {response.text[:100]}")

        # You can make additional navigations in the same window
        _response2 = await f.fetch("https://example.com/page2", engine="browser")

    print("\n✓ Session recording should now work with Scrapeless!")
    print("  Check your Scrapeless dashboard for the recording.")


async def disable_page_reuse():
    """If you need to create new windows (recording won't work), set use_existing_page=False."""

    async with Fetcher(
        browser_engine="cdp",
        browser_engine_config={
            "cdp_endpoint": "wss://YOUR_SESSION_ID.scrapeless.com/chrome/cdp",
            "use_existing_page": False,  # Creates new windows (breaks recording)
        },
    ) as f:
        # This creates a new window - Scrapeless won't record it
        _response = await f.fetch("https://example.com", engine="browser")


if __name__ == "__main__":
    asyncio.run(main())
