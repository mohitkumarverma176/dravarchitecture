# Gunicorn configuration — optimised for 1 GB RAM (Oracle Cloud Free Tier)
# Docs: https://docs.gunicorn.org/en/stable/settings.html

bind = "0.0.0.0:5000"

# 2 workers fit comfortably in 1 GB RAM.
# Formula for memory-constrained servers: 1–2 workers per core.
workers = 2

# Sync workers are simplest and lowest overhead for a low-traffic portfolio site.
worker_class = "sync"

# Load the Flask app once in the master process before forking workers.
# Workers share the loaded code via copy-on-write — saves ~40–60 MB per worker.
preload_app = True

# Recycle workers after N requests to prevent slow memory leaks.
max_requests = 500
max_requests_jitter = 50  # randomise so workers don't all restart at once

# Kill a worker if it doesn't respond within 60 s (e.g. stuck on a DB write).
timeout = 60

# Keep connections alive for 2 s — reduces TCP handshake overhead from Nginx.
keepalive = 2

# Log to stdout so `docker compose logs` captures everything.
accesslog = "-"
errorlog  = "-"
loglevel  = "warning"  # 'info' if you want per-request logs
