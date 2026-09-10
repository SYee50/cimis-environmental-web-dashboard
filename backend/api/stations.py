from fastapi import APIRouter
from backend.services.data_service import load_data


router = APIRouter()


@router.get("/stations")
def get_stations():
    """
    Return the available CIMIS weather stations.

    Returns:
        dict: A dictionary containing the unique CIMIS station names.
    """
    df = load_data()
    stations = df["Station Name"].unique().tolist()

    return {"stations": stations}
