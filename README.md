# 🚀 Production-Style DevOps Platform for Flask

A production-oriented DevOps implementation for a containerized Python Flask application, demonstrating **CI/CD, containerization, Kubernetes orchestration, Helm, GitOps with Argo CD, and observability with Prometheus and Grafana**.

The project is designed as a hands-on DevOps/SRE platform rather than a simple Flask application. It demonstrates how an application can move from source code through automated validation and containerization into Kubernetes, with health checks, monitoring, metrics, and operational testing.

---

## 📌 Project Overview

This project demonstrates an end-to-end DevOps workflow for deploying and operating a Flask application.

The application is:

* Containerized using Docker
* Deployed to Kubernetes
* Packaged using Helm
* Exposed through NGINX Ingress
* Managed using Argo CD following GitOps principles
* Monitored using Prometheus
* Visualized using Grafana
* Instrumented with application metrics
* Tested using health, latency, and failure simulation endpoints
* Integrated with CI/CD and container security scanning

The project is currently designed for a **local Kubernetes environment using Minikube**, allowing the complete workflow to be practiced without requiring a production cloud environment.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Developer       │
                         │                      │
                         │ Git / GitHub         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    GitHub Actions    │
                         │                      │
                         │ CI / Validation      │
                         │ Security Scanning    │
                         │ Docker Build         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Container Image   │
                         │        Docker        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │           Argo CD             │
                    │          GitOps                │
                    │                               │
                    │ Desired State → Kubernetes    │
                    └──────────────┬────────────────┘
                                   │
                                   ▼
             ┌──────────────────────────────────────────┐
             │                Kubernetes                 │
             │                 Minikube                  │
             │                                          │
             │  ┌───────────────┐                       │
             │  │    Ingress    │                       │
             │  │    NGINX      │                       │
             │  └───────┬───────┘                       │
             │          │                                │
             │          ▼                                │
             │  ┌───────────────┐                       │
             │  │ Flask Service │                       │
             │  └───────┬───────┘                       │
             │          │                                │
             │          ▼                                │
             │  ┌───────────────┐                       │
             │  │ Flask Pods    │                       │
             │  │ Gunicorn      │                       │
             │  └───────┬───────┘                       │
             │          │                                │
             └──────────┼────────────────────────────────┘
                        │
                        │ /metrics
                        ▼
              ┌──────────────────────┐
              │     Prometheus       │
              │                      │
              │ Metrics Collection   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │       Grafana        │
              │                      │
              │ Dashboards           │
              │ RPS / CPU / Services │
              └──────────────────────┘
```

---

# 🛠️ Technology Stack

| Area               | Technology               |
| ------------------ | ------------------------ |
| Application        | Python / Flask           |
| Application Server | Gunicorn                 |
| Containerization   | Docker                   |
| Orchestration      | Kubernetes               |
| Local Kubernetes   | Minikube                 |
| Package Management | Helm                     |
| Ingress            | NGINX Ingress Controller |
| GitOps             | Argo CD                  |
| CI/CD              | GitHub Actions           |
| Monitoring         | Prometheus               |
| Visualization      | Grafana                  |
| Metrics            | Prometheus Client        |
| Security Scanning  | Trivy                    |
| Load Testing       | ApacheBench              |
| Version Control    | Git / GitHub             |

---

# 📂 Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── flask-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── .helmignore
│   │
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── serviceaccount.yaml
│       ├── configmap.yaml
│       └── _helpers.tpl
│
├── ingress.yaml
├── servicemonitor.yaml
│
├── ai-agent/
│   └── ai_debug.py
│
└── README.md
```

---

# 🚀 Application

The Flask application exposes several endpoints for application functionality and operational testing.

| Endpoint   | Purpose                    |
| ---------- | -------------------------- |
| `/`        | Main application response  |
| `/live`    | Kubernetes liveness check  |
| `/ready`   | Kubernetes readiness check |
| `/metrics` | Prometheus metrics         |
| `/slow`    | Simulated latency          |
| `/error`   | Simulated HTTP 500 failure |

---

# ❤️ Health Checks

The application provides dedicated Kubernetes health endpoints.

### Liveness

`/live`

Used to determine whether the application process is alive.

Example response:

```json
{
  "status": "alive"
}
```

### Readiness

`/ready`

Used to determine whether the application is ready to receive traffic.

Example response:

```json
{
  "status": "ready"
}
```

These endpoints allow Kubernetes probes to distinguish between:

* Application process failure
* Application not ready to receive traffic

---

# 📊 Application Metrics

The Flask application exposes:

`/metrics`

Prometheus-compatible metrics are generated using the Python Prometheus client.

The application currently exposes a request counter:

```text
app_requests_total
```

Prometheus periodically scrapes this endpoint through the Kubernetes `ServiceMonitor`.

---

# 📈 Prometheus

Prometheus is used to collect application and Kubernetes metrics.

The project includes:

`servicemonitor.yaml`

The ServiceMonitor configures Prometheus to discover the Flask service and scrape:

```text
/metrics
```

with a:

```text
15 second
```

scrape interval.

The ServiceMonitor targets the Flask service in the Kubernetes `default` namespace.

---

# 📊 Grafana

Grafana is used to visualize the collected metrics.

The monitoring setup is used to observe operational information such as:

* Application request rate
* Service/pod information
* CPU utilization
* Kubernetes workload health
* Application behavior during load testing

The dashboard provides an operational view of the application rather than relying only on application logs.

---

# 🔥 Load Testing

ApacheBench (`ab`) is used to generate application traffic and validate application behavior under load.

Example:

```bash
ab -n 10000 -c 50 http://flask.local/
```

Higher-concurrency testing can also be performed:

```bash
ab -n 100000 -c 100 http://flask.local/
```

The generated traffic can then be observed through:

**Application → Prometheus → Grafana**

This allows request-rate behavior and resource utilization to be correlated during testing.

---

# 🧪 Failure Testing

The application contains endpoints specifically designed to simulate operational conditions.

### Latency Simulation

```text
/slow
```

The endpoint introduces a random delay between approximately 1 and 3 seconds.

This can be used to study:

* Request latency
* User-facing response behavior
* Monitoring signals
* Performance under slow dependencies

### HTTP 500 Simulation

```text
/error
```

Returns an HTTP `500` response.

This allows testing of:

* Application error monitoring
* Prometheus metrics
* Grafana visualization
* Incident troubleshooting workflows

These endpoints are intended for **controlled testing**, not production business functionality.

---

# 🐳 Docker

The application is containerized using Docker.

The Docker image packages:

* Python runtime
* Flask application
* Application dependencies
* Gunicorn application server

The application listens on port:

```text
5000
```

The container is designed to run the same application that is deployed into Kubernetes.

---

# ☸️ Kubernetes

The application is deployed to Kubernetes using a Helm chart.

The Kubernetes deployment manages:

* Application Pods
* Service
* ConfigMap
* ServiceAccount
* Application configuration

The application runs behind a Kubernetes Service and is exposed externally through NGINX Ingress.

---

# 📦 Helm

The Kubernetes deployment is packaged as a Helm chart.

Chart location:

```text
flask-chart/
```

The chart separates:

* Application configuration
* Deployment configuration
* Service configuration
* ConfigMap configuration
* ServiceAccount configuration

This makes Kubernetes deployment configuration easier to manage and reproduce.

---

# 🌐 Ingress

NGINX Ingress provides external HTTP routing to the Flask application.

Configured hostname:

```text
flask.local
```

Traffic flow:

```text
Browser
   ↓
NGINX Ingress
   ↓
Kubernetes Service
   ↓
Flask Pod
```

For local testing, the hostname must resolve to the Minikube environment.

---

# 🔄 GitOps with Argo CD

Argo CD is used to implement a GitOps-style deployment workflow.

Instead of manually changing Kubernetes resources repeatedly, the desired deployment configuration is maintained in Git.

Conceptually:

```text
Git Repository
      ↓
   Argo CD
      ↓
Kubernetes Cluster
      ↓
Flask Application
```

Argo CD continuously compares the desired state with the Kubernetes cluster state.

This provides:

* Declarative deployments
* Git-based change history
* Deployment visibility
* Drift detection
* Repeatable application delivery

---

# ⚙️ CI/CD

GitHub Actions is used for continuous integration.

The CI workflow is responsible for automating validation and security-related checks before changes progress through the delivery workflow.

The project also uses **Trivy** for container security scanning.

The overall workflow is:

```text
Git Push
   ↓
GitHub Actions
   ↓
Application Validation
   ↓
Security Scan
   ↓
Docker Build
   ↓
Deployment Workflow
```

The exact workflow can be found at:

```text
.github/workflows/ci.yml
```

---

# 🔐 Security

Security is treated as part of the delivery process rather than as a separate activity.

The project uses Trivy to identify known vulnerabilities in container images.

Security scanning helps identify:

* Vulnerable operating-system packages
* Vulnerable application dependencies
* Container image security issues

The goal is to catch security problems earlier in the software delivery lifecycle.

---

# 🖥️ Local Environment

The project is currently designed to run locally using:

* Minikube
* Docker
* Kubernetes
* Helm
* Argo CD
* Prometheus
* Grafana

This provides a complete environment for practicing cloud-native DevOps concepts without requiring a continuously running AWS environment.

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/kiranz9871/Python-flask-app.git
```

```bash
cd Python-flask-app
```

---

## 2. Create a Python virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Run Flask locally

```bash
python app.py
```

The application listens on:

```text
http://localhost:5000
```

Test:

```bash
curl http://localhost:5000/
```

---

# 🐳 Run with Docker

Build the image:

```bash
docker build -t flask-app .
```

Run the container:

```bash
docker run -d --name flask-app -p 5000:5000 flask-app
```

Test:

```bash
curl http://localhost:5000/
```

Check metrics:

```bash
curl http://localhost:5000/metrics
```

---

# ☸️ Deploy to Minikube

Start Minikube:

```bash
minikube start
```

Verify the cluster:

```bash
kubectl get nodes
```

Check namespaces:

```bash
kubectl get namespaces
```

Install the Helm release:

```bash
helm upgrade --install flask-app ./flask-chart
```

Check the deployment:

```bash
kubectl get deployments
```

Check Pods:

```bash
kubectl get pods
```

Check the Service:

```bash
kubectl get svc
```

---

# 🌐 Access the Application

Verify the Ingress:

```bash
kubectl get ingress
```

The application is configured for:

```text
http://flask.local
```

Verify application health:

```bash
curl http://flask.local/live
```

```bash
curl http://flask.local/ready
```

Verify metrics:

```bash
curl http://flask.local/metrics
```

---

# 📊 Verify Monitoring

Check monitoring components:

```bash
kubectl get pods -n monitoring
```

Check Prometheus:

```bash
kubectl get svc -n monitoring
```

Check Grafana:

```bash
kubectl get svc -n monitoring
```

Verify the ServiceMonitor:

```bash
kubectl get servicemonitor -n monitoring
```

The Flask application's `/metrics` endpoint should be discovered by Prometheus through the ServiceMonitor configuration.

---

# 🔎 Useful Kubernetes Troubleshooting Commands

### Application Pods

```bash
kubectl get pods
```

### Detailed Pod information

```bash
kubectl describe pod <pod-name>
```

### Application logs

```bash
kubectl logs <pod-name>
```

### Follow application logs

```bash
kubectl logs -f <pod-name>
```

### Deployment status

```bash
kubectl rollout status deployment/<deployment-name>
```

### Service

```bash
kubectl get svc
```

### Ingress

```bash
kubectl describe ingress flask-ingress
```

### Events

```bash
kubectl get events --sort-by=.lastTimestamp
```

These commands are useful when troubleshooting:

* CrashLoopBackOff
* ImagePullBackOff
* Pending Pods
* Failed health probes
* Service routing problems
* Ingress issues
* Configuration problems

---

# 🧠 DevOps/SRE Concepts Demonstrated

This project provides hands-on experience with:

### Infrastructure & Platform

* Containers
* Docker
* Kubernetes
* Helm
* Kubernetes Services
* Ingress
* ConfigMaps
* ServiceAccounts

### CI/CD

* Git
* GitHub
* GitHub Actions
* Automated validation
* Container builds
* Security scanning

### GitOps

* Argo CD
* Declarative deployments
* Desired vs actual state
* Deployment synchronization

### Observability

* Prometheus
* Grafana
* Application metrics
* ServiceMonitor
* Request-rate monitoring
* CPU/resource monitoring
* Health checks
* Failure simulation
* Load testing

### Reliability

* Liveness checks
* Readiness checks
* Latency simulation
* HTTP failure simulation
* Kubernetes troubleshooting
* Application monitoring

---

# 🔧 Troubleshooting Approach

When an application is unavailable, troubleshooting follows a layered approach.

```text
1. Application
       ↓
2. Container
       ↓
3. Pod
       ↓
4. Deployment
       ↓
5. Service
       ↓
6. Ingress
       ↓
7. Kubernetes
       ↓
8. Monitoring
```

For example:

### Application not responding

Check:

```bash
kubectl get pods
```

Then:

```bash
kubectl logs <pod-name>
```

Then:

```bash
kubectl describe pod <pod-name>
```

Then check the Service:

```bash
kubectl get svc
```

Then check Ingress:

```bash
kubectl get ingress
```

This approach prevents random troubleshooting and helps isolate the failure layer.

---

# 📈 Observability Workflow

The project demonstrates the following monitoring flow:

```text
Flask Application
       │
       │ /metrics
       ▼
ServiceMonitor
       │
       ▼
Prometheus
       │
       ▼
PromQL
       │
       ▼
Grafana
       │
       ▼
Operational Dashboard
```

Load testing can be introduced at the application layer:

```text
ApacheBench
     ↓
Flask
     ↓
Prometheus
     ↓
Grafana
```

This provides a practical way to understand how application traffic affects observable system behavior.

---

# 💼 Why This Project Matters

This project demonstrates more than simply deploying a Flask application.

It brings together the major stages of a modern DevOps workflow:

```text
Source Control
      ↓
CI/CD
      ↓
Security
      ↓
Containerization
      ↓
Kubernetes
      ↓
Helm
      ↓
GitOps
      ↓
Observability
      ↓
Operational Testing
```

The project can therefore be used as a practical environment for studying **DevOps, Platform Engineering, SRE, Kubernetes, CI/CD, and cloud-native operations**.

---

# 🗺️ Future Improvements

The current implementation can be extended toward a production cloud architecture.

Planned improvements include:

* AWS infrastructure using Terraform
* VPC and subnet architecture
* IAM roles and policies
* EKS deployment
* AWS Load Balancer integration
* Route 53
* CloudWatch
* Kubernetes HPA
* CPU and memory-based autoscaling
* Alertmanager alerting
* Centralized logging
* Advanced Prometheus metrics
* Deployment strategies such as rolling and blue/green deployments
* Infrastructure security scanning with Checkov
* Secret management
* Remote Terraform state
* Multi-environment configuration
* Disaster/failure testing
* Cost-aware AWS infrastructure design

These improvements will extend the local Kubernetes platform toward a more complete cloud platform.

---

# 📚 Key Interview Topics Covered

This project provides practical examples for discussing:

* How CI/CD pipelines work
* How GitOps works
* How Argo CD synchronizes applications
* Kubernetes Deployments and Services
* Kubernetes health probes
* Ingress vs Service
* Helm charts
* Prometheus and Grafana
* ServiceMonitor
* Application metrics
* Load testing
* Container security scanning
* Docker image creation
* Kubernetes troubleshooting
* Application failure simulation
* Observability and monitoring
* DevOps/SRE operational practices

---

# 👨‍💻 Author

**Kiran Zirpe**

DevOps / Cloud / Platform Engineering

Focused on:

* AWS
* Kubernetes
* Docker
* Terraform
* CI/CD
* GitOps
* Observability
* Infrastructure Automation

---

# ⭐ Project Goal

The goal of this project is to continuously evolve a simple Flask application into a **production-style DevOps platform**, demonstrating the complete lifecycle of building, delivering, deploying, monitoring, and troubleshooting a cloud-native application.
