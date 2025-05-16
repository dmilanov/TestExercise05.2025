from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from poller import Poller

app = Flask(__name__)
registry = CollectorRegistry()

url_metrics = {
    "https://httpstat.us/503": {
        "up": Gauge("sample_external_url_up", "Is the external URL up", ["url"], registry=registry),
        "response_time": Gauge("sample_external_url_response_ms", "Response time in milliseconds", ["url"], registry=registry),
    },
    "https://httpstat.us/200": {
        "up": Gauge("sample_external_url_up", "Is the external URL up", ["url"], registry=registry),
        "response_time": Gauge("sample_external_url_response_ms", "Response time in milliseconds", ["url"], registry=registry),
    },
}

poller = Poller()

def update_metrics():
    for url in url_metrics.keys():
        status, response_time = poller.check_url(url)
        url_metrics[url]["up"].set(1 if status == 200 else 0)
        url_metrics[url]["response_time"].set(response_time)

@app.route("/metrics")
def metrics():
    update_metrics()
    return Response(generate_latest(registry), mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)