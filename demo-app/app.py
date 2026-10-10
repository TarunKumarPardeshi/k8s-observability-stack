"""Sample microservice emitting Prometheus metrics and structured JSON logs."""
import json
import logging
import os
import random
import time
from flask import Flask, Response, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Structured JSON Logger for Loki/Promtail
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("demo-service")

def log_event(level: str, msg: str, **kwargs):
    payload = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "service": "demo-telemetry-app",
        "message": msg,
        **kwargs,
    }
    logger.info(json.dumps(payload))

# Prometheus Metrics (Golden Signals)
REQUESTS_TOTAL = Counter(
    "demo_requests_total",
    "Total HTTP requests handled",
    ["method", "endpoint", "status"]
)
REQUEST_DURATION = Histogram(
    "demo_request_duration_seconds",
    "HTTP request latency histogram in seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

@app.route("/")
def index():
    start = time.time()
    # Simulate workload latency
    latency = random.uniform(0.01, 0.15)
    time.sleep(latency)
    
    # 5% random error rate for alert testing
    status_code = 500 if random.random() < 0.05 else 200
    REQUESTS_TOTAL.labels(method="GET", endpoint="/", status=str(status_code)).inc()
    REQUEST_DURATION.labels(endpoint="/").observe(time.time() - start)
    
    log_event(
        level="ERROR" if status_code == 500 else "INFO",
        msg=f"Processed request to / with status {status_code}",
        status=status_code,
        latency_ms=round((time.time() - start) * 1000, 2)
    )
    return jsonify({"service": "demo-app", "status": "ok", "code": status_code}), status_code

@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    log_event("INFO", f"Starting Demo Telemetry Application on port {port}")
    app.run(host="0.0.0.0", port=port)
