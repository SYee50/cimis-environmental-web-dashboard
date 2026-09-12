import pytest

from backend.services.data_service import compare_stations


def test_compare_two_stations():
    result = compare_stations(
        ["Davis", "Bishop"]
    )

    assert "Davis" in result
    assert "Bishop" in result

    assert len(result["Davis"]) > 0
    assert len(result["Bishop"]) > 0


def test_compare_multiple_stations():
    result = compare_stations(
        ["Davis", "Bishop", "FivePoints"]
    )

    assert len(result) == 3

    assert "Davis" in result
    assert "Bishop" in result
    assert "FivePoints" in result


def test_compare_stations_with_date_range():
    result = compare_stations(
        ["Davis", "Bishop"],
        start_date="2024-01-01",
        end_date="2024-01-31"
    )

    assert len(result["Davis"]) > 0
    assert len(result["Bishop"]) > 0

    for station_data in result.values():
        for record in station_data:
            assert "2024-01" in record["Date"]


def test_compare_stations_monthly_aggregation():
    result = compare_stations(
        ["Davis", "Bishop"],
        aggregation="monthly"
    )

    assert len(result["Davis"]) > 0
    assert len(result["Bishop"]) > 0

    for station_data in result.values():
        for record in station_data:
            assert len(record["Date"]) == 7


def test_compare_stations_annual_aggregation():
    result = compare_stations(
        ["Davis", "Bishop"],
        aggregation="annual"
    )

    assert len(result["Davis"]) > 0
    assert len(result["Bishop"]) > 0

    for station_data in result.values():
        for record in station_data:
            assert len(record["Date"]) == 4


def test_compare_stations_invalid_station():
    with pytest.raises(ValueError, match="not found"):
        compare_stations(
            ["Davis", "NotAStation"]
        )


def test_compare_stations_no_stations():
    with pytest.raises(
        ValueError,
        match="At least one station is required"
    ):
        compare_stations([])


def test_compare_stations_invalid_date_range():
    with pytest.raises(
        ValueError,
        match="start_date cannot be after end_date"
    ):
        compare_stations(
            ["Davis", "Bishop"],
            start_date="2024-12-01",
            end_date="2024-01-01"
        )


def test_compare_stations_invalid_aggregation():
    with pytest.raises(
        ValueError,
        match="Aggregation must be"
    ):
        compare_stations(
            ["Davis", "Bishop"],
            aggregation="weekly"
        )
