"""Sample microservice exposing Prometheus metrics."""
from prometheus_client import Counter, start_http_server
import time

REQUESTS = Counter("demo_requests_total", "Total requests")

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        REQUESTS.inc()
        time.sleep(1)
