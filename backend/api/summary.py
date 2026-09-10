from typing import Optional
from fastapi import APIRouter, HTTPException

from backend.services.data_service import filter_data, calculate_summary


router = APIRouter()


@router.get("/summary")
def get_summary(
        station: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None):
    """
    Return summary statistics for a specified weather station
    and optional date range.

    Args:
        station (str): Name of the CIMIS weather station.
        start_date (Optional[str]): Optional start date for filtering observations.
        end_date (Optional[str]]): Optional end date for filtering observations.

    Returns:
        dict: Summary statistics for the filtered CIMIS observations.

    Raises:
        HTTPException: If the station does not exist, a date is malformed,
        or the date range is invalid.
    """
    try:
        filtered_df = filter_data(station, start_date, end_date)
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

    if filtered_df.empty:
        return {}

    summary = calculate_summary(filtered_df)

    return summary
