<!-- last_verified: 2026-03-05 -->
# Fly.io Gotchas

Common deployment pitfalls on Fly.io, learned from real failures.

## Volume Mounts

- **Release commands run in ephemeral machines WITHOUT volume mounts.** If your app uses SQLite or any file-based storage on a volume, `release_command` will fail with "unable to open database file". Move migrations to the CMD entrypoint instead.
- Volumes are pinned to a single region and a single machine. You cannot scale horizontally with volumes.
- If a volume mount path doesn't exist in the image, Fly creates it — but the directory will be owned by root.

## Health Checks

- Fly health checks hit `localhost:<internal_port>` over plain HTTP from inside the machine.
- If `localhost` is not in `ALLOWED_HOSTS` (Django, Rails, etc.), the framework returns 400 Bad Request and health checks fail silently with "timeout waiting for health checks to pass".
- If `SECURE_SSL_REDIRECT=True`, the health check HTTP request gets redirected to HTTPS, causing a loop/timeout.
- **Fix pattern:** Add a health check middleware as the FIRST middleware in the stack, responding before host validation or SSL redirect logic runs.
- `grace_period` should be >= app startup time. For Django + SQLite migrate, 30s is a safe default.

## Secrets vs Environment Variables

- `fly secrets set` stores encrypted secrets, injected as env vars at runtime.
- `[env]` in `fly.toml` stores non-secret config (visible in the toml file).
- Secrets are NOT available at build time (Dockerfile RUN commands). If a build step needs a secret (e.g., `collectstatic` needs `SECRET_KEY`), use a placeholder: `RUN SECRET_KEY=build-placeholder python manage.py collectstatic --noinput`.

## Machine Lifecycle

- `auto_stop_machines = "suspend"` suspends idle machines instead of stopping them. Resume is faster (~2s vs ~10s cold start) but uses some memory.
- `min_machines_running = 1` keeps at least one machine warm. Without this, first request after idle triggers a cold start.
- Machines are ephemeral by default — anything written outside a volume mount is lost on restart.

## SQLite on Fly.io

- Works well for single-machine deployments with a volume mount.
- Set WAL mode and busy_timeout for concurrency: `PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;`
- Database path must be on the mounted volume (e.g., `/data/db.sqlite3`), not in the app directory.
- Backups: use `fly ssh console` + `sqlite3 /data/db.sqlite3 ".backup /data/backup.sqlite3"` then `fly sftp get`.

## Networking

- Internal services communicate via `<app-name>.internal` DNS (Fly private network).
- `fly proxy 8000:8000` forwards local traffic to the remote machine — useful for debugging.
- Fly terminates TLS at the edge. The app sees plain HTTP. Use `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")` to detect HTTPS.

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| "timeout waiting for health checks" | Health check endpoint returning non-2xx | Check ALLOWED_HOSTS, SSL redirect, middleware order |
| "unable to open database file" | SQLite path not on volume, or release_command | Move DB to volume path, move migrations to CMD |
| "no machines in group" | All machines stopped/crashed | `fly machine start` or check logs with `fly logs` |
| "volume not found" | Volume in different region than machine | Create volume in target region: `fly volumes create <name> -r <region>` |
