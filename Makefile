up:
	helm upgrade --install prometheus prometheus-community/kube-prometheus-stack -f helm/values/prometheus.yaml
	helm upgrade --install loki grafana/loki-stack -f helm/values/loki.yaml
	kubectl apply -f manifests/

demo:
	kubectl apply -f demo-app/

down:
	helm uninstall prometheus loki || true
