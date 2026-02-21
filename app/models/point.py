"""
Point Model

Represents a 2D point on the facility location grid.
"""

from pydantic import BaseModel, Field


class Point(BaseModel):
    """
    Represents a 2D point on the grid.

    Attributes:
        x: X-coordinate (0 to 100)
        y: Y-coordinate (0 to 100)
    """
    x: float = Field(ge=0, le=100, description="X-coordinate on 100x100 grid")
    y: float = Field(ge=0, le=100, description="Y-coordinate on 100x100 grid")

