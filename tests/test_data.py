"""
Tests for data loading, fingerprinting, and chronological split isolation.
"""

import pandas as pd
from src.utils import load_raw_data, split_data_chronological, get_dataset_fingerprint


def test_fingerprint():
    fp = get_dataset_fingerprint()
    assert isinstance(fp, str)
    assert len(fp) == 64


def test_load_raw_data_sample():
    df = load_raw_data()
    assert len(df) == 198369
    assert "Yield" in df.columns
    assert "Crop" in df.columns
    assert "Year" in df.columns


def test_split_data_chronological():
    # Synthetic test DataFrame
    years = [1970, 1990, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    df = pd.DataFrame({
        "Year": years,
        "Crop": ["Wheat"] * len(years),
        "Yield": [1000.0 * i for i in range(len(years))]
    })

    train_df, val_df, test_df = split_data_chronological(df, train_end_year=2011, val_end_year=2014)

    assert len(train_df) == 3
    assert len(val_df) == 3
    assert len(test_df) == 3

    assert train_df["Year"].max() <= 2011
    assert val_df["Year"].min() >= 2012
    assert val_df["Year"].max() <= 2014
    assert test_df["Year"].min() >= 2015

    # Ensure no temporal overlap
    assert len(set(train_df["Year"]).intersection(set(val_df["Year"]))) == 0
    assert len(set(val_df["Year"]).intersection(set(test_df["Year"]))) == 0
