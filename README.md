# k8s-observability-stack

One-command Kubernetes observability stack (Prometheus, Grafana, Loki, Alertmanager) with SRE-grade dashboards and runbook-linked alerts.

## Tech Stack

Kubernetes (kind/minikube locally, EKS-ready) · Helm · Prometheus · Grafana · Loki · Promtail · Alertmanager · Python (demo exporter)

## Quick Start

```bash
make up        # deploys the full stack via Helm with sane defaults
make demo      # deploys the sample Python microservice
make down      # tears everything down
```

Then open:
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

## What's Included

- **Dashboards** (`dashboards/`): cluster health, pod resources, app golden signals (latency / traffic / errors / saturation)
- **Alerts** (`manifests/`): Alertmanager config with severity routing (Slack webhook), silencing examples, recording rules
- **Demo app** (`demo-app/`): Python microservice emitting Prometheus metrics + structured logs — exercises the pipeline end-to-end
- **Runbooks**: the top 5 alerts each link to a runbook snippet (what to check, in order)

## Repository Layout

```
helm/values/    # prometheus, grafana, loki overrides
manifests/      # alertmanager config, recording rules
demo-app/       # python service with /metrics endpoint
dashboards/     # exported grafana JSON
Makefile
```

## What I'd Do Next

- Tempo for distributed tracing (complete the three pillars)
- Thanos/Cortex for long-term metric retention
- SLO burn-rate alerts following Google SRE workbook

---
Built by [Tarun Kumar Pardeshi](https://github.com/TarunKumarPardeshi) — Cloud & DevOps Engineer
