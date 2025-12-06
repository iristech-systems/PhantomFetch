"""Tests for Fetcher initialization and configuration."""

from phantomfetch import Fetcher, FileSystemCache, Proxy
from phantomfetch.pool import ProxyPool


class TestFetcherInit:
    """Test Fetcher initialization."""

    def test_fetcher_basic_init(self):
        """Test basic fetcher initialization."""
        f = Fetcher()
        assert f is not None
        assert f.timeout == 30.0
        assert f.max_retries == 3

    def test_fetcher_with_custom_timeout(self):
        """Test fetcher with custom timeout."""
        f = Fetcher(timeout=60.0)
        assert f.timeout == 60.0

    def test_fetcher_with_proxies_list(self):
        """Test fetcher with proxy list."""
        proxies = ["http://proxy1:8080", "http://proxy2:8080"]
        f = Fetcher(proxies=proxies)
        assert isinstance(f.proxy_pool, ProxyPool)
        assert len(f.proxy_pool.proxies) == 2

    def test_fetcher_with_proxy_objects(self):
        """Test fetcher with Proxy objects."""
        proxies = [
            Proxy(url="http://proxy1:8080", location="US"),
            Proxy(url="http://proxy2:8080", location="EU"),
        ]
        f = Fetcher(proxies=proxies)
        assert len(f.proxy_pool.proxies) == 2
        assert f.proxy_pool.proxies[0].location == "US"

    def test_fetcher_with_cache_true(self):
        """Test fetcher with cache=True creates FileSystemCache."""
        f = Fetcher(cache=True)
        assert f.cache is not None
        assert isinstance(f.cache, FileSystemCache)

    def test_fetcher_with_cache_false(self):
        """Test fetcher with cache=False."""
        f = Fetcher(cache=False)
        assert f.cache is None

    def test_fetcher_with_custom_cache(self):
        """Test fetcher with custom cache instance."""
        cache = FileSystemCache(cache_dir=".test_cache")
        f = Fetcher(cache=cache)
        assert f.cache is cache


class TestProxyPool:
    """Test ProxyPool functionality."""

    def test_proxy_pool_init_empty(self):
        """Test empty proxy pool."""
        pool = ProxyPool([])
        assert len(pool.proxies) == 0

    def test_proxy_pool_with_strings(self):
        """Test proxy pool with string URLs."""
        pool = ProxyPool(["http://proxy1:8080", "http://proxy2:8080"])
        assert len(pool.proxies) == 2
        assert all(isinstance(p, Proxy) for p in pool.proxies)

    def test_proxy_pool_round_robin(self):
        """Test round-robin proxy selection."""
        proxies = [
            Proxy(url="http://proxy1:8080"),
            Proxy(url="http://proxy2:8080"),
        ]
        pool = ProxyPool(proxies, strategy="round_robin")

        # Get proxies in sequence
        p1 = pool.get()
        p2 = pool.get()
        p3 = pool.get()

        assert p1.url == "http://proxy1:8080"
        assert p2.url == "http://proxy2:8080"
        assert p3.url == "http://proxy1:8080"  # Wraps around

    def test_proxy_pool_mark_success(self):
        """Test marking proxy as successful."""
        proxy = Proxy(url="http://proxy:8080")
        pool = ProxyPool([proxy])

        pool.mark_success(proxy)
        assert proxy.failures == 0  # Resets on success

    def test_proxy_pool_mark_failed(self):
        """Test marking proxy as failed."""
        proxy = Proxy(url="http://proxy:8080")
        pool = ProxyPool([proxy])

        initial_failures = proxy.failures
        pool.mark_failed(proxy)
        assert proxy.failures == initial_failures + 1
