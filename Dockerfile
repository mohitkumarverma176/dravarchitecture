# ── Stage 1: builder ────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install in small groups — each RUN layer has a lower memory peak.
# This lets Docker cache individual layers so a retry doesn't restart from scratch.
RUN pip install --no-cache-dir --prefix=/install \
    Flask==3.0.3 \
    Flask-WTF==1.2.1 \
    Werkzeug==3.0.3

RUN pip install --no-cache-dir --prefix=/install \
    Flask-SQLAlchemy==3.1.1 \
    SQLAlchemy==2.0.52

RUN pip install --no-cache-dir --prefix=/install \
    Flask-Login==0.6.3 \
    python-dotenv==1.0.1

# Pillow is the heaviest — isolated so it gets its own memory budget
RUN pip install --no-cache-dir --prefix=/install Pillow==12.3.0

RUN pip install --no-cache-dir --prefix=/install gunicorn

# ── Stage 2: runtime ────────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/static/uploads/images /app/static/uploads/pdfs /app/data && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "app:app"]
