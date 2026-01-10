# OpenTelemetry Integration

PhantomFetch includes built-in OpenTelemetry support for observability and distributed tracing.

## Overview

PhantomFetch automatically creates spans for:

- HTTP requests (curl engine)
- Browser page loads (browser engine)
- Browser actions (clicks, inputs, etc.)
- Cache operations
- Network exchanges

## Basic Setup

### Enable Tracing

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

# Set up the tracer provider
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Now use PhantomFetch normally
from phantomfetch import Fetcher

async with Fetcher() as fetcher:
    # This request will create spans
    response = await fetcher.fetch("https://example.com")
```

### Jaeger Integration

Export traces to Jaeger:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

# Set up tracing
provider = TracerProvider(resource=Resource.create({"service.name": "my-scraper"}))
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(provider)

# Use PhantomFetch
from phantomfetch import Fetcher

async with Fetcher() as fetcher:
    response = await fetcher.fetch("https://example.com")
```

### OTLP (OpenTelemetry Protocol)

Send traces to any OTLP-compatible backend:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True,
)

# Set up tracing
resource = Resource.create({"service.name": "my-scraper"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

# Use PhantomFetch
from phantomfetch import Fetcher

async with Fetcher() as fetcher:
    response = await fetcher.fetch("https://example.com")
```

## Understanding Spans

### Span Hierarchy

PhantomFetch creates the following span hierarchy:

```
fetch (root span)
├── cache.get (if cache enabled)
├── http.request (curl engine)
│   └── curl.perform
└── browser.navigate (browser engine)
    ├── page.goto
    ├── action.click
    ├── action.input
    ├── action.screenshot
    └── network.exchange (for each XHR/fetch)
```

### Span Attributes

Each span includes relevant attributes:

**HTTP Request Spans:**
- `http.method`: HTTP method (GET, POST, etc.)
- `http.url`: Request URL
- `http.status_code`: Response status code
- `http.response_size`: Response body size in bytes
- `http.user_agent`: User agent string

**Browser Spans:**
- `browser.engine`: Browser engine type (cdp, playwright)
- `browser.headless`: Whether running headless
- `page.url`: Page URL
- `page.title`: Page title

**Action Spans:**
- `action.type`: Action type (click, input, wait, etc.)
- `action.selector`: CSS selector (if applicable)
- `action.value`: Input value or parameter

**Cache Spans:**
- `cache.hit`: Whether cache hit occurred
- `cache.key`: Cache key

## Custom Instrumentation

Add your own spans and attributes:

```python
from opentelemetry import trace
from phantomfetch import Fetcher

tracer = trace.get_tracer(__name__)

async def scrape_products():
    with tracer.start_as_current_span("scrape_products") as span:
        span.set_attribute("category", "electronics")

        async with Fetcher() as fetcher:
            response = await fetcher.fetch("https://store.example.com/electronics")

            # Parse products
            products = parse_products(response.text)
            span.set_attribute("product.count", len(products))

            return products
```

## Context Propagation

PhantomFetch automatically propagates trace context in HTTP headers:

```python
from opentelemetry import trace
from phantomfetch import Fetcher

tracer = trace.get_tracer(__name__)

async def api_call():
    # Create a parent span
    with tracer.start_as_current_span("api_workflow"):
        async with Fetcher() as fetcher:
            # This request will include traceparent header
            # for distributed tracing
            response = await fetcher.fetch("https://api.example.com/data")
```

## Sampling

Control which requests are traced:

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.sdk.trace import TracerProvider

# Sample 10% of requests
sampler = TraceIdRatioBased(0.1)
provider = TracerProvider(sampler=sampler)
trace.set_tracer_provider(provider)
```

## Performance Monitoring

Use spans to monitor performance:

```python
from opentelemetry import trace
from phantomfetch import Fetcher

async def monitor_performance():
    async with Fetcher() as fetcher:
        response = await fetcher.fetch("https://example.com")

        # Extract span context
        span = trace.get_current_span()

        # Add custom metrics
        span.set_attribute("response.size_kb", len(response.content) / 1024)
        span.set_attribute("response.encoding", response.encoding)

        if response.elapsed:
            span.set_attribute("response.time_ms", response.elapsed * 1000)
```

## Debugging

Use console exporter for debugging:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# Use SimpleSpanProcessor for immediate output
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

# Now all spans will be printed to console
```

## Best Practices

1. **Use descriptive span names**: Make it clear what each span represents
2. **Add relevant attributes**: Include context that helps with debugging
3. **Minimize overhead**: Use sampling in production
4. **Batch exports**: Use `BatchSpanProcessor` instead of `SimpleSpanProcessor`
5. **Set resource attributes**: Include service name, version, environment

## Example: Complete Setup

Here's a complete example with best practices:

```python
import asyncio
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from phantomfetch import Fetcher

def setup_telemetry():
    """Configure OpenTelemetry."""
    resource = Resource.create({
        SERVICE_NAME: "my-web-scraper",
        SERVICE_VERSION: "1.0.0",
        "environment": "production",
    })

    provider = TracerProvider(resource=resource)

    otlp_exporter = OTLPSpanExporter(
        endpoint="http://otel-collector:4317",
        insecure=True,
    )

    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(provider)

async def main():
    setup_telemetry()

    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("scraping_job") as span:
        span.set_attribute("job.type", "product_sync")

        async with Fetcher(cache=True) as fetcher:
            response = await fetcher.fetch(
                "https://example.com",
                engine="browser",
                actions=["wait_for_load"]
            )

            span.set_attribute("pages.scraped", 1)
            span.set_attribute("status", "success")

asyncio.run(main())
```

## See Also

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Jaeger](https://www.jaegertracing.io/)
- [Advanced Usage](advanced.md)
