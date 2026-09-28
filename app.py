# import flask framework --> used to create a web application
import os
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time
import random

# __name__ helps Flask determine the root path of the application, which is important for locating resources and templates
app = Flask(__name__)

# Read values from ConfigMap
APP_NAME = os.getenv("APP_NAME", "Default Flask App")
ENV = os.getenv("ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Metric
REQUEST_COUNT = Counter('app_requests_total', 'Total requests')

# define a route for homepage  ("/") and associate it with the home function
@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hi Argo CD ,i like to learn"

# Liveness endpoint
# Kubernetes uses this to determine whether the application process is alive.
@app.route("/live")
def live():
    return {"status": "alive"}, 200

# Readiness endpoint
# Kubernetes uses this to determine whether the application can receive traffic.
@app.route("/ready")
def ready():
    return {"status": "ready"}, 200

# Metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Slow endpoint (simulate latency)
@app.route("/slow")
def slow():
    REQUEST_COUNT.inc()
    delay = random.uniform(1, 3)  # random delay between 1–3 seconds
    time.sleep(delay)
    return {
        "message": "Slow response",
        "delay": round(delay, 2)
    }

# Error endpoint (simulate failure)
@app.route("/error")
def error():
    REQUEST_COUNT.inc()
    return {
        "error": "Something went wrong!"}, 500

# Entry point of the application, it runs the Flask app in debug mode on port 5000
# Run app on:
    # host="0.0.0.0" → allows external access (Docker/K8s REQUIRED)
    # port=5000 → app runs on port 5000
if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
