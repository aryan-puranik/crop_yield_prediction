"""
Tests for chronological dataset splitting to prevent data leakage.
"""

import pandas as pd
from src.data.loader import DataLoader


def test_chronological_splits_logic():
    # Synthetic multi-year test DataFrame
    years = [1970, 1990, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
    sample_data = {
        "Year": years,
        "Yield": [100.0 * i for i in range(len(years))],
        "Crop": ["Rice"] * len(years)
    }
    df = pd.DataFrame(sample_data)

    loader = DataLoader()
    train_df, val_df, test_df = loader.split_chronological(
        df=df, train_end_year=2011, val_end_year=2014
    )

    # Verify partition rows
    assert len(train_df) == 3  # 1970, 1990, 2011
    assert len(val_df) == 3    # 2012, 2013, 2014
    assert len(test_df) == 3   # 2015, 2016, 2017

    # Verify boundary years
    assert train_df["Year"].max() <= 2011
    assert val_df["Year"].min() >= 2012
    assert val_df["Year"].max() <= 2014
    assert test_df["Year"].min() >= 2015

    # Verify no overlap
    train_years = set(train_df["Year"])
    val_years = set(val_df["Year"])
    test_years = set(test_df["Year"])
    assert len(train_years.intersection(val_years)) == 0
    assert len(val_years.intersection(test_years)) == 0
    assert len(train_years.intersection(test_years)) == 0
