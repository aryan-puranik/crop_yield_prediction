"""
Tests for independent module interfaces (feature selection and metrics).
"""

import numpy as np
import pandas as pd
from src.features.selector import NoFeatureSelection
from src.evaluation.metrics import calculate_regression_metrics, calculate_crop_wise_metrics


def test_no_feature_selection_interface():
    X = pd.DataFrame({
        "Temperature": [25.0, 30.0, 22.0],
        "Rainfall": [500.0, 700.0, 450.0],
        "pH": [6.5, 7.0, 6.8]
    })
    y = pd.Series([1200.0, 1500.0, 1100.0])

    selector = NoFeatureSelection()
    selector.fit(X, y)

    assert selector.is_fitted_ is True
    assert selector.get_feature_names_out() == ["Temperature", "Rainfall", "pH"]
    assert np.all(selector.get_support())

    X_trans = selector.transform(X)
    assert X_trans.shape == X.shape
    pd.testing.assert_frame_equal(X_trans, X)


def test_regression_metrics_known_values():
    y_true = np.array([100.0, 200.0, 300.0])
    y_pred = np.array([110.0, 190.0, 310.0])  # errors: +10, -10, +10

    metrics = calculate_regression_metrics(y_true, y_pred)
    assert metrics["mae"] == 10.0
    assert metrics["rmse"] == 10.0
    assert metrics["mse"] == 100.0
    assert metrics["r2"] > 0.95


def test_crop_wise_metrics():
    df = pd.DataFrame({
        "Crop": ["Rice", "Rice", "Wheat", "Wheat"],
        "Yield": [1000.0, 1200.0, 2000.0, 2200.0],
        "pred_yield": [1050.0, 1180.0, 1950.0, 2220.0]
    })
    res = calculate_crop_wise_metrics(df, crop_col="Crop", y_true_col="Yield", y_pred_col="pred_yield")
    assert len(res) == 2
    assert set(res["Crop"]) == {"Rice", "Wheat"}
    assert "mae" in res.columns
    assert "rmse" in res.columns
    assert "r2" in res.columns
