# Python K8s URL Monitor

This project implements a service that queries two external URLs (`https://httpstat.us/503` and `https://httpstat.us/200`), checks their status codes and response times, and exposes the metrics in Prometheus format. The service is designed to run in a Kubernetes cluster and can be easily deployed using Helm.

## Project Structure

```
python-k8s-url-monitor
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── poller.py
├── helm_chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates
│       ├── _helpers.tpl
│       ├── deployment.yaml
│       └── service.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.x
- Docker
- Kubernetes
- Helm

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd python-k8s-url-monitor
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application Locally

To run the application locally, you can execute the following command:
```
python src/main.py
```
This will start the web server and expose the metrics at `http://localhost:5000/metrics`.

## Building the Docker Image

To build the Docker image, run the following command in the project root:
```
docker build -t python-k8s-url-monitor .
```

## Deploying to Kubernetes

1. Install the Helm chart:
   ```
   helm install python-k8s-url-monitor helm_chart
   ```

2. To check the status of the deployment:
   ```
   kubectl get pods
   ```

3. To access the service, you may need to set up port forwarding:
   ```
   kubectl port-forward service/python-k8s-url-monitor 5000:5000
   ```

4. Access the metrics at `http://localhost:5000/metrics`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.