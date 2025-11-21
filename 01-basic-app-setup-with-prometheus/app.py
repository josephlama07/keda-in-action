#!/usr/bin/env python3
"""
Simple Python HTTP server with Prometheus metrics
Exposes metrics for KEDA autoscaling demonstrations
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import json


# Prometheus Metrics
REQUEST_COUNT = Counter(
    'python_app_requests_total',
    'Total HTTP requests received',
    ['path', 'method', 'status']
)

REQUEST_DURATION = Histogram(
    'python_app_request_duration_seconds',
    'Request duration in seconds',
    ['path', 'method'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

ACTIVE_REQUESTS = Gauge(
    'python_app_requests_in_progress',
    'Requests currently being processed'
)


class MetricsHandler(BaseHTTPRequestHandler):
    """HTTP handler with Prometheus metrics tracking."""

    def _write_response(
        self,
        body: bytes,
        status: int = 200,
        content_type: str = 'text/plain; charset=utf-8'
    ) -> None:
        """Send a byte response with common headers."""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_metrics(self):
        return generate_latest(REGISTRY), 200, 'text/plain; version=0.0.4; charset=utf-8'

    def _handle_health(self):
        return b'OK\n', 200, 'text/plain; charset=utf-8'

    def _handle_ready(self):
        payload = {'status': 'ready', 'timestamp': time.time()}
        return json.dumps(payload).encode('utf-8'), 200, 'application/json'

    def _handle_slow(self):
        time.sleep(2)
        return b'Slow response completed\n', 200, 'text/plain; charset=utf-8'

    def _handle_compute(self):
        result = sum(i * i for i in range(10000))
        payload = {'result': result, 'message': 'Computation completed'}
        return json.dumps(payload).encode('utf-8'), 200, 'application/json'

    def _handle_root(self):
        return b'Hello, World!\n', 200, 'text/plain; charset=utf-8'

    ROUTES = {
        '/metrics': '_handle_metrics',
        '/healthz': '_handle_health',
        '/ready': '_handle_ready',
        '/slow': '_handle_slow',
        '/api/compute': '_handle_compute',
        '/': '_handle_root',
    }

    def do_GET(self):
        """Handle GET requests and record metrics."""
        ACTIVE_REQUESTS.inc()
        start_time = time.time()
        status = 500

        try:
            method_name = self.ROUTES.get(self.path, '_handle_root')
            handler = getattr(self, method_name)
            body, status, content_type = handler()
            self._write_response(body, status=status, content_type=content_type)
        except Exception as error:
            body = f'Error: {error}\n'.encode('utf-8')
            self._write_response(body, status=500)
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(path=self.path, method=self.command).observe(duration)
            REQUEST_COUNT.labels(path=self.path, method=self.command, status=str(status)).inc()
            ACTIVE_REQUESTS.dec()

    def log_message(self, fmt, *args):
        """Suppress default HTTP server logging"""
        return


def main():
    """Start the HTTP server"""
    port = 8000
    server = HTTPServer(('0.0.0.0', port), MetricsHandler)
    
    print('=' * 60)
    print('Python App with Prometheus Metrics')
    print('=' * 60)
    print(f'Server running on port {port}')
    print(f'Metrics endpoint: http://localhost:{port}/metrics')
    print(f'Liveness check: http://localhost:{port}/healthz')
    print(f'Readiness check: http://localhost:{port}/ready')
    print(f'Slow endpoint: http://localhost:{port}/slow')
    print(f'Compute endpoint: http://localhost:{port}/api/compute')
    print('=' * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server...')
        server.shutdown()


if __name__ == '__main__':
    main()