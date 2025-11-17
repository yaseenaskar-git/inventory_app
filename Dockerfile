# Simple single-stage Dockerfile for inventory app

FROM python:3.13-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements (binary only to avoid building from source)
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Expose port (Cloud Run uses 8080)
EXPOSE 8080

# Set environment for Cloud Run
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run Django on port 8080 for Cloud Run (use PORT env variable)
CMD ["python", "manage.py", "runserver", "0.0.0.0:${PORT:-8080}"]
