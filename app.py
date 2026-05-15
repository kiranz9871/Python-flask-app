# import flask framework --> used to create a web application
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import time
import random 

# __name__ helps Flask determine the root path of the application, which is important for locating resources and templates
app = Flask(__name__)

# Metric
REQUEST_COUNT = Counter('app_requests_total', 'Total requests')

# define a route for homepage  ("/") and associate it with the home function
@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "hello from flask app, your app is working fine, happy coding! 🚀,this is very simple flask app, i love learning new things, flask is so easy to use, i am enjoying it , and i love it "

# New Health Endpoint
@app.route("/health")
def health():
    return {"status": "healthy"}, 200

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