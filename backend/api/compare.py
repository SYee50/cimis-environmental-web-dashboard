from typing import Optional
from fastapi import APIRouter, HTTPException
from backend.services.data_service import compare_stations


router = APIRouter()


@router.get("/compare")
def get_comparison(
        stations: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        aggregation: str = "daily"):
    """
    Return CIMIS observations for multiple weather stations.

    Args:
        stations (str): Comma-seperated CIMIS weather station names.
        start_date (Optional[str]): Optional start date for filtering observations.
        end_date (Optional[str]): Optional end date for filtering observations.
        aggregation (str): Aggregation level: "daily", "monthly", or "annual".

    Returns:
        dict: CIMIS observations grouped by weather station.

    Raises:
        HTTPException: If a station does not exist, the aggregation level
        is invalid, a date is malformed, or the date range is invalid.
    """
    valid_aggregations = {"daily", "monthly", "annual"}

    if aggregation not in valid_aggregations:
        raise HTTPException(
            status_code=400,
            detail="Aggregation must be 'daily', 'monthly', or 'annual'."
        )

    station_list = []
    for station in stations.split(","):
        if station.strip():
            station_list.append(station.strip())

    try:
        return compare_stations(
            station_list,
            start_date,
            end_date,
            aggregation
        )
    except ValueError as error:
        if "not found" in str(error):
            raise HTTPException(
                status_code=404,
                detail=str(error)
            )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
