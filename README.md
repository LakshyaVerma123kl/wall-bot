# Wall-Bit: Autonomous Wall-Finishing Robot Control System

## Overview

This project is a robust, server-intensive control system designed for an autonomous wall-finishing robot. It generates optimized coverage paths (Boustrophedon) while handling user-defined obstacles and persists trajectory data for analysis and playback.

The system is architected to handle high-concurrency demands through optimized database configurations and custom middleware logging.

## 🛠 Technical Architecture

### 1. Path Planning Algorithm (The Brain)

- **Strategy:** Boustrophedon Cellular Decomposition (Lawnmower Pattern).
- **Implementation:** The system discretizes the wall surface into vertical strips based on the tool width (50cm). It performs AABB (Axis-Aligned Bounding Box) collision detection against user-defined obstacles to interrupt and resume paths dynamically.

### 2. Backend & Data Layer (The "Overkill" Optimizations)

- **Framework:** FastAPI (Python).
- **Database:** SQLite with SQLAlchemy.
- **Optimizations:**
  - **Indexing:** A composite index on `(trajectory_id, sequence_order)` was implemented to ensure $O(\log N)$ retrieval times for path playback, regardless of table size.
  - **Concurrency:** SQLite **WAL (Write-Ahead Logging) Mode** is enabled with increased timeouts. This allows the frontend to read visualization data while the backend simultaneously calculates and writes new path segments, preventing database locks during intensive computations.
- **Observability:** Custom Middleware injects a microsecond-precision `X-Process-Time` header into every response for real-time latency monitoring.

### 3. Frontend Visualization

- **Engine:** HTML5 Canvas API (No Matplotlib).
- **Features:**
  - Real-time trajectory playback.
  - Dynamic scaling for different wall aspect ratios.
  - "Intelligent" logs that explain the robot's current sector and status.

## 🚀 Setup & Installation

1.  **Clone the Repository**

    ```bash
    git clone [https://github.com/LakshyaVerma123kl/wall-bot](https://github.com/LakshyaVerma123kl/wall-bot)
    cd wall-bit-assignment
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Server**

    ```bash
    uvicorn app.main:app
    ```

    _Note: The server runs on port 8000._

4.  **Launch Visualization**
    Open `frontend/index.html` in any modern browser.

## 🧪 Testing

The project includes a `pytest` suite validating CRUD operations, path generation logic, and response timing constraints.

```bash
python -m pytest -v -s
```

## Frontend Link

[\[Link to frontend\]]
(http://127.0.0.1:8000/)

## 🎥 Video Walkthrough

[\[Link to your video walkthrough here\]](https://www.loom.com/share/b4eff89132944d71a68909b9a2cf0c12)
