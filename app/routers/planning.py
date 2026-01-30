from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas import robot
from app.core import path_planner

router = APIRouter()

@router.post("/calculate-path", response_model=robot.TrajectoryResponse)
def create_path(request: robot.PathRequest, db: Session = Depends(get_db)):
   
    path_coords = path_planner.calculate_coverage_path(
        request.wall_width, 
        request.wall_height, 
        0.5, 
        request.obstacles
    )
    
    if not path_coords:
        raise HTTPException(status_code=400, detail="Could not generate path.")

 
    db_traj = models.Trajectory(
        wall_width=request.wall_width,
        wall_height=request.wall_height
    )
    db.add(db_traj)
    db.commit()
    db.refresh(db_traj)

   
    points_objects = [
        models.TrajectoryPoint(
            trajectory_id=db_traj.id,
            x=p[0],
            y=p[1],
            sequence_order=i
        ) for i, p in enumerate(path_coords)
    ]
    
    db.add_all(points_objects)
    db.commit()

  
    return {
        "id": db_traj.id,
        "wall_width": db_traj.wall_width,
        "wall_height": db_traj.wall_height,
        "created_at": db_traj.created_at,
        "path": [{"x": p.x, "y": p.y} for p in points_objects]
    }

@router.get("/trajectories/{trajectory_id}", response_model=robot.TrajectoryResponse)
def get_trajectory(trajectory_id: int, db: Session = Depends(get_db)):
    traj = db.query(models.Trajectory).filter(models.Trajectory.id == trajectory_id).first()
    if not traj:
        raise HTTPException(status_code=404, detail="Trajectory not found")
    
   
    return {
        "id": traj.id,
        "wall_width": traj.wall_width,
        "wall_height": traj.wall_height,
        "created_at": traj.created_at,
        "path": traj.points 
    }