from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider


def check_provider():
    provider = trace.get_tracer_provider()
    print(f"Provider type: {type(provider)}")
    print(f"Is Proxy: {type(provider).__name__ == 'ProxyTracerProvider'}")


print("--- Initial state ---")
check_provider()

print("\n--- Setting provider ---")
trace.set_tracer_provider(TracerProvider())
check_provider()
