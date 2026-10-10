.PHONY: up demo down port-forward-grafana port-forward-prometheus

up:
	@echo "Deploying Prometheus, Grafana, Alertmanager, and Loki stack..."
	kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo add grafana https://grafana.github.io/helm-charts || true
	helm repo update
	helm upgrade --install prometheus prometheus-community/kube-prometheus-stack -n monitoring -f helm/values/prometheus.yaml
	helm upgrade --install loki grafana/loki-stack -n monitoring -f helm/values/loki.yaml
	kubectl apply -n monitoring -f manifests/

demo:
	@echo "Deploying Demo Telemetry Application..."
	kubectl apply -f demo-app/k8s.yaml

down:
	@echo "Uninstalling Observability Stack and demo workloads..."
	helm uninstall prometheus -n monitoring || true
	helm uninstall loki -n monitoring || true
	kubectl delete -f demo-app/k8s.yaml || true

port-forward-grafana:
	kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

port-forward-prometheus:
	kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
