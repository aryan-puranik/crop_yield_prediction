"""
Data loading and utility functions for Crop Yield Prediction project.
Simple, beginner-friendly helper functions.
"""

from pathlib import Path
import hashlib
from typing import Tuple, Optional
import pandas as pd


def get_dataset_fingerprint(filepath: Optional[str] = None) -> str:
    """Calculates SHA-256 checksum of raw dataset for reproducibility."""
    if filepath is None:
        filepath = str(Path(__file__).resolve().parents[1] / "data" / "raw" / "crop_yield_dataset.csv")
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")

    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_raw_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads the historical crop yield dataset from CSV.
    Preserves raw data immutability.
    """
    if filepath is None:
        filepath = str(Path(__file__).resolve().parents[1] / "data" / "raw" / "crop_yield_dataset.csv")
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found at {path}")

    dtypes = {
        "Year": "int64",
        "Region": "string",
        "Crop": "string",
        "Season": "string",
        "Temperature": "float64",
        "Rainfall": "float64",
        "Humidity": "float64",
        "Soil Type": "string",
        "pH": "float64",
        "Nitrogen": "float64",
        "Phosphorus": "float64",
        "Potassium": "float64",
        "Fertilizer": "float64",
        "Pesticide": "float64",
        "Yield": "float64",
    }
    return pd.read_csv(path, dtype=dtypes)


def split_data_chronological(
    df: pd.DataFrame,
    train_end_year: int = 2011,
    val_end_year: int = 2014
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits data chronologically to prevent temporal data leakage:
    - Train: Year <= train_end_year (1966-2011)
    - Validation: train_end_year < Year <= val_end_year (2012-2014)
    - Test: Year > val_end_year (2015-2017)
    """
    train_df = df[df["Year"] <= train_end_year].copy().reset_index(drop=True)
    val_df = df[(df["Year"] > train_end_year) & (df["Year"] <= val_end_year)].copy().reset_index(drop=True)
    test_df = df[df["Year"] > val_end_year].copy().reset_index(drop=True)

    return train_df, val_df, test_df
