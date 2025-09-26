# Production-ready Dockerfile for Cloud Run
# - SSL disabled by default via env; adjust as needed later
# - Uses python:3.13-slim and installs CA bundle anyway for future enablement

FROM python:3.13-slim AS base

# Install OS CA store and minimal runtime deps
RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user (recommended for Cloud Run)
RUN useradd -m appuser
WORKDIR /app

# Copy only requirements first for efficient caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source
COPY . .

# Ensure Python can import from src
ENV PYTHONPATH=/app/src

# Default environment variables (can be overridden in Cloud Run)
ENV DATABASE_SSL_MODE=require
ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080

# Switch to non-root
USER appuser

# Start FastAPI app
# Adjust module path if your main app is different
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
