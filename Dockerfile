# Backend Dockerfile for Flask app
# Uses official Python image and runs with gunicorn for production

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Ensure known env defaults (can be overridden in host/CI)
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000

# Use gunicorn to run the Flask app (run:app exports the app object)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app", "--workers", "2", "--threads", "2"]
