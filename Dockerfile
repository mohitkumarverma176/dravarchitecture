FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Non-root user for security + create persistent-volume mount points
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/static/uploads/images /app/static/uploads/pdfs /app/data && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Use gunicorn for production (4 workers)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "app:app"]
