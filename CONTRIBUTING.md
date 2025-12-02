# Contributing to PhantomFetch

Thank you for your interest in contributing to PhantomFetch! 🎉

## Getting Started

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/iristech-systems/PhantomFetch.git
   cd PhantomFetch
   ```

2. **Install dependencies**
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project with dev dependencies
   uv sync

   # Install Playwright browsers
   uv run playwright install chromium
   ```

3. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

4. **Run tests**
   ```bash
   uv run pytest
   ```

## Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**
   - Write tests for new features
   - Update documentation as needed
   - Follow existing code style (enforced by pre-commit)

3. **Run tests and linting**
   ```bash
   # Run tests
   uv run pytest

   # Run pre-commit checks
   uv run pre-commit run --all-files

   # Optional: check type hints
   uv run mypy src/phantomfetch
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `chore:` - Build/tooling changes
   - `refactor:` - Code refactoring

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub!

## Code Style

- **Formatting**: Automatically handled by `ruff format` via pre-commit
- **Linting**: Automatically checked by `ruff` via pre-commit
- **Type hints**: Use type hints for all public APIs
- **Docstrings**: Use Google-style docstrings

Example:
```python
async def fetch(
    self,
    url: str,
    *,
    engine: EngineType = "curl",
) -> Response:
    """
    Fetch a URL.

    Args:
        url: Target URL to fetch
        engine: Engine to use ("curl" or "browser")

    Returns:
        Response object with status, body, headers, etc.

    Raises:
        TimeoutError: If request times out
    """
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Use `pytest` fixtures for setup/teardown
- Mark integration tests with `@pytest.mark.integration`

```python
import pytest
from phantomfetch import Fetcher

def test_feature():
    """Test description."""
    # Arrange
    f = Fetcher()

    # Act
    result = f.do_something()

    # Assert
    assert result is not None

@pytest.mark.asyncio
async def test_async_feature():
    """Test async functionality."""
    async with Fetcher() as f:
        resp = await f.fetch("https://example.com")
        assert resp.ok
```

### Test Coverage

We aim for >80% test coverage. Run with coverage report:

```bash
uv run pytest --cov=phantomfetch --cov-report=html
```

## Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/)
- Add docstrings to all public functions/classes
- Include examples for new features

## Pull Request Process

1. **Ensure all tests pass**
2. **Update documentation** if needed
3. **Update CHANGELOG.md** under "Unreleased" section
4. **Request review** from maintainers
5. **Address feedback** promptly
6. **Squash commits** if requested before merge

## Reporting Bugs

Use the GitHub issue tracker with the bug report template. Include:
- PhantomFetch version
- Python version
- Operating system
- Minimal reproduction code
- Expected vs. actual behavior

## Feature Requests

Use the GitHub issue tracker with the feature request template. Include:
- Clear description of the feature
- Use cases and examples
- Why it would benefit the project

## Questions?

- Open a [Discussion](https://github.com/iristech-systems/PhantomFetch/discussions)
- Check existing [Issues](https://github.com/iristech-systems/PhantomFetch/issues)
- Read the [Documentation](https://github.com/iristech-systems/PhantomFetch#readme)

## Code of Conduct

Please note we have a [Code of Conduct](CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to PhantomFetch!** 🚀
