# CMD is a command executed at container start time.
# RUN is a command executed at container build time.

# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app

# Expose the port FastAPI will use
EXPOSE 8000

# - Why uvicorn:
# Is a lightweight, high-performance ASGI (Asynchronous Server Gateway Interface) web server for Python. It provides the runtime layer that allows modern
# asynchronous frameworks—such as FastAPI to handle concurrent HTTP and WebSocket connections efficiently. Built for speed and simplicity, it’s widely adopted in the
# Python web ecosystem for both development and production deployments. This is the engine that serves HTTP requests and is listening to a port.

# Why app.main:app
# app → folder
# main → file main.py
# app → FastAPI object inside that file
# So within app/main.py I should have the app object instantiating FastAPI()
#
# Why --host", 0.0.0.0:
# Inside the container 127.0.0.1 means "inside the container only"
# Inside the container 0.0.0.0 means "listen on all network interfaces" -> this to make my browser be able to reach it
#
# Why --port, 8000:
# This tells Uvicorn to listen on port 8000 inside the container
# When I run the container like this: `docker run -p 8000:8000 optimization-api`
# Docker:
# 1. Creates the container
# 2. Starts it
# 3. Executes the CMD line
# 4. Runs: uvicorn app.main:app --host 0.0.0.0 --port 8000
# 5. Uvicorn starts listening
# Note 1: the container needs a foreground process. A container runs as long as the main process runs. Here uvicorn is the main process. If it stops, the container stops.
# Note 2: uvicorn is a single-worker by default, if you need concurrency you may want to use gunicorn.
#
# Summary: the meaning is: When this container starts, run my FastAPI application using Uvicorn, listen on all interfaces, and expose it on port 8000.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]