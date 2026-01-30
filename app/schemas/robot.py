from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Obstacle(BaseModel):
    x: float
    y: float
    width: float
    height: float

class PathRequest(BaseModel):
    wall_width: float = Field(..., gt=0, description="Width of the wall in meters")
    wall_height: float = Field(..., gt=0, description="Height of the wall in meters")
    obstacles: List[Obstacle] = []

class PointResponse(BaseModel):
    x: float
    y: float

class TrajectoryResponse(BaseModel):
    id: int
    wall_width: float
    wall_height: float
    created_at: datetime
    
    path: List[PointResponse] 

    class Config:
        orm_mode = True