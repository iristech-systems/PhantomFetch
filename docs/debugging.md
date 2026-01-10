# Reliability & Debugging

Web scraping is inherently unstable. Layouts change, networks flake, and antibot systems wake up. PhantomFetch provides robust tools to debug and harden your scrapers.

## The Debugging Workflow

When a scraper fails, follow this workflow:

1.  **Analyze the Failure**: Check the `ActionResult` error message.
2.  **Inspect State**: Look at the automatic **screenshots** and **HAR logs**.
3.  **Reproduce**: Use the **Selector Builder** to test new selectors.
4.  **Harden**: Implement `try/catch` blocks or `wait` logic to handle the instability.

## HAR File Replay

PhantomFetch can save a standard HAR (HTTP Archive) file of the session. This is invaluable for seeing exactly what network requests happened (and what failed).

```python
# Save network log to HAR
path = response.save_har("debug_session.har")
print(f"HAR saved to {path}")
```

> **Tip**: Drag and drop this `.har` file into the Chrome DevTools "Network" tab to replay the session locally and inspect headers/payloads.

## Handling Flaky UI (`try`/`try_actions`)

Some elements, like newsletters or "Rate Us" modals, appear randomly. Us the `try` action to attempt an interaction without crashing the entire script if it fails.

```python
Action(
    action="try",
    actions=[
        # Try to close a popup if it exists
        Action(action="click", selector=".modal-close", timeout=2000, fail_on_error=True)
    ],
    else_actions=[
        # If no popup, just log and continue
        Action(action="evaluate", value="console.log('No popup found')")
    ]
)
```

## The Interactive Selector Builder

Guessing selectors is painful. Use the built-in CLI tool to find robust, reliable selectors for any text on a page.

```bash
# Syntax: python -m phantomfetch.tools.selector_builder <URL> <TEXT_TO_FIND>
python -m phantomfetch.tools.selector_builder "https://example.com" "Login"
```

**Output Example**:
```
Found 1 visible match:
Preview: Login
Suggested Selectors:
  [UNIQUE] #login-btn
  [UNIQUE] a[href='/login']
  [UNIQUE] text="Login"
```

This tool automatically verifies **uniqueness** and **visibility**, saving you hours of `DevTools -> Copy Selector` trial and error.

## Fail Fast Strategy

For production pipelines, it is often better to fail immediately than to scrape bad data.

```python
# If this critical Click fails, the script will raise an Exception immediately
# instead of continuing to the Extract step (which would produce empty/wrong data).
Action(action="click", selector="#critical-btn", fail_on_error=True)
```

Using `fail_on_error=True` ensures your downstream data pipleline stays clean.
