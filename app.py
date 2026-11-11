"""A9 demo app: OpenTelemetry tracing (based on A8).

注意：這個檔案「故意」留了幾個問題，讓 flake8 / bandit 抓得到，
報告裡可以寫「找到什麼 → 怎麼修」。修完記得再跑一次 flake8 截圖。
"""
import os
import subprocess
import requests

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

API_KEY = "fake-demo-key-123456"  # 故意的：寫死的密碼/金鑰 (bandit S105)


def fetch_status(url):
    with tracer.start_as_current_span("fetch_status"):
        r = requests.get(url)  # 故意的：沒有 timeout (bandit S113)
        return r.status_code


def run_cmd(cmd):
    with tracer.start_as_current_span("run_cmd"):
        return subprocess.call(cmd, shell=True)  # 故意的：shell=True (bandit S602)


def main():
    unused = 1  # 故意的：未使用變數 (F841)
    with tracer.start_as_current_span("main"):
        print("status:", fetch_status("https://example.com"))
        run_cmd("echo hello from A9")


if __name__ == "__main__":
    main()
