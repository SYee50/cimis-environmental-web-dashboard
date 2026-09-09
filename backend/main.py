from fastapi import FastAPI
from backend.services.data_service import load_data
from backend.services.aggregation_service import aggregate_data
from typing import Optional

app = FastAPI()


@app.get("/")
def home():
    return {"message": "CIMIS Dashboard API"}


@app.get("/stations")
def get_stations():
    """
    Return the available CIMIS weather stations

    Returns:
        dict: A dictionary containing the unique CIMIS station names
    """
    df = load_data()

    stations = df["Station Name"].unique().tolist()

    return {"stations": stations}


@app.get("/data")
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
    """
    df = load_data()

    filtered_df = df[df["Station Name"] == station]

    if start_date:
        filtered_df = filtered_df[filtered_df["Date"] >= start_date]

    if end_date:
        filtered_df = filtered_df[filtered_df["Date"] <= end_date]

    filtered_df = aggregate_data(filtered_df, aggregation)

    return filtered_df.to_dict(orient="records")
