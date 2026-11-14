"""
Evaluation metrics calculation for crop yield regression models.
Computes standard academic metrics and crop-wise performance breakdowns.
"""

from typing import Dict, Union
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_regression_metrics(
    y_true: Union[np.ndarray, pd.Series],
    y_pred: Union[np.ndarray, pd.Series]
) -> Dict[str, float]:
    """
    Computes standard regression metrics:
    - MAE: Mean Absolute Error (kg/ha)
    - RMSE: Root Mean Squared Error (kg/ha)
    - MSE: Mean Squared Error ((kg/ha)^2)
    - R2: Coefficient of Determination
    """
    y_t = np.asarray(y_true).ravel()
    y_p = np.asarray(y_pred).ravel()

    if len(y_t) != len(y_p):
        raise ValueError(f"Length mismatch: y_true ({len(y_t)}) vs y_pred ({len(y_p)})")

    mae = float(mean_absolute_error(y_t, y_p))
    mse = float(mean_squared_error(y_t, y_p))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_t, y_p))

    return {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "mse": round(mse, 2),
        "r2": round(r2, 4),
    }


def calculate_crop_wise_metrics(
    df: pd.DataFrame,
    crop_col: str = "Crop",
    y_true_col: str = "Yield",
    y_pred_col: str = "pred_yield"
) -> pd.DataFrame:
    """
    Calculates regression metrics per crop.
    Essential in agriculture because crop yield baselines differ by an order of magnitude.
    """
    records = []
    for crop, group in df.groupby(crop_col):
        metrics = calculate_regression_metrics(group[y_true_col], group[y_pred_col])
        metrics["Crop"] = crop
        metrics["n_samples"] = len(group)
        metrics["mean_true_yield"] = round(float(group[y_true_col].mean()), 2)
        records.append(metrics)

    res_df = pd.DataFrame(records)
    cols = ["Crop", "n_samples", "mean_true_yield", "mae", "rmse", "r2"]
    return res_df[cols].sort_values("rmse", ascending=False).reset_index(drop=True)
