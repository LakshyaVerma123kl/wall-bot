import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import planning
from app.db import models
from app.db.session import engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

models.Base.metadata.create_all(bind=engine)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("robot_server.log"), logging.StreamHandler()]
)
logger = logging.getLogger("RobotControl")

app = FastAPI(title="Wall-Finishing Robot API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000 
    formatted_process_time = "{0:.2f}".format(process_time)
    
 
    logger.info(
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Status: {response.status_code} | "
        f"Time: {formatted_process_time}ms"
    )
    
   
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


app.include_router(planning.router, prefix="/api/v1", tags=["planning"])
app.mount("/static", StaticFiles(directory="frontend"), name="static")
@app.get("/")
def read_root():
    return FileResponse('frontend/index.html')