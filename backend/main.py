from fastapi import FastAPI

from backend.api.data import router as data_router
from backend.api.stations import router as stations_router


app = FastAPI()


@app.get("/")
def home():
    """
    Return a message confirming that the CIMIS Dashboard API is running.

    Returns:
        dict: A message confirming that the API is running.
    """
    return {"message": "CIMIS Dashboard API"}


# Add the routes defined in data.py to the main FastAPI application
app.include_router(data_router)

# Add the routes defined in stations.py to the main FastAPI application
app.include_router(stations_router)