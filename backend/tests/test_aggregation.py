"""
Tests monthly and annual aggregation.
"""

import pandas as pd
import pytest

from backend.services.aggregation_service import aggregate_data
from backend.services.data_service import load_data


@pytest.fixture
def df() -> pd.DataFrame:
    return load_data()


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({
        "Station Number": [1, 1, 1],
        "Station Name": ["Davis", "Davis", "Davis"],
        "CIMIS Region": ["Sacramento Valley"] * 3,
        "Date": pd.to_datetime([
            "2025-01-01",
            "2025-01-02",
            "2025-01-03"
        ]),
        "Jul": [1, 2, 3],
        "ETo (mm)": [2.0, 3.0, 4.0],
        "Precip (mm)": [5.0, 0.0, 10.0],
        "Avg Sol Rad (W/m²)": [100.0, 200.0, 300.0],
        "Avg Vap Pres (kPa)": [1.0, 2.0, 3.0],
        "Max Air Temp (°C)": [20.0, 25.0, 22.0],
        "Min Air Temp (°C)": [10.0, 12.0, 8.0],
        "Avg Air Temp (°C)": [15.0, 18.0, 14.0],
        "Max Rel Hum (%)": [80.0, 90.0, 85.0],
        "Min Rel Hum (%)": [40.0, 50.0, 45.0],
        "Avg Rel Hum (%)": [60.0, 70.0, 65.0],
        "Dew Point (°C)": [10.0, 12.0, 11.0],
        "Avg Wind Speed (m/s)": [1.0, 2.0, 3.0],
    })


def test_daily_aggregation_returns_original_data(df):
    result = aggregate_data(df, "daily")

    pd.testing.assert_frame_equal(result, df)


def test_monthly_aggregation_reduces_to_one_row_per_month(df):
    result = aggregate_data(df, "monthly")
    expected_months = df["Date"].dt.to_period("M").nunique()

    assert len(result) == expected_months


def test_annual_aggregation_reduces_to_one_row_per_year(df):
    result = aggregate_data(df, "annual")
    expected_years = df["Date"].dt.year.nunique()

    assert len(result) == expected_years


def test_station_number_is_preserved(df):
    result = aggregate_data(df, "monthly")
    expected_station_number = df["Station Number"].iloc[0]

    assert result["Station Number"].iloc[0] == expected_station_number


def test_jul_is_removed_from_aggregated_results(df):
    monthly_result = aggregate_data(df, "monthly")
    annual_result = aggregate_data(df, "annual")

    assert "Jul" not in monthly_result.columns
    assert "Jul" not in annual_result.columns


def test_invalid_aggregation_raises_value_error(df):
    with pytest.raises(ValueError):
        aggregate_data(df, "weekly")


def test_sum_aggregation(sample_df):
    monthly_result = aggregate_data(sample_df, "monthly")
    annual_result = aggregate_data(sample_df, "annual")

    for result in [monthly_result, annual_result]:
        assert result["ETo (mm)"].iloc[0] == pytest.approx(9.0)
        assert result["Precip (mm)"].iloc[0] == pytest.approx(15.0)


def test_mean_aggregation(sample_df):
    monthly_result = aggregate_data(sample_df, "monthly")
    annual_result = aggregate_data(sample_df, "annual")

    for result in [monthly_result, annual_result]:
        assert result["Avg Sol Rad (W/m²)"].iloc[0] == pytest.approx(200.0)
        assert result["Avg Vap Pres (kPa)"].iloc[0] == pytest.approx(2.0)
        assert result["Avg Air Temp (°C)"].iloc[0] == pytest.approx(47 / 3)
        assert result["Avg Rel Hum (%)"].iloc[0] == pytest.approx(65.0)
        assert result["Dew Point (°C)"].iloc[0] == pytest.approx(11.0)
        assert result["Avg Wind Speed (m/s)"].iloc[0] == pytest.approx(2.0)


def test_max_aggregation(sample_df):
    monthly_result = aggregate_data(sample_df, "monthly")
    annual_result = aggregate_data(sample_df, "annual")

    for result in [monthly_result, annual_result]:
        assert result["Max Air Temp (°C)"].iloc[0] == pytest.approx(25.0)
        assert result["Max Rel Hum (%)"].iloc[0] == pytest.approx(90.0)


def test_min_aggregation(sample_df):
    monthly_result = aggregate_data(sample_df, "monthly")
    annual_result = aggregate_data(sample_df, "annual")

    for result in [monthly_result, annual_result]:
        assert result["Min Air Temp (°C)"].iloc[0] == pytest.approx(8.0)
        assert result["Min Rel Hum (%)"].iloc[0] == pytest.approx(40.0)
