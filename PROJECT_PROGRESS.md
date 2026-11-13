# Project Progress Tracker: Notebook-First Workflow

| Phase | Phase Name | Primary Research Artifact | Status | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Project Initialization & Data Audit | `notebooks/01_data_audit.ipynb` | **COMPLETED** | Modular architecture, YAML configs, data loader & schema validation, module interfaces, automated tests (12/12 passing), executed 35-cell data audit notebook. |
| **Phase 2** | Exploratory Data Analysis (EDA) | `notebooks/02_exploratory_data_analysis.ipynb` | **COMPLETED** | 20-section executed research notebook (71 cells), target skewness analysis (log1p normalization), crop heterogeneity (sugarcane vs pulses), deterministic crop-season mapping, Green Revolution non-stationarity, climate non-linearities, nutrient collinearity proof, pesticide macro-broadcast verification, 20 figures in `reports/figures/eda/`, 16 tables in `reports/tables/eda/`. |
| **Phase 3** | Outlier Handling Experiments | `notebooks/03_outlier_analysis.ipynb` | **Up Next** | Crop-specific IQR, Z-score, capping strategies restricted to training split; handling Bihar Chickpea reporting anomalies. |
| **Phase 4** | Preprocessing Pipelines | `notebooks/04_preprocessing.ipynb` | Planned | Sklearn ColumnTransformers, encoders, scalers, handling NPK-fertilizer collinearity, log-target transformation. |
| **Phase 5** | Agricultural Feature Engineering | `notebooks/05_feature_engineering.ipynb` | Planned | Nutrient stoichiometry (N:P, N:K), aridity indices, historical district baselines. |
| **Phase 6** | Independent Feature Selection | `notebooks/06_feature_selection.ipynb` | Planned | Mutual Information, LASSO, Tree importance, RFE, baseline comparison. |
| **Phase 7** | Model Training & Hyperparameter Tuning | `notebooks/07_model_training.ipynb` | Planned | Linear models, Random Forest, Extra Trees, Gradient Boosting, XGBoost with chronological cross-validation. |
| **Phase 8** | Final Benchmark Evaluation | `notebooks/08_model_evaluation.ipynb` | Planned | Final 2015–2017 test evaluation, residual diagnostics, crop-disaggregated error tables. |
| **Phase 9** | Scenario Inference & Streamlit App | `notebooks/09_future_yield_prediction.ipynb` & `app/` | Planned | Scenario inference engine, interactive UI, final academic synthesis. |

**Current Branch:** `main`  
**Phase 2 Status:** Verified & Executed from fresh kernel (`notebooks/02_exploratory_data_analysis.ipynb`)  
**Test Suite:** 12 passed in 3.04s
