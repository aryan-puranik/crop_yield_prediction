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

### Phase 2: Comprehensive Exploratory Data Analysis (Completed)
- **Primary Notebook:** `notebooks/02_exploratory_data_analysis.ipynb`
- [x] Target distribution analysis: Skewness (+3.74), kurtosis (26.38), and log1p normalization (-0.10 skewness).
- [x] Crop-wise yield disaggregation across all 21 crops: Sugarcane scale disparity (median 5,200 kg/ha vs Cotton 212.50 kg/ha).
- [x] Seasonal confounding analysis: Discovered exact 1-to-1 deterministic mapping between Crop and Season.
- [x] Temporal productivity trends (1966–2017): Non-stationary Green Revolution trajectories in Wheat and Rice (>300% yield growth).
- [x] Geographic variation across 20 states and 309 districts: Spatial sampling distribution and irrigation disparity.
- [x] Non-linear agro-climatic response curves: Thermal optima and crop-specific precipitation thresholds.
- [x] Edaphic constraints: Soil taxonomy and narrow pH distributions (std 0.12–0.35 within Soil Orders).
- [x] Nutrient collinearity proof: Mathematical identity $\text{Fertilizer} \equiv N + P + K$ across 100.00% of rows ($|\Delta| < 0.21$).
- [x] Pesticide macro-investigation: Zero within-year variance; confirmed national FAOSTAT step-function assignment.
- [x] Correlation & collinearity matrices: Isolated severe predictor pairs ($|r| \ge 0.70$) and explained low pooled linear climate correlations.
- [x] Outlier exploration: Contextualized Chickpea reporting anomalies in Bihar 2007 (58,363.64 and 32,000 kg/ha) vs valid Sugarcane extremes.
- [x] Feature Availability Contract: Pre-season known vs in-season contemporaneous vs management scenario variables.
- [x] Evidence-based findings matrix (10 core findings) and actionable recommendations for Phases 3 through 9.
- [x] Exported 20 publication-grade figures (`reports/figures/eda/`) and 16 summary tables (`reports/tables/eda/`).

---

### Phase 3: Outlier Handling & Robustness Analysis (Up Next)
- **Primary Notebook:** `notebooks/03_outlier_analysis.ipynb`
- [ ] Implement configurable crop-stratified outlier handling strategies on training data:
  - Baseline: No outlier removal.
  - Crop-specific IQR trimming ($Q3 + 1.5 \times IQR$ and $Q3 + 3.0 \times IQR$).
  - Crop-specific Z-score / Modified Z-score.
  - Percentile capping (winsorization at 1st and 99th percentiles).
- [ ] Address identified data-entry reporting errors in training split (e.g. Bihar Chickpea records).
- [ ] Strictly ensure validation and test partitions remain untouched and unclipped.

---

### Phase 4: Preprocessing & Categorical Encoding Pipelines
- **Primary Notebook:** `notebooks/04_preprocessing.ipynb`
- [ ] Build reusable `ColumnTransformer` pipelines:
  - Categorical encoders: OneHotEncoder (handling unseen categories) for `Region`, `Crop`, `Soil Type`.
  - Address `Season` redundancy (since `Crop` deterministically encodes `Season`).
  - Numerical scalers: StandardScaler, RobustScaler, MinMaxScaler.
- [ ] Log-target transformation (`TransformedTargetRegressor` with `np.log1p`).
- [ ] Handle `Fertilizer` collinearity with $N, P, K$.
- [ ] Save fitted transformers for inference.

---

### Phase 5: Agricultural Feature Engineering
- **Primary Notebook:** `notebooks/05_feature_engineering.ipynb`
- [ ] Nutrient stoichiometry: $N:P$, $N:K$, and $P:K$ ratios (with zero-division protection $\epsilon$).
- [ ] Agro-climatic interaction terms: Aridity index proxies ($\text{Rainfall} / (\text{Temperature} + 10)$).
- [ ] Historical temporal indicators: Expanding-window district-crop historical mean yields (strictly computed on past years).
- [ ] Distinguish pre-season available features from contemporaneous scenario inputs.

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
- [ ] Run matrix of experiments without altering training code.
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
