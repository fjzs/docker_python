"""
FastAPI application for the OptOps knapsack problem solver.

This module defines the main API endpoints for the web application.
It uses FastAPI, a modern Python web framework for building APIs
with automatic interactive documentation (Swagger UI). This module
is like the controller in an MVC architecture, handling incoming HTTP requests,
processing them, and returning appropriate responses. The actual business
logic for solving the knapsack problem will be implemented in separate modules, which this controller will call as needed
"""

from fastapi import FastAPI
from pydantic import BaseModel


# Initialize the FastAPI application
# FastAPI handles all the routing, validation, and documentation automatically
app = FastAPI()


# Define response models using Pydantic for explicit type validation
class GreetingResponse(BaseModel):
    """
    Response model for the root endpoint.

    Attributes:
        greeting (str): A greeting message.
    """
    greeting: str


@app.get("/", response_model=GreetingResponse)
def read_root() -> GreetingResponse:
    """
    Root endpoint - simple health check.

    Returns:
        GreetingResponse: A Pydantic model containing a greeting message.

    Example:
        GET http://localhost:8000/
        Response: {"greeting": "Hello, World!"}
    """
    return GreetingResponse(greeting="Hello, World!")
