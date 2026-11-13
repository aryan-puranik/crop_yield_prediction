# Methodological Risks and Leakage Prevention

**Project Title:** Crop Yield Prediction and Forecasting Using Agricultural Data and Machine Learning  
**Date:** November 2026  

---

## 1. Overview of Methodological Risks

Agricultural data science projects frequently suffer from methodological flaws that inflate retrospective evaluation metrics while causing severe degradation in real-world deployment. This document formalizes the primary failure modes and the architectural safeguards enacted in this project.

---

## 2. Identified Risks & Architectural Countermeasures

### 2.1 Temporal Data Leakage
- **The Risk:** In standard random cross-validation ($k$-fold), training observations include future years, allowing models to learn temporal macro-trends (e.g. Green Revolution fertilizer adoption, climatic shifts) and apply them backwards in time. Furthermore, fitting encoders, scalers, or imputers across the entire dataset exposes future distributions to the model.
- **Countermeasure:**
  - Strict chronological holdout: Training ($1966\text{–}2011$), Validation ($2012\text{–}2014$), Test ($2015\text{–}2017$).
  - Preprocessing and feature transformers are fitted strictly on training data and stored in scikit-learn Pipelines.
  - Future years are never observed during feature selection or hyperparameter tuning.

### 2.2 Feature Selection Target Leakage
- **The Risk:** Applying supervised feature selection (e.g. mutual information, LASSO, recursive feature elimination) on the whole dataset prior to cross-validation introduces optimistic bias into validation scores.
- **Countermeasure:**
  - All feature selectors implement the scikit-learn `fit`/`transform` contract.
  - Supervised selectors are fitted inside nested training loops only.
  - A permanent `NoFeatureSelection` baseline is maintained to rigorously verify whether feature selection yields actual performance gains.

### 2.3 Target-Dependent Filtering on Evaluation Sets
- **The Risk:** Removing outliers from test or validation sets artificially improves reported performance by discarding difficult-to-predict real-world agricultural events (droughts, pest outbreaks, record harvests).
- **Countermeasure:**
  - Test and validation observations must never be pruned, altered, or imputed based on target ($Yield$) values.
  - Target-based filtering, if scientifically justified during training, is strictly confined to the training partition.

### 2.4 Scenario Prediction vs. Advance Forecasting
- **The Risk:** Many published agricultural ML papers claim "crop yield forecasting" while utilizing actual observed full-season rainfall, temperature, and fertilizer consumption. In real operational settings, future rainfall during the growing season is not known prior to planting.
- **Countermeasure:**
  - Predictions conditioned on contemporaneous weather and management variables are explicitly designated as **scenario-based yield estimations** (i.e. "What would the yield be under these specified weather and management conditions?").
  - True advance pre-season forecasts must rely strictly on pre-season indices, historical district averages, or climate forecasts.

### 2.5 Spatial and Crop Generalization Limits
- **The Risk:** Evaluating models primarily on aggregated $R^2$ hides catastrophic failures on low-volume crops or peripheral geographic zones.
- **Countermeasure:**
  - Mandatory crop-wise error breakdowns (MAE, RMSE, $R^2$ per crop).
  - Residual analysis across time and geographic states.
  - Model comparison based primarily on RMSE and MAE rather than overall $R^2$.
