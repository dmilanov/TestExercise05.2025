class Poller:
    def __init__(self):
        self.urls = [
            "https://httpstat.us/503",
            "https://httpstat.us/200"
        ]

    def check_url(self, url):
        import time
        import requests

        start_time = time.time()
        try:
            response = requests.get(url)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            status = 1 if response.status_code == 200 else 0
        except requests.RequestException:
            response_time = (time.time() - start_time) * 1000
            status = 0

        return status, response_time

    def poll(self):
        metrics = {}
        for url in self.urls:
            status, response_time = self.check_url(url)
            metrics[url] = {
                "up": status,
                "response_ms": response_time
            }
        return metrics