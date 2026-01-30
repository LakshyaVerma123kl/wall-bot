import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


valid_payload = {
    "wall_width": 5.0,
    "wall_height": 5.0,
    "obstacles": [
        {"x": 2.0, "y": 2.0, "width": 1.0, "height": 1.0}
    ]
}

def test_read_root():
  
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Robot Control System Online"}

def test_calculate_path_creation():
   
    response = client.post("/api/v1/calculate-path", json=valid_payload)
    

    assert response.status_code == 200
    

    data = response.json()
    assert "id" in data
    assert "path" in data
    assert len(data["path"]) > 0 
    assert data["wall_width"] == 5.0

    
    assert "X-Process-Time" in response.headers
    process_time = float(response.headers["X-Process-Time"])
    print(f"\n[Perf] Path calculation took: {process_time:.2f}ms")
    assert process_time > 0

def test_get_trajectory():
  
    create_res = client.post("/api/v1/calculate-path", json=valid_payload)
    traj_id = create_res.json()["id"]


    response = client.get(f"/api/v1/trajectories/{traj_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == traj_id
 
    assert data["path"][0]["x"] == 0.0 

def test_invalid_dimensions():
  
    invalid_payload = valid_payload.copy()
    invalid_payload["wall_width"] = -5
    
    response = client.post("/api/v1/calculate-path", json=invalid_payload)
    assert response.status_code == 422 