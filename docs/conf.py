"""Sphinx configuration for PhantomFetch documentation."""

import sys
from pathlib import Path

# Add src to path for autodoc
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# -- Project information -----------------------------------------------------
project = "PhantomFetch"
copyright = "2025, CosmicBull"
author = "CosmicBull"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_wagtail_theme",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
    "tasklist",
]

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "playwright": ("https://playwright.dev/python/docs/api/class-playwright", None),
}

# -- HTML output configuration -----------------------------------------------
html_theme = "sphinx_wagtail_theme"

html_theme_options = {
    "project_name": "PhantomFetch",
    "logo": "logo.svg",
    "logo_alt": "PhantomFetch",
    "logo_url": "/",
    "github_url": "https://github.com/iristech-systems/PhantomFetch",
    "footer_links": ",".join(
        [
            "About|https://github.com/iristech-systems/PhantomFetch#readme",
            "GitHub|https://github.com/iristech-systems/PhantomFetch",
            "Issues|https://github.com/iristech-systems/PhantomFetch/issues",
        ]
    ),
}

html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]

html_title = f"{project} {release}"
html_short_title = project

# -- Options for other outputs -----------------------------------------------
htmlhelp_basename = "PhantomFetchdoc"
