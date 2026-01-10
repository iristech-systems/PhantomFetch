# Documentation Build Guide

This directory contains the Sphinx documentation for PhantomFetch.

## Building the Documentation

### Prerequisites

Install the development dependencies:

```bash
# Using uv (recommended)
uv sync --group dev

# Or using pip
pip install -e ".[dev]"
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `docs/_build/html/`. Open `docs/_build/html/index.html` in your browser.

### Live Reload (Development)

For automatic rebuilds during editing:

```bash
# Install sphinx-autobuild first
pip install sphinx-autobuild

# Start live server
cd docs
make livehtml
```

This will start a local server at `http://127.0.0.1:8000` that automatically rebuilds when you edit documentation files.

### Clean Build

Remove all build artifacts:

```bash
cd docs
make clean
```

## Documentation Structure

```
docs/
├── conf.py              # Sphinx configuration
├── index.md            # Main page
├── quickstart.md       # Quick start guide
├── cheatsheet.md       # Examples and recipes
├── advanced.md         # Advanced usage patterns
├── telemetry.md        # OpenTelemetry integration
├── api.md              # API reference
├── types.md            # Type reference
├── engines.md          # Engine documentation
├── _static/            # Static assets (CSS, images)
│   └── custom.css     # Custom styling
└── _build/            # Generated documentation (git-ignored)
```

## Writing Documentation

### MyST Markdown

We use MyST (Markedly Structured Text) for documentation. It extends Markdown with reStructuredText features.

**Links:**
```markdown
[Link text](https://example.com)
[Cross-reference](quickstart.md)
```

**Code blocks:**
````markdown
```python
import phantomfetch
```
````

**Admonitions:**
```markdown
:::{note}
This is a note
:::

:::{warning}
This is a warning
:::
```

**Autodoc:**
````markdown
```{eval-rst}
.. autoclass:: phantomfetch.Fetcher
   :members:
```
````

### Adding New Pages

1. Create a new `.md` file in `docs/`
2. Add it to the `toctree` in `index.md`
3. Write content using MyST syntax
4. Build and review: `make html`

## Theme Customization

The documentation uses `sphinx_wagtail_theme`. Customize in `conf.py`:

```python
html_theme_options = {
    "project_name": "PhantomFetch",
    "github_url": "https://github.com/iristech-systems/PhantomFetch",
    # Add more options
}
```

Custom CSS goes in `_static/custom.css`.

## Publishing

The documentation can be published to:

- **GitHub Pages**: Use GitHub Actions to build and deploy
- **Read the Docs**: Connect your repository
- **Netlify/Vercel**: Deploy the `_build/html` directory

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [MyST Parser](https://myst-parser.readthedocs.io/)
- [Wagtail Theme](https://github.com/wagtail/sphinx_wagtail_theme)
