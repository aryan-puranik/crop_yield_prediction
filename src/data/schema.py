"""
Schema definitions and validation utilities for agricultural crop yield data.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
import pandas as pd


class SchemaValidationError(Exception):
    """Raised when dataset fails schema or data contract validation."""
    pass


class DataSchema:
    """
    Manages expected column definitions, data types, physical bounds,
    and categorical integrity checks for the crop yield dataset.
    """

    def __init__(self, config_path: Optional[str] = None):
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        else:
            # Fallback to standard project defaults
            default_path = Path(__file__).resolve().parents[2] / "config" / "schema_config.yaml"
            if default_path.exists():
                with open(default_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
            else:
                self.config = self._fallback_config()

        self.expected_columns: List[str] = self.config.get("expected_columns", [])
        self.target_column: str = self.config.get("target_column", "Yield")
        self.time_column: str = self.config.get("time_column", "Year")
        self.categorical_features: List[str] = self.config.get("categorical_features", [])
        self.numerical_features: List[str] = self.config.get("numerical_features", [])
        self.bounds: Dict[str, Dict[str, float]] = self.config.get("bounds", {})
        self.allowed_categories: Dict[str, List[str]] = self.config.get("allowed_categories", {})

    def validate(self, df: pd.DataFrame, raise_error: bool = True) -> Dict[str, Any]:
        """
        Validates dataframe against schema contract:
        1. Checks for missing required columns.
        2. Validates numerical bounds (e.g. non-negative rainfall, valid pH).
        3. Validates category domains.

        Returns a dictionary with validation status and details.
        """
        issues: List[str] = []

        # 1. Missing columns
        missing_cols = [c for c in self.expected_columns if c not in df.columns]
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")

        # 2. Null values check
        null_counts = df.isnull().sum()
        cols_with_nulls = null_counts[null_counts > 0].to_dict()
        if cols_with_nulls:
            issues.append(f"Null values detected in columns: {cols_with_nulls}")

        # 3. Numerical bounds
        for col, b in self.bounds.items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                min_val = b.get("min")
                max_val = b.get("max")
                if min_val is not None:
                    viol_min = (df[col] < min_val).sum()
                    if viol_min > 0:
                        issues.append(
                            f"Column '{col}' has {viol_min} rows below minimum valid bound ({min_val})."
                        )
                if max_val is not None:
                    viol_max = (df[col] > max_val).sum()
                    if viol_max > 0:
                        issues.append(
                            f"Column '{col}' has {viol_max} rows above maximum valid bound ({max_val})."
                        )

        # 4. Categorical domains
        for cat_col, allowed in self.allowed_categories.items():
            if cat_col in df.columns:
                invalid_cats = set(df[cat_col].dropna().unique()) - set(allowed)
                if invalid_cats:
                    issues.append(
                        f"Column '{cat_col}' contains unpermitted categories: {invalid_cats}"
                    )

        report = {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
        }

        if not report["is_valid"] and raise_error:
            raise SchemaValidationError("; ".join(issues))

        return report

    @staticmethod
    def _fallback_config() -> Dict[str, Any]:
        return {
            "expected_columns": [
                "Year", "Region", "Crop", "Season", "Temperature", "Rainfall",
                "Humidity", "Soil Type", "pH", "Nitrogen", "Phosphorus",
                "Potassium", "Fertilizer", "Pesticide", "Yield"
            ],
            "target_column": "Yield",
            "time_column": "Year",
            "categorical_features": ["Region", "Crop", "Season", "Soil Type"],
            "numerical_features": [
                "Temperature", "Rainfall", "Humidity", "pH", "Nitrogen",
                "Phosphorus", "Potassium", "Fertilizer", "Pesticide"
            ],
            "bounds": {
                "Rainfall": {"min": 0.0},
                "Humidity": {"min": 0.0, "max": 100.0},
                "pH": {"min": 3.0, "max": 11.0},
                "Yield": {"min": 0.0}
            },
            "allowed_categories": {
                "Season": ["Kharif", "Rabi", "Whole Year"]
            }
        }
