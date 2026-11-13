# Project Implementation Roadmap: Notebook-First Research Workflow

**Project Title:** Crop Yield Prediction and Forecasting Using Agricultural Data and Machine Learning  
**Target:** Crop Yield in kg/ha  
**Research Paradigm:** Academic Jupyter Notebooks backed by modular Python packages (`src/`).

---

## Multi-Phase Execution Plan

### Phase 1: Project Initialization & Notebook Data Audit (Completed)
- **Primary Notebook:** `notebooks/01_data_audit.ipynb`
- [x] Inspect raw CSV schema, provenance, and data characteristics.
- [x] Verify data types, missing values, logical keys, and bounds.
- [x] Establish modular directory structure (`config/`, `data/`, `src/`, `notebooks/`, `tests/`, `reports/`, `experiments/`).
- [x] Configure pinned, verified dependencies (`pyproject.toml`, `requirements.txt`).
- [x] Implement YAML configuration scaffolding (`default_config.yaml`, `schema_config.yaml`, `data_split_config.yaml`).
- [x] Define abstract base classes and interfaces for data loader, preprocessors, feature selectors, models, and evaluation in `src/`.
- [x] Build automated test suite covering schema validation, file reading, chronological splitting, and interfaces (12 passing tests).
- [x] Consolidate data audit into fully executed, publication-grade notebook `notebooks/01_data_audit.ipynb`.
- [x] Retire redundant standalone data-audit scripts and Markdown reports.

---

### Phase 2: Exploratory Data Analysis (EDA)
- **Primary Notebook:** `notebooks/02_exploratory_data_analysis.ipynb`
- [ ] Univariate distributions of Yield and agricultural inputs (skewness, log distributions).
- [ ] Bivariate relationships: climate (temperature, rainfall, humidity) vs. yield.
- [ ] Soil taxonomy and pH impact across crop families.
- [ ] Crop-specific and season-specific yield profiles.
- [ ] Temporal trends (1966–2017) reflecting technology and Green Revolution adoption.
- [ ] State-wise geographic distribution and harvest intensity.
- [ ] Publication-quality inline visualizations with academic interpretations.

---

### Phase 3: Outlier Handling & Robustness Analysis
- **Primary Notebook:** `notebooks/03_outlier_analysis.ipynb`
- [ ] Investigate recording anomalies (e.g. chickpea extreme maximum yield).
- [ ] Implement configurable outlier handling strategies on training data:
  - Baseline: No outlier removal.
  - IQR-based detection.
  - Z-score / Modified Z-score.
  - Percentile capping (winsorization).
  - Crop-specific dynamic thresholds (mandatory for sugarcane vs. pulses).
- [ ] Strictly ensure test and validation partitions remain unfiltered.

---

### Phase 4: Preprocessing & Categorical Encoding Pipelines
- **Primary Notebook:** `notebooks/04_preprocessing.ipynb`
- [ ] Build reusable `ColumnTransformer` pipelines:
  - Categorical encoders: One-Hot Encoding with handling of unseen categories, Target Encoding (out-of-fold), or Ordinal Encoding where appropriate.
  - Numerical scalers: StandardScaler, RobustScaler, MinMaxScaler.
- [ ] Address strict collinearity of `Fertilizer` with `N`, `P`, and `K`.
- [ ] Log / Power transformations for skewed features where statistically indicated.
- [ ] Save fitted transformers for inference.

---

### Phase 5: Agricultural Feature Engineering
- **Primary Notebook:** `notebooks/05_feature_engineering.ipynb`
- [ ] Nutrient stoichiometry: N:P, N:K, P:K ratios (with zero-division protection).
- [ ] Agro-climatic interaction terms: Aridity index proxies, rainfall-to-temperature ratios.
- [ ] Historical temporal indicators: District rolling averages, crop historical productivity baselines.
- [ ] Distinguish pre-season available features from contemporaneous scenario inputs.
- [ ] Strict temporal leakage prevention during lag and rolling calculations.

---

### Phase 6: Independent Feature Selection Experiments
- **Primary Notebook:** `notebooks/06_feature_selection.ipynb`
- [ ] Implement interchangeable feature selectors inheriting from `BaseFeatureSelector`:
  - `NoFeatureSelection` (Benchmark baseline).
  - Correlation-based collinearity filter.
  - Mutual Information regression selector.
  - LASSO (L1-regularized linear model) selector.
  - Tree-based feature importance selector (Random Forest / Extra Trees).
  - Recursive Feature Elimination (RFE).
- [ ] Run matrix of experiments (e.g. Standard Scaler + MI, Robust Scaler + LASSO) without altering training code.
- [ ] Track selected features, selection runtime, and feature stability.

---

### Phase 7: Machine Learning Model Training & Optimization
- **Primary Notebook:** `notebooks/07_model_training.ipynb`
- [ ] Model candidates:
  - Baselines: Linear Regression, Ridge, Lasso, ElasticNet.
  - Non-linear trees: Decision Tree, Random Forest, Extra Trees, Gradient Boosting, XGBoost.
- [ ] Chronological cross-validation (rolling / expanding window on 1966–2011).
- [ ] Hyperparameter tuning using Optuna or RandomizedSearchCV on validation partition.
- [ ] Experiment registry tracking hyperparameter configs, runtimes, and validation scores.

---

### Phase 8: Final Benchmark Evaluation
- **Primary Notebook:** `notebooks/08_model_evaluation.ipynb`
- [ ] Evaluate best-performing models on the held-out Test Set (2015–2017).
- [ ] Comprehensive evaluation: MAE, RMSE, $R^2$, crop-wise error tables, residual diagnostics.
- [ ] Model comparison leaderboards and error visualizations.

---

### Phase 9: Scenario Inference Engine & Streamlit Application
- **Primary Notebook:** `notebooks/09_future_yield_prediction.ipynb` & `app/`
- [ ] Build end-to-end inference pipeline supporting user-defined agricultural scenarios.
- [ ] Input validation for scenario bounds and uncertainty caveats.
- [ ] Multi-tab Streamlit dashboard:
  - Overview & dataset provenance.
  - Interactive EDA visuals.
  - Experiment comparison leaderboard.
  - Scenario-based crop yield predictor with input validation and scientific disclosures.
