"""A9 demo app: OpenTelemetry tracing (based on A8)."""
import os
import subprocess  # noqa: S404 - only runs fixed commands, no user input
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

API_KEY = os.environ.get("API_KEY", "")  # 修正：金鑰改從環境變數讀取


def fetch_status(url):
    with tracer.start_as_current_span("fetch_status"):
        r = requests.get(url, timeout=10)  # 修正：加上 timeout (S113)
        return r.status_code


def run_cmd(args):
    with tracer.start_as_current_span("run_cmd"):
        return subprocess.call(args)  # noqa: S603 - args are hard-coded, not user input


def main():
    with tracer.start_as_current_span("main"):  # 修正：刪掉未使用變數 (F841)
        print("status:", fetch_status("https://example.com"))
        run_cmd(["echo", "hello from A9"])


if __name__ == "__main__":
    main()
