import pandas as pd


def aggregate_data(df: pd.DataFrame, aggregation: str) -> pd.DataFrame:
    """
    Aggregate CIMIS observations by day, month, or year.

    Args:
        df (pandas.DataFrame): CIMIS observations to aggregate.
        aggregation (str): Aggregation level: "daily", "monthly", or "annual".

    Returns:
        pandas.DataFrame: Aggregated CIMIS observations.
    """
    if aggregation == "daily":
        return df

    if aggregation == "monthly":
        df = df.copy()
        df["Date"] = df["Date"].dt.to_period("M")

        station_number = df["Station Number"].iloc[0]

        df = df.drop(columns=["Station Number", "Jul"])

        monthly_df = df.groupby("Date").mean(numeric_only=True).reset_index()

        monthly_df.insert(1, "Station Number", station_number)
        monthly_df["Date"] = monthly_df["Date"].astype(str)

        return monthly_df

    if aggregation == "annual":
        df = df.copy()
        df["Date"] = df["Date"].dt.year

        station_number = df["Station Number"].iloc[0]

        df = df.drop(columns=["Station Number", "Jul"])

        annual_df = df.groupby("Date").mean(numeric_only=True).reset_index()

        annual_df.insert(1, "Station Number", station_number)
        annual_df["Date"] = annual_df["Date"].astype(str)

        return annual_df

    raise ValueError("Aggregation must ve 'daily', 'monthly', or 'annual'")


if __name__ == "__main__":
    from backend.services.data_service import load_data

    df = load_data()

    monthly_df = aggregate_data(df, "monthly")

    print(monthly_df.head())