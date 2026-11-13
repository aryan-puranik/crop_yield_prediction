"""
Tests for DataSchema validation constraints and error handling.
"""

import pytest
import pandas as pd
from src.data.schema import DataSchema, SchemaValidationError


@pytest.fixture
def valid_sample_df():
    """Provides a valid minimal agricultural DataFrame."""
    return pd.DataFrame({
        "Year": [2010, 2011],
        "Region": ["Anantapur, AndhraPradesh", "Guntur, AndhraPradesh"],
        "Crop": ["Rice", "Wheat"],
        "Season": ["Kharif", "Rabi"],
        "Temperature": [26.5, 22.0],
        "Rainfall": [850.0, 320.0],
        "Humidity": [65.0, 45.0],
        "Soil Type": ["Alfisols", "Vertisols"],
        "pH": [6.5, 7.2],
        "Nitrogen": [45.0, 60.0],
        "Phosphorus": [15.0, 20.0],
        "Potassium": [10.0, 12.0],
        "Fertilizer": [70.0, 92.0],
        "Pesticide": [0.44, 0.44],
        "Yield": [1500.0, 2200.0],
    })


def test_schema_valid_data(valid_sample_df):
    schema = DataSchema()
    report = schema.validate(valid_sample_df, raise_error=True)
    assert report["is_valid"] is True
    assert len(report["issues"]) == 0


def test_schema_missing_column(valid_sample_df):
    schema = DataSchema()
    invalid_df = valid_sample_df.drop(columns=["Yield"])
    with pytest.raises(SchemaValidationError) as exc_info:
        schema.validate(invalid_df, raise_error=True)
    assert "Missing required columns" in str(exc_info.value)


def test_schema_invalid_rainfall_bound(valid_sample_df):
    schema = DataSchema()
    invalid_df = valid_sample_df.copy()
    invalid_df.loc[0, "Rainfall"] = -50.0  # Physically impossible negative rainfall
    with pytest.raises(SchemaValidationError) as exc_info:
        schema.validate(invalid_df, raise_error=True)
    assert "below minimum valid bound" in str(exc_info.value)


def test_schema_invalid_ph_bound(valid_sample_df):
    schema = DataSchema()
    invalid_df = valid_sample_df.copy()
    invalid_df.loc[0, "pH"] = 14.5  # Extreme unviable pH
    with pytest.raises(SchemaValidationError) as exc_info:
        schema.validate(invalid_df, raise_error=True)
    assert "above maximum valid bound" in str(exc_info.value)


def test_schema_invalid_season_category(valid_sample_df):
    schema = DataSchema()
    invalid_df = valid_sample_df.copy()
    invalid_df.loc[0, "Season"] = "Monsoon_Spring"  # Unpermitted season
    with pytest.raises(SchemaValidationError) as exc_info:
        schema.validate(invalid_df, raise_error=True)
    assert "unpermitted categories" in str(exc_info.value)
