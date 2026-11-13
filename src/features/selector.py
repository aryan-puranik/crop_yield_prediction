"""
Independent Feature Selection Interface.
Adheres strictly to the scikit-learn fit/transform transformer contract.
Prevents target leakage and maintains feature-name mapping across all experiments.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import time
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class BaseFeatureSelector(BaseEstimator, TransformerMixin, ABC):
    """
    Abstract base class for independent, interchangeable feature selectors.
    
    Architectural requirements:
    1. Must implement fit(X, y) and transform(X).
    2. Must track selected feature names, selection runtime, and feature importances/scores.
    3. Must never peek at validation/test targets outside nested CV loops.
    """

    def __init__(self, name: str = "base_selector"):
        self.name = name
        self.feature_names_in_: List[str] = []
        self.selected_features_: List[str] = []
        self.feature_scores_: Dict[str, float] = {}
        self.selection_runtime_sec_: float = 0.0
        self.is_fitted_: bool = False

    @abstractmethod
    def _select(self, X: pd.DataFrame, y: pd.Series) -> List[str]:
        """Internal selection logic returning list of selected feature column names."""
        pass

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "BaseFeatureSelector":
        """
        Fits selector on training data only.
        """
        if y is None:
            raise ValueError(f"{self.name} requires target y for supervised feature selection.")

        if isinstance(X, pd.DataFrame):
            self.feature_names_in_ = list(X.columns)
        else:
            self.feature_names_in_ = [f"feature_{i}" for i in range(X.shape[1])]
            X = pd.DataFrame(X, columns=self.feature_names_in_)

        start_time = time.perf_counter()
        self.selected_features_ = self._select(X, y)
        self.selection_runtime_sec_ = time.perf_counter() - start_time

        self.is_fitted_ = True
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transforms feature matrix by filtering to selected features only."""
        if not self.is_fitted_:
            raise ValueError(f"Feature selector '{self.name}' must be fitted before transforming.")

        if isinstance(X, pd.DataFrame):
            return X[self.selected_features_].copy()
        else:
            df = pd.DataFrame(X, columns=self.feature_names_in_)
            return df[self.selected_features_].to_numpy()

    def get_support(self, indices: bool = False) -> Any:
        """Mask or indices of selected features."""
        if not self.is_fitted_:
            raise ValueError(f"Feature selector '{self.name}' is not fitted.")
        mask = [f in self.selected_features_ for f in self.feature_names_in_]
        if indices:
            return np.where(mask)[0]
        return np.array(mask)

    def get_feature_names_out(self, input_features: Optional[List[str]] = None) -> List[str]:
        """Returns list of selected feature names."""
        if not self.is_fitted_:
            raise ValueError(f"Feature selector '{self.name}' is not fitted.")
        return list(self.selected_features_)

    def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata for experiment tracking and logging."""
        return {
            "selector_name": self.name,
            "n_features_in": len(self.feature_names_in_),
            "n_features_selected": len(self.selected_features_),
            "selected_features": self.selected_features_,
            "selection_runtime_sec": round(self.selection_runtime_sec_, 4),
        }


class NoFeatureSelection(BaseFeatureSelector):
    """
    Baseline selector: retains all features without modification.
    Serves as the benchmark to evaluate whether feature selection actually improves performance.
    """

    def __init__(self):
        super().__init__(name="no_feature_selection")

    def _select(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> List[str]:
        # Keeps 100% of input features
        return list(X.columns)

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> "NoFeatureSelection":
        if isinstance(X, pd.DataFrame):
            self.feature_names_in_ = list(X.columns)
        else:
            self.feature_names_in_ = [f"feature_{i}" for i in range(X.shape[1])]
            X = pd.DataFrame(X, columns=self.feature_names_in_)

        start_time = time.perf_counter()
        self.selected_features_ = self._select(X, y)
        self.selection_runtime_sec_ = time.perf_counter() - start_time
        self.is_fitted_ = True
        return self
