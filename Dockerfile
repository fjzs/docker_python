# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app/ ./app

# Set entrypoint
CMD ["python", "app/main.py"]