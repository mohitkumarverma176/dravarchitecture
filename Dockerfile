# ── Stage 1: builder ────────────────────────────────────────────────────────
# Install all deps into an isolated prefix; builder stage is discarded after.
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    pip install --no-cache-dir --prefix=/install gunicorn

# ── Stage 2: runtime ────────────────────────────────────────────────────────
# Clean slim image — no pip, no build tools, no cache. Smaller & less RAM.
FROM python:3.12-slim

WORKDIR /app

# Pull only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Non-root user for security + create persistent-volume mount points
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/static/uploads/images /app/static/uploads/pdfs /app/data && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Gunicorn reads gunicorn.conf.py automatically
CMD ["gunicorn", "app:app"]
