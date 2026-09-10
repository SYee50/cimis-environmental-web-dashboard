from datetime import datetime
from typing import Optional
import pandas as pd


DATA_PATH = "data/cimis_daily_clean.csv"


def load_data():
    """
    Load the cleaned CIMIS dataset and convert dates to datetime objects.

    Returns:
        pandas.DataFrame: The CIMIS observations with dates converted
        to datetime format for filtering and aggregation.
    """
    df = pd.read_csv(DATA_PATH)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


def filter_data(
        station: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None):
    """
    Filter CIMIS observations by station and optional date range.

    Args:
        station (str): Name of the CIMIS weather station.
        start_date (Optional[str]): Optional start date in YYYY-MM-DD format.
        end_date (Optional[str]): Optional end date in YYYY-MM-DD format.

    Returns:
        pandas.DataFrame: CIMIS observations matching the specified filters.

    Raises:
        ValueError: If the dataset is empty, the station does not exist,
        a date is malformed, or the date range is invalid.
    """
    df = load_data()

    if df.empty:
        raise ValueError("CIMIS dataset is empty")

    # Validate station
    if station not in df["Station Name"].unique():
        raise ValueError(f"Station '{station}' not found.")

    # Validate and convert start date
    parsed_start_date = None
    if start_date:
        try:
            parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("start_date must be in the YYYY-MM-DD format.")

    # Validate and convert end date
    parsed_end_date = None
    if end_date:
        try:
            parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("end_date must be in the YYYY-MM-DD format.")

    # Validate date range
    if parsed_start_date and parsed_end_date:
        if parsed_start_date > parsed_end_date:
            raise ValueError("start_date cannot be after end_date")

    # Filter by station
    filtered_df = df[df["Station Name"] == station]

    # Filter by date
    if parsed_start_date:
        filtered_df = filtered_df[
            filtered_df["Date"] >= parsed_start_date
        ]
    if parsed_end_date:
        filtered_df = filtered_df[
            filtered_df["Date"] <= parsed_end_date
        ]

    return filtered_df
