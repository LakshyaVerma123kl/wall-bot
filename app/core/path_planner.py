from typing import List, Tuple
from pydantic import BaseModel


class Obstacle(BaseModel):
    x: float
    y: float
    width: float
    height: float

def calculate_coverage_path(
    wall_width: float, 
    wall_height: float, 
    tool_width: float, 
    obstacles: List[Obstacle]
) -> List[Tuple[float, float]]:
    
    path = []
    
    
    step_size = tool_width 
    
    x = 0.0
    moving_up = True
    
    while x <= wall_width:
      
        
        if moving_up:
            y_start, y_end, step = 0.0, wall_height, 0.1 
        else:
            y_start, y_end, step = wall_height, 0.0, -0.1
            
        current_y = y_start
        
        
        while (moving_up and current_y <= y_end) or (not moving_up and current_y >= y_end):
            if not is_colliding(x, current_y, obstacles):
                path.append((round(x, 2), round(current_y, 2)))
            else:
               
                pass
                
            current_y += step
            
        
        x += step_size
        moving_up = not moving_up
        
    return path

def is_colliding(x: float, y: float, obstacles: List[Obstacle]) -> bool:

    for obs in obstacles:
     
        if (obs.x <= x <= obs.x + obs.width) and \
           (obs.y <= y <= obs.y + obs.height):
            return True
    return False