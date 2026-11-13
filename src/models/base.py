"""
Base model wrapper interface for interchangeable ML estimators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time
import numpy as np
import pandas as pd


class BaseModelWrapper(ABC):
    """
    Uniform wrapper around regression algorithms.
    Decouples model definition from training loops and tracks fit/predict runtimes.
    """

    def __init__(self, model_name: str, params: Optional[Dict[str, Any]] = None):
        self.model_name = model_name
        self.params = params or {}
        self.model: Any = None
        self.fit_time_sec: float = 0.0
        self.predict_time_sec: float = 0.0
        self.is_fitted: bool = False

    @abstractmethod
    def build_model(self) -> Any:
        """Instantiates the underlying ML estimator."""
        pass

    def fit(self, X: pd.DataFrame, y: pd.Series) -> "BaseModelWrapper":
        """Fits model and records training duration."""
        if self.model is None:
            self.model = self.build_model()

        start_time = time.perf_counter()
        self.model.fit(X, y)
        self.fit_time_sec = time.perf_counter() - start_time
        self.is_fitted = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Generates predictions and records inference duration."""
        if not self.is_fitted or self.model is None:
            raise ValueError(f"Model '{self.model_name}' has not been fitted.")

        start_time = time.perf_counter()
        preds = self.model.predict(X)
        self.predict_time_sec = time.perf_counter() - start_time
        return preds

    def get_metadata(self) -> Dict[str, Any]:
        """Returns execution and configuration metadata."""
        return {
            "model_name": self.model_name,
            "params": self.params,
            "fit_time_sec": round(self.fit_time_sec, 4),
            "predict_time_sec": round(self.predict_time_sec, 4),
            "is_fitted": self.is_fitted,
        }
