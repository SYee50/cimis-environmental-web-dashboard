"""
Tests data loading, filtering, and summary.
"""

import pandas as pd
import pytest

from backend.services.data_service import calculate_summary, load_data


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


def test_load_data_returns_dataframe(df):
    assert isinstance(df, pd.DataFrame)


def test_load_data_converts_dates_to_datetime(df):
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_calculate_summary(sample_df):
    result = calculate_summary(sample_df)

    assert result["eto"]["total"] == pytest.approx(9.0)
    assert result["eto"]["average_daily"] == pytest.approx(3.0)
    assert result["eto"]["minimum_daily"] == pytest.approx(2.0)
    assert result["eto"]["maximum_daily"] == pytest.approx(4.0)

    assert result["precipitation"]["total"] == pytest.approx(15.0)
    assert result["precipitation"]["maximum_daily"] == pytest.approx(10.0)

    assert result["temperature"]["average"] == pytest.approx(47 / 3)
    assert result["temperature"]["minimum"] == pytest.approx(8.0)
    assert result["temperature"]["maximum"] == pytest.approx(25.0)

    assert result["humidity"]["average"] == pytest.approx(65.0)
    assert result["humidity"]["minimum"] == pytest.approx(40.0)
    assert result["humidity"]["maximum"] == pytest.approx(90.0)

    assert result["solar_radiation"]["average_daily"] == pytest.approx(200.0)
    assert result["solar_radiation"]["minimum_daily"] == pytest.approx(100.0)
    assert result["solar_radiation"]["maximum_daily"] == pytest.approx(300.0)

    assert result["vapor_pressure"]["average"] == pytest.approx(2.0)
    assert result["dew_point"]["average"] == pytest.approx(11.0)
    assert result["wind_speed"]["average"] == pytest.approx(2.0)
