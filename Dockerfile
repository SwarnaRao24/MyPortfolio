# Use a slim, lightweight official Python runtime
FROM python:3.11-slim

# Set environment variables to optimize Python inside the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed for compiling packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy your dependencies file first to leverage Docker caching layers
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django app code into the container
COPY . /app/

# Expose port 8000 for web traffic
EXPOSE 8000

# Run collectstatic to prepare assets, then start the production server (Gunicorn)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]