"""
FastAPI application for the Facility Location Optimization Problem solver.
This module defines the main API endpoints and serves the web application frontend.
It uses FastAPI, a modern Python web framework for building APIs with automatic
interactive documentation (Swagger UI). This module orchestrates:
- Static file serving (HTML, CSS, JavaScript)
- API endpoint routing
- Business logic integration
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.controllers.generate_instance import router as generate_instance_router
from app.controllers.solve_instance import router as solve_instance_router

# Initialize the FastAPI application
app = FastAPI(
    title="Facility Location Optimizer",
    description="Optimize facility placement to serve customers efficiently",
    version="2.0.0",
)

# Mount static files (CSS, JavaScript, images, etc.)
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API routers
app.include_router(generate_instance_router)
app.include_router(solve_instance_router)


@app.get("/")
def read_root():
    """
    Root endpoint - serves the landing page HTML.

    Returns the index.html file which contains the facility location UI.

    Example:
        GET http://localhost:8000/
        Response: HTML content (index.html)
    """
    return FileResponse(static_path / "index.html", media_type="text/html")