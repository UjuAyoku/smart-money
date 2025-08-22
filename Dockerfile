# Use a small Python image
FROM python:3.11-slim-bookworm

# System packages that help matplotlib wheels run smoothly
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libfreetype6-dev libpng-dev \
  && rm -rf /var/lib/apt/lists/*

# App directory
WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py ./ 
COPY templates ./templates
COPY static ./static

# Force non-GUI backend for matplotlib (also set in your code)
ENV MPLBACKEND=Agg

# Non-root user (safer)
RUN useradd -m appuser
USER appuser

# Cloud Run routes traffic to $PORT (default 8080)
EXPOSE 8080

# Run with Gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:app"]
