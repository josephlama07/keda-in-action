# KEDA in Action

A hands-on guide to implementing Kubernetes autoscaling with KEDA (Kubernetes Event-Driven Autoscaling).

## 📚 Overview

This repository contains practical examples and tutorials for setting up KEDA autoscaling in Kubernetes. Each directory represents a different scenario or use case.

## 🗂️ Project Structure

```
keda-in-action/
├── 01-basic-app-setup-with-prometheus/    # Basic Python app with Prometheus metrics and KEDA autoscaling
│   ├── app.py                             # Python HTTP server with Prometheus metrics
│   ├── Dockerfile                         # Container image definition
│   ├── k8s/                               # Kubernetes manifests
│   │   ├── python-app-deployment.yml      # Main application deployment
│   │   ├── python-service-monitor.yml     # Prometheus ServiceMonitor
│   │   ├── python-scaledobject.yml        # KEDA ScaledObject configuration
│   │   └── python-load-generator.yml      # Load generator for testing
│   └── README.md                          # Detailed setup instructions
└── README.md                              # This file
```

## 🚀 Getting Started

Each example includes its own README with detailed instructions. Start with:

```bash
cd 01-basic-app-setup-with-prometheus
```

See the [README](01-basic-app-setup-with-prometheus/README.md) for complete setup instructions.

## 📋 Prerequisites

- Kubernetes cluster (minikube, kind, or cloud)
- kubectl configured
- KEDA installed in your cluster
- Prometheus Operator (for Prometheus-based scaling)
- Docker (for building images)

## 🎯 What You'll Learn

- Setting up applications with Prometheus metrics
- Configuring KEDA ScaledObjects
- Implementing autoscaling based on custom metrics
- Testing and monitoring autoscaling behavior
- Best practices for production deployments

## 📖 Examples

### 01-basic-app-setup-with-prometheus

A complete example demonstrating:
- Python application with Prometheus metrics
- Prometheus ServiceMonitor configuration
- KEDA autoscaling based on request rate
- Load generator for testing autoscaling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available for educational purposes.
