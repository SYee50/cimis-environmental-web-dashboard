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
