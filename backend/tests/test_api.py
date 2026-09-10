"""
Tests the HTTP/API behavior.
"""

from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "CIMIS Dashboard API"}


def test_get_stations():
    response = client.get("/stations")
    data = response.json()

    assert response.status_code == 200
    assert "stations" in data
    assert len(data["stations"]) > 0


def test_get_stations_returns_expected_stations():
    response = client.get("/stations")
    stations = response.json()["stations"]
    expected_stations = {
        "FivePoints",
        "Davis",
        "Bishop",
        "Calipatria/Mulberry",
        "San Luis Obispo"
    }

    assert set(stations) == expected_stations


def test_data_request_returns_correct_station():
    response = client.get(
        "/data",
        params={
            "station": "Davis"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0
    assert all(row["Station Name"] == "Davis" for row in data)


def test_invalid_station():
    response = client.get(
        "/data",
        params={
            "station": "NotARealStation"
        }
    )

    assert response.status_code == 404


def test_invalid_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "aggregation": "weekly"
        }
    )

    assert response.status_code == 400


def test_invalid_start_date():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "not-a-date"
        }
    )

    assert response.status_code == 400


def test_start_date_after_end_date():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "2025-12-31",
            "end_date": "2025-01-01"
        }
    )

    assert response.status_code == 400


def test_date_filtering():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "2025-01-01",
            "end_date": "2025-01-31"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0
    assert all(row["Date"].startswith("2025-01-") for row in data)


def test_monthly_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "aggregation": "monthly"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

    dates = [row["Date"] for row in data]

    assert all(len(date) == 7 for date in dates)
    assert all(date[4] == "-" for date in dates)
    assert len(dates) == len(set(dates))


def test_annual_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "aggregation": "annual"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0

    dates = [row["Date"] for row in data]

    assert all(len(date) == 4 for date in dates)
    assert len(dates) == len(set(dates))


def test_empty_date_range_returns_empty_list():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "1900-01-01",
            "end_date": "1900-01-31"
        }
    )

    assert response.status_code == 200
    assert response.json() == []


def test_data_request_with_date_range_and_monthly_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "2025-01-01",
            "end_date": "2025-03-31",
            "aggregation": "monthly"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3

    dates = [row["Date"] for row in data]

    assert dates == ["2025-01", "2025-02", "2025-03"]


def test_data_request_with_date_range_and_annual_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "2024-01-01",
            "end_date": "2025-12-31",
            "aggregation": "annual"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2

    dates = [row["Date"] for row in data]

    assert dates == ["2024", "2025"]


def test_data_request_with_date_range_and_daily_aggregation():
    response = client.get(
        "/data",
        params={
            "station": "Davis",
            "start_date": "2025-01-01",
            "end_date": "2025-01-05",
            "aggregation": "daily"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 5

    assert all(row["Station Name"] == "Davis" for row in data)

    dates = [row["Date"] for row in data]

    assert dates == [
        "2025-01-01T00:00:00",
        "2025-01-02T00:00:00",
        "2025-01-03T00:00:00",
        "2025-01-04T00:00:00",
        "2025-01-05T00:00:00"
    ]