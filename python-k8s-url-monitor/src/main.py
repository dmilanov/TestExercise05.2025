import os # Import the os module
from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from poller import Poller

app = Flask(__name__)
registry = CollectorRegistry()

# Get URLs from environment variables, with fallbacks if not set
# (though they should be set by your deployment.yaml)
url1 = os.environ.get('URL_1', "https://httpstat.us/200") # Default to 200 if URL_1 not set
url2 = os.environ.get('URL_2', "https://httpstat.us/503") # Default to 503 if URL_2 not set

url_metrics = {
    url1: {
        "up": Gauge("sample_external_url_up", "Is the external URL up", ["url"], registry=registry),
        "response_time": Gauge("sample_external_url_response_ms", "Response time in milliseconds", ["url"], registry=registry)
    },
    url2: {
        "up": Gauge("sample_external_url_up", "Is the external URL up", ["url"], registry=registry),
        "response_time": Gauge("sample_external_url_response_ms", "Response time in milliseconds", ["url"], registry=registry)
    }
}

poller = Poller()

def update_metrics():
    for url_key in url_metrics.keys(): # url_key will be the actual URL string
        status, response_time = poller.check_url(url_key)
        url_metrics[url_key]["up"].labels(url=url_key).set(status)
        url_metrics[url_key]["response_time"].labels(url=url_key).set(response_time)

@app.route("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(registry), mimetype="text/plain")

def start_server():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    start_server()