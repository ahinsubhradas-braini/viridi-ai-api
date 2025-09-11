# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]