"""
Tests for DataLoader functionality, file reading, and fingerprinting.
"""

import pytest
from pathlib import Path
import pandas as pd

from src.data.loader import DataLoader


def test_dataset_fingerprint():
    loader = DataLoader()
    fingerprint = loader.get_dataset_fingerprint()
    assert isinstance(fingerprint, str)
    assert len(fingerprint) == 64  # SHA-256 length


def test_data_loader_raw_sample():
    loader = DataLoader()
    # Read first 100 rows directly to test read behavior and types
    df = pd.read_csv(loader.raw_path, nrows=100)
    assert len(df) == 100
    assert "Yield" in df.columns
    assert "Year" in df.columns
    assert "Crop" in df.columns


def test_file_not_found():
    loader = DataLoader(raw_path="non_existent_file.csv")
    with pytest.raises(FileNotFoundError):
        loader.load_raw()
