# FILE: Dockerfile
# Use the official Python 3.11 slim image as the base image for a smaller footprint
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files and from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for compilation and WeasyPrint
# - build-essential, python3-dev, libffi-dev: Required for compiling Python packages
# - libcairo2, libpango-1.0-0, libpangocairo-1.0-0, shared-mime-info: Required for WeasyPrint
# - libgdk-pixbuf-xlib-2.0-0: Replaces the obsolete libgdk-pixbuf2.0-0 package
# - curl: Added to ensure the HEALTHCHECK command works
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi-dev \
    shared-mime-info \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt first to leverage Docker's layer caching for dependencies
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files (filtered by .dockerignore) into the container
COPY . .

# Expose port 8501 which Streamlit uses to serve the app
EXPOSE 8501

# Add a healthcheck to verify that the Streamlit app is up and running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Specify the default command to run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
