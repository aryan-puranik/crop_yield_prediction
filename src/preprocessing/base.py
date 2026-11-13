"""
Abstract Base Class and interface for preprocessing pipelines.
Complies with scikit-learn TransformerMixin and BaseEstimator.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BasePreprocessor(BaseEstimator, TransformerMixin, ABC):
    """
    Base class for interchangeable preprocessing transformations.
    Ensures that transformations fitted on training data preserve
    feature names and are strictly reused during inference.
    """

    def __init__(self):
        self.feature_names_in_: List[str] = []
        self.feature_names_out_: List[str] = []
        self.is_fitted_: bool = False

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "BasePreprocessor":
        """Fit preprocessor strictly on training data."""
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform features using fitted parameters."""
        pass

    def fit_transform(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> pd.DataFrame:
        """Fit to data, then transform it."""
        return self.fit(X, y).transform(X)

    def get_feature_names_out(self, input_features: Optional[List[str]] = None) -> List[str]:
        """Returns transformed feature names."""
        if not self.is_fitted_:
            raise ValueError("Preprocessor has not been fitted yet.")
        return self.feature_names_out_
