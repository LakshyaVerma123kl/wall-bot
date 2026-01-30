from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base

class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    wall_width = Column(Float, nullable=False)
    wall_height = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    

    points = relationship("TrajectoryPoint", back_populates="trajectory", cascade="all, delete-orphan")

class TrajectoryPoint(Base):
    __tablename__ = "trajectory_points"

    id = Column(Integer, primary_key=True, index=True)
    trajectory_id = Column(Integer, ForeignKey("trajectories.id"), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    sequence_order = Column(Integer, nullable=False) 

    trajectory = relationship("Trajectory", back_populates="points")

  
    __table_args__ = (
        Index('idx_traj_order', 'trajectory_id', 'sequence_order'),
    )