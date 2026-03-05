# Fly.io Reference

Key commands and configuration for Fly.io deployments.

## CLI Commands

```bash
# Deploy
fly deploy                          # Build and deploy
fly deploy --local-only             # Build locally (no remote builder)

# Machines
fly machine list                    # List all machines
fly machine start <id>              # Start a stopped machine
fly machine stop <id>               # Stop a running machine

# Logs and debugging
fly logs                            # Stream live logs
fly ssh console                     # SSH into running machine
fly proxy 8000:8000                 # Forward local port to machine

# Secrets
fly secrets set KEY=value           # Set encrypted secret
fly secrets list                    # List secret names (not values)
fly secrets unset KEY               # Remove a secret

# Volumes
fly volumes create <name> -r <region> -s <size_gb>
fly volumes list
fly sftp get <remote_path> <local_path>   # Download file from machine

# Scaling
fly scale count 1                   # Set machine count
fly scale vm shared-cpu-1x          # Set VM size
```

## fly.toml Structure

```toml
app = "app-name"
primary_region = "sjc"

[build]
  # Uses Dockerfile by default

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "suspend"    # "stop" | "suspend" | false
  auto_start_machines = true
  min_machines_running = 1

  [[http_service.checks]]
    grace_period = "30s"
    interval = "30s"
    method = "GET"
    path = "/healthz/"
    timeout = "5s"

[mounts]
  source = "volume_name"
  destination = "/data"

[env]
  KEY = "value"                     # Non-secret environment variables

[[vm]]
  memory = "512mb"                  # 256mb | 512mb | 1gb | 2gb
  cpu_kind = "shared"               # "shared" | "performance"
  cpus = 1
```

## Django-Specific Configuration

### Dockerfile Pattern
```dockerfile
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Use placeholder SECRET_KEY for collectstatic at build time
RUN SECRET_KEY=build-placeholder python manage.py collectstatic --noinput
EXPOSE 8000
# Migrate at startup (not release_command — volumes aren't available there)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 4"]
```

### Health Check Middleware (must be FIRST middleware)
```python
class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.path == "/healthz/":
            from django.db import connection
            from django.http import JsonResponse
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                return JsonResponse({"status": "ok"})
            except Exception as e:
                return JsonResponse({"status": "error", "detail": str(e)}, status=500)
        return self.get_response(request)
```

### Settings for Fly.io
```python
# SSL — Fly terminates TLS at edge
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True  # Safe because health check middleware runs first

# Database — path must be on mounted volume
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:////data/db.sqlite3")}

# ALLOWED_HOSTS — include Fly internal hostname
ALLOWED_HOSTS = ["app-name.fly.dev", ".yourdomain.com"]
```

## Regions

Common US regions: `sjc` (San Jose), `sea` (Seattle), `iad` (Ashburn), `ord` (Chicago), `dfw` (Dallas).

Volumes are region-locked. Machine and volume must be in the same region.
