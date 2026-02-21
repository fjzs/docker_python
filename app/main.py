"""
FastAPI application for the Facility Location Optimization Problem solver.

This module defines the main API endpoints and serves the web application frontend.
It uses FastAPI, a modern Python web framework for building APIs with automatic
interactive documentation (Swagger UI). This module orchestrates:
- Static file serving (HTML, CSS, JavaScript)
- API endpoint routing
- Business logic integration
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from pydantic import BaseModel
from app.controllers.facility_location_controller import router as facility_router

# Initialize the FastAPI application
# FastAPI handles all the routing, validation, and documentation automatically
app = FastAPI(
    title="Facility Location Optimizer",
    description="Optimize facility placement to serve customers efficiently",
    version="1.0.0",
)

# Mount static files (CSS, JavaScript, images, etc.)
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Include API routers
app.include_router(facility_router)


# Define response models using Pydantic for explicit type validation
class GreetingResponse(BaseModel):
    """
    Response model for the root endpoint.

    Attributes:
        greeting (str): A greeting message.
    """
    greeting: str


@app.get("/")
def read_root():
    """
    Root endpoint - serves the landing page HTML.

    Returns the index.html file which contains the facility location UI.
    This allows the application to be accessed at the root URL.

    Example:
        GET http://localhost:8000/
        Response: HTML content (index.html)
    """
    return FileResponse(static_path / "index.html", media_type="text/html")
