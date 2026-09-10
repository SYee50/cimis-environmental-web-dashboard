from fastapi import FastAPI

from backend.api.data import router as data_router
from backend.api.stations import router as stations_router
from backend.api.summary import router as summary_router


app = FastAPI()


@app.get("/")
def home():
    """
    Return a message confirming that the CIMIS Dashboard API is running.

    Returns:
        dict: A message confirming that the API is running.
    """
    return {"message": "CIMIS Dashboard API"}


# Add routes to the main FastAPI application
app.include_router(data_router)
app.include_router(stations_router)
app.include_router(summary_router)