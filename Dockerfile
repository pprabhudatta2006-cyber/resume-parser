# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_md

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run entrypoint script (to be created)
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
