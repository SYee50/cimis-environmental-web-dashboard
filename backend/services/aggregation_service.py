import pandas as pd


def aggregate_data(df: pd.DataFrame, aggregation: str) -> pd.DataFrame:
    """
    Aggregate CIMIS observations by day, month, or year.

    Args:
        df (pandas.DataFrame): CIMIS observations to aggregate.
        aggregation (str): Aggregation level: "daily", "monthly", or "annual".

    Returns:
        pandas.DataFrame: Aggregated CIMIS observations

    Raises:
        ValueError: If the aggregation level is not "daily", "monthly", or "annual".
    """
    if aggregation == "daily":
        return df

    if aggregation not in {"monthly", "annual"}:
        raise ValueError("Aggregation must be 'daily', 'monthly', or 'annual'")

    # Copy DataFrame to prevent modification to original DataFrame passed-in
    df = df.copy()

    # Convert each date to corresponding YYYY-MM or YYYY
    if aggregation == "monthly":
        df["Date"] = df["Date"].dt.to_period("M")
    else:
        df["Date"] = df["Date"].dt.year

    # Define aggregation operation for each measurement
    aggregation_rules = {
        "Station Number": "first",
        "ETo (mm)": "sum",
        "Precip (mm)": "sum",
        "Avg Sol Rad (W/m²)": "mean",
        "Avg Vap Pres (kPa)": "mean",
        "Max Air Temp (°C)": "max",
        "Min Air Temp (°C)": "min",
        "Avg Air Temp (°C)": "mean",
        "Max Rel Hum (%)": "max",
        "Min Rel Hum (%)": "min",
        "Avg Rel Hum (%)": "mean",
        "Dew Point (°C)": "mean",
        "Avg Wind Speed (m/s)": "mean",
    }

    # Remove Jul column that should not be aggregated
    df = df.drop(columns=["Jul"])

    # Group observations by the converted Date
    # Apply the aggregation operation for each column
    aggregated_df = df.groupby("Date").agg(aggregation_rules).reset_index()

    # Convert the grouped Date values to strings for the JSON response
    aggregated_df["Date"] = aggregated_df["Date"].astype(str)

    return aggregated_df


if __name__ == "__main__":
    from backend.services.data_service import load_data

    df = load_data()

    monthly_df = aggregate_data(df, "monthly")

    print(monthly_df.head())