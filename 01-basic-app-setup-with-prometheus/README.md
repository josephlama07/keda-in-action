# KEDA in Action - Part 1: Basic Setup with Prometheus

## 🎯 What You'll Learn

- Building a Python app with Prometheus metrics
- Containerizing with Docker
- Deploying to Kubernetes
- Setting up Prometheus ServiceMonitor for metrics collection
- Configuring KEDA autoscaling based on Prometheus metrics
- Testing autoscaling with a load generator

## 📋 Prerequisites

- Docker installed
- Kubernetes cluster (minikube, kind, or cloud)
- kubectl configured
- KEDA installed in your cluster
- Prometheus Operator installed (for ServiceMonitor)
- Docker registry access (optional, for pushing images)

## 🏗️ Project Structure

```
01-basic-app-setup-with-prometheus/
├── app.py                          # Python HTTP server with Prometheus metrics
├── Dockerfile                      # Container image definition
├── k8s/
│   ├── python-app-deployment.yml   # Main application deployment
│   ├── python-service-monitor.yml  # Prometheus ServiceMonitor
│   ├── python-scaledobject.yml     # KEDA ScaledObject for autoscaling
│   └── python-load-generator.yml   # Load generator for testing
└── README.md
```

## 🚀 Quick Start

### 1. Build Docker Image

```bash
cd 01-basic-app-setup-with-prometheus
docker build -t python-app:latest .
```

### 2. Push to Registry (Optional)

If you want to push to Docker Hub or another registry:

```bash
# Tag with your registry
docker tag python-app:latest your-registry/python-app:v1.0.0

# Push to registry
docker push your-registry/python-app:v1.0.0
```

Then update the image in `k8s/python-app-deployment.yml` to use your registry image.

### 3. Deploy Application

```bash
# Deploy the main application
kubectl apply -f k8s/python-app-deployment.yml

# Verify deployment
kubectl get pods -l app=python-app
kubectl get svc python-app
```

### 4. Configure Prometheus Monitoring

```bash
# Deploy ServiceMonitor (adjust namespace and release label if needed)
kubectl apply -f k8s/python-service-monitor.yml

# Verify ServiceMonitor
kubectl get servicemonitor -n monitoring
```

**Note:** Update the `release` label in `python-service-monitor.yml` to match your Prometheus Operator Helm release name.

### 5. Configure KEDA Autoscaling

```bash
# Deploy KEDA ScaledObject
kubectl apply -f k8s/python-scaledobject.yml

# Verify ScaledObject and HPA
kubectl get scaledobject
kubectl get hpa
```

### 6. Test the Application

```bash
# Port forward to access the app
kubectl port-forward service/python-app 8000:80

# In another terminal, test endpoints
curl http://localhost:8000/
curl http://localhost:8000/metrics
curl http://localhost:8000/healthz
curl http://localhost:8000/ready
```

## 📊 Metrics Exposed

The application exposes the following Prometheus metrics:

- `python_app_requests_total` - Total HTTP requests received (counter)
- `python_app_request_duration_seconds` - Request duration in seconds (histogram)
- `python_app_requests_in_progress` - Requests currently being processed (gauge)

## 🔗 Endpoints

- `/` - Hello World response
- `/healthz` - Liveness probe endpoint
- `/ready` - Readiness probe endpoint (returns JSON)
- `/slow` - Slow endpoint (2s delay for testing)
- `/api/compute` - CPU-intensive endpoint
- `/metrics` - Prometheus metrics endpoint

## ⚙️ KEDA Autoscaling Configuration

The ScaledObject is configured with:

- **Min Replicas:** 1
- **Max Replicas:** 5
- **Polling Interval:** 30 seconds
- **Cooldown Period:** 180 seconds
- **Scale Trigger:** Prometheus metric `sum(rate(python_app_requests_total[1m]))`
- **Threshold:** 20 requests/second
- **Activation Threshold:** 5 requests/second

**Scaling Behavior:**
- **Scale Up:** Can add 2 pods or double replicas every 30 seconds (whichever is more aggressive)
- **Scale Down:** Can remove 1 pod or 50% of replicas every 60 seconds (whichever is more conservative)

## 🧪 Testing Autoscaling

### Deploy Load Generator

```bash
# Deploy the load generator (generates ~100 requests/second: 2 replicas × 50 req/s)
kubectl apply -f k8s/python-load-generator.yml

# Monitor scaling
watch kubectl get pods -l app=python-app

# Check HPA status
kubectl get hpa keda-hpa-python-app-scaler
kubectl describe hpa keda-hpa-python-app-scaler
```

### Monitor Scaling

```bash
# Watch pods scaling up
kubectl get pods -l app=python-app -w

# Check ScaledObject status
kubectl describe scaledobject python-app-scaler

# View HPA metrics
kubectl get hpa keda-hpa-python-app-scaler -o yaml
```

### Stop Load Generator

```bash
# Scale down load generator to stop generating load
kubectl scale deployment load-generator --replicas=0

# Watch pods scale down (after cooldown period)
kubectl get pods -l app=python-app -w
```

## 🔍 Troubleshooting

### Check Application Logs

```bash
kubectl logs -l app=python-app --tail=50
```

### Check Metrics Endpoint

```bash
kubectl port-forward service/python-app 8000:80
curl http://localhost:8000/metrics
```

### Verify Prometheus is Scraping

Check Prometheus UI to verify metrics are being collected:
- Query: `python_app_requests_total`
- Query: `sum(rate(python_app_requests_total[1m]))`

### Check KEDA Status

```bash
# Check ScaledObject status
kubectl describe scaledobject python-app-scaler

# Check KEDA operator logs
kubectl logs -n keda-system -l app=keda-operator --tail=50
```

## 📝 Configuration Details

### ServiceMonitor

The ServiceMonitor tells Prometheus to scrape metrics from the `python-app` service:
- Scrapes from port `http` at path `/metrics`
- Scraping interval: 30 seconds
- Must match the `release` label of your Prometheus Operator installation

### ScaledObject

The ScaledObject defines how KEDA should scale the `python-app` deployment:
- Uses Prometheus query: `sum(rate(python_app_requests_total[1m]))`
- Scales when request rate exceeds 20 requests/second
- Includes fallback behavior if metrics are unavailable

### Load Generator

The load generator creates synthetic load for testing:
- 2 replicas generating 50 requests/second each
- Total: ~100 requests/second
- Uses Vegeta load testing tool for controlled, consistent load
- Runs for 1 hour duration

## ⏭️ Next Steps

- Experiment with different threshold values
- Try different scaling policies
- Monitor resource usage during scaling
- Test with different load patterns
