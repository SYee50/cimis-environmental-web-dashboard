from typing import Optional

from fastapi import APIRouter, HTTPException

from backend.services.data_service import filter_data
from backend.services.aggregation_service import aggregate_data


router = APIRouter()


@router.get("/data")
def get_data(
        station: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        aggregation: str = "daily"):
    """
    Return CIMIS observations for a specified weather station and optional date range.

    Args:
        station (str): Name of the CIMIS weather station.
        start_date (Optional[str]): Optional start date for filtering observations.
        end_date (Optional[str]): Optional end date for filtering observations.
        aggregation (str): Aggregation level: "daily", "monthly", or "annual".

    Returns:
        list: CIMIS observations matching the specified filters and aggregation level.

    Raises:
        HTTPException: If the station does not exist, the aggregation level is invalid,
        a date is malformed, or the date range is invalid.
    """
    # Validate aggregation
    valid_aggregations = {"daily", "monthly", "annual"}

    if aggregation not in valid_aggregations:
        raise HTTPException(
            status_code=400,
            detail="Aggregation must be 'daily', 'monthly', or 'annual'."
        )

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

    # Return an empty list if the valid query has no matching observations
    if filtered_df.empty:
        return []

    # Aggregate the filtered observations
    filtered_df = aggregate_data(filtered_df, aggregation)

    return filtered_df.to_dict(orient="records")
