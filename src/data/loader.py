"""
Data loading and chronological partitioning utilities.
Ensures zero data contamination and provides dataset fingerprinting.
"""

from typing import Tuple, Optional, Dict, Any
from pathlib import Path
import hashlib
import pandas as pd

from src.data.schema import DataSchema, SchemaValidationError


class DataLoader:
    """
    Handles robust loading, schema validation, fingerprinting,
    and chronological train/validation/test splitting.
    """

    def __init__(self, raw_path: Optional[str] = None, schema: Optional[DataSchema] = None):
        if raw_path is None:
            # Default to data/raw/crop_yield_dataset.csv relative to project root
            raw_path = str(Path(__file__).resolve().parents[2] / "data" / "raw" / "crop_yield_dataset.csv")
        self.raw_path = Path(raw_path)
        self.schema = schema or DataSchema()

    def get_dataset_fingerprint(self) -> str:
        """Computes SHA-256 checksum of raw dataset for reproducible experiment tracking."""
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw dataset not found at: {self.raw_path}")
        
        hasher = hashlib.sha256()
        with open(self.raw_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def load_raw(self, validate: bool = True) -> pd.DataFrame:
        """
        Loads the raw CSV dataset into a pandas DataFrame.
        Leaves the raw dataset strictly read-only.
        """
        if not self.raw_path.exists():
            raise FileNotFoundError(f"Raw dataset file not found at: {self.raw_path}")

        # Explicit type casting for safety
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

        df = pd.read_csv(self.raw_path, dtype=dtypes)

        if validate:
            self.schema.validate(df, raise_error=True)

        return df

    def split_chronological(
        self,
        df: Optional[pd.DataFrame] = None,
        train_end_year: int = 2011,
        val_end_year: int = 2014,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Splits data chronologically to mirror real-world forecasting:
        - Train: Year <= train_end_year (Default: 1966–2011)
        - Validation: train_end_year < Year <= val_end_year (Default: 2012–2014)
        - Test: Year > val_end_year (Default: 2015–2017)

        Ensures temporal isolation and no leakage.
        """
        if df is None:
            df = self.load_raw(validate=True)

        train_mask = df["Year"] <= train_end_year
        val_mask = (df["Year"] > train_end_year) & (df["Year"] <= val_end_year)
        test_mask = df["Year"] > val_end_year

        train_df = df[train_mask].copy().reset_index(drop=True)
        val_df = df[val_mask].copy().reset_index(drop=True)
        test_df = df[test_mask].copy().reset_index(drop=True)

        return train_df, val_df, test_df


def load_raw_data(raw_path: Optional[str] = None, validate: bool = True) -> pd.DataFrame:
    """Convenience helper to load raw dataset."""
    loader = DataLoader(raw_path=raw_path)
    return loader.load_raw(validate=validate)


def split_data_chronological(
    df: Optional[pd.DataFrame] = None,
    train_end_year: int = 2011,
    val_end_year: int = 2014,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Convenience helper to chronologically split dataset."""
    loader = DataLoader()
    return loader.split_chronological(
        df=df, train_end_year=train_end_year, val_end_year=val_end_year
    )
