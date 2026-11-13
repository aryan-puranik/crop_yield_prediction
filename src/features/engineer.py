"""
Base interface for agricultural feature engineering.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BaseFeatureEngineer(BaseEstimator, TransformerMixin, ABC):
    """
    Abstract interface for feature engineering transformers.
    Distinguishes pre-season, in-season, and static features to prevent leakage.
    """

    def __init__(self):
        self.feature_names_in_: List[str] = []
        self.engineered_feature_names_: List[str] = []
        self.is_fitted_: bool = False

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "BaseFeatureEngineer":
        """Fits historical parameters (e.g. historical crop means, climate baselines)."""
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms input DataFrame by adding engineered domain features."""
        pass

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        return self.fit(X, y).transform(X)

    def get_feature_names_out(self, input_features: Optional[List[str]] = None) -> List[str]:
        if not self.is_fitted_:
            raise ValueError("Feature engineer has not been fitted yet.")
        return list(input_features or self.feature_names_in_) + self.engineered_feature_names_
