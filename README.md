# Crop Yield Prediction and Forecasting Using Agricultural Data and Machine Learning

A research-oriented, reproducible, and modular machine learning framework for predicting and forecasting crop yields across Indian agricultural districts using historical multi-source data (1966–2017).

---

## 1. Project Overview & Research Paradigm

Accurate crop yield prediction is vital for national food security planning, agro-economic risk management, supply-chain resilience, and agricultural policy formulation. 

This project follows an academic, **notebook-first research workflow**:
- **Research Execution via Notebooks:** All exploratory data analysis, outlier investigations, feature engineering, feature selection experiments, model training, evaluation, and visualizations are implemented in structured, publication-grade Jupyter Notebooks (`notebooks/01_*.ipynb` through `notebooks/09_*.ipynb`).
- **Modular Python Backend:** Reusable data loading, schema validation, preprocessing transformers, feature selectors, model wrappers, and evaluation metrics remain in decoupled Python modules under `src/` and are imported into notebooks.
- **Primary Target:** Crop Yield measured in **$\text{kg/ha}$** (yield per unit area, not gross production volume).
- **Evaluation Paradigm:** Strict chronological partitioning (Train: 1966–2011, Validation: 2012–2014, Test: 2015–2017) to prevent temporal target leakage.
- **Scientific Honesty:** Clear differentiation between scenario-based yield estimation (conditioned on observed season inputs) and true advance pre-season forecasting.

---

## 2. Dataset Attribution and Provenance

- **File Location:** `data/raw/crop_yield_dataset.csv`
- **Dataset Fingerprint (SHA-256):** Verified at runtime to guarantee reproducibility.
- **Total Observations:** 198,369 rows across 52 consecutive harvest years (1966–2017).
- **Geographic Coverage:** 309 agricultural districts across 20 Indian states.
- **Crop Coverage:** 21 major Indian crops (Cereals, Pulses, Oilseeds, Fibers, and Commercial crops).
- **Integrated Sources:**
  - **ICRISAT (District Level Data):** District-wise agricultural yields, cropping patterns, and fertilizer statistics.
  - **NASA POWER Agroclimatology:** Satellite and reanalysis meteorological parameters (temperature, precipitation, relative humidity).
  - **FAOSTAT:** National-level agricultural input aggregates (pesticide macro-consumption).

### Key Audit Findings (from `notebooks/01_data_audit.ipynb`):
1. **Multicollinearity:** Total `Fertilizer` is an exact mathematical sum of `Nitrogen + Phosphorus + Potassium` ($|\Delta| < 0.21$ in 100% of observations).
2. **Pesticide Invariance:** Pesticide consumption reflects annual national macro-aggregates from FAOSTAT and is constant across all districts within any single year.
3. **Crop Yield Heterogeneity:** Sugarcane yields (median $5,200\text{ kg/ha}$) differ by an order of magnitude from oilseeds/pulses (median $200\text{--}700\text{ kg/ha}$). Outlier handling must be crop-specific.
4. **Logical Key Integrity:** The composite tuple `(Year, Region, Crop, Season)` uniquely identifies all 198,369 rows with zero duplicate keys.

---

## 3. Project Directory Structure

```text
crop_yield_prediction/
├── config/                     # Configuration scaffolding (YAML)
│   ├── default_config.yaml     # Global paths, metrics, seeds
│   ├── schema_config.yaml      # Expected columns, data types, physical bounds
│   └── data_split_config.yaml  # Chronological split definitions
├── data/
│   ├── raw/                    # Read-only historical dataset (crop_yield_dataset.csv)
│   ├── processed/              # Processed datasets (generated during experiments)
│   └── interim/                # Temporary transformed partitions
├── notebooks/                  # Primary Research Environment (Jupyter Notebooks)
│   ├── 01_data_audit.ipynb     # Executed audit, schema integrity, and initial findings
│   ├── 02_exploratory_data_analysis.ipynb   # (Phase 2)
│   ├── 03_outlier_analysis.ipynb            # (Phase 3)
│   ├── 04_preprocessing.ipynb               # (Phase 4)
│   ├── 05_feature_engineering.ipynb         # (Phase 5)
│   ├── 06_feature_selection.ipynb           # (Phase 6)
│   ├── 07_model_training.ipynb              # (Phase 7)
│   ├── 08_model_evaluation.ipynb            # (Phase 8)
│   └── 09_future_yield_prediction.ipynb     # (Phase 9)
├── src/                        # Reusable Python Modules (imported by notebooks)
│   ├── data/                   # Data loader, schema validator, chronological splitters
│   │   ├── loader.py
│   │   └── schema.py
│   ├── preprocessing/          # Interchangeable preprocessing pipelines
│   │   └── base.py
│   ├── features/               # Domain feature engineering & independent selectors
│   │   ├── engineer.py
│   │   └── selector.py
│   ├── models/                 # Model wrappers and training orchestrators
│   │   └── base.py
│   └── evaluation/             # Academic regression metrics & crop breakdowns
│       └── metrics.py
├── tests/                      # Automated test suite
│   ├── test_data_loader.py
│   ├── test_schema_validation.py
│   ├── test_splits.py
│   └── test_interfaces.py
├── reports/                    # Methodological notes & governance documentation
│   └── methodological_risks.md
├── experiments/                # Persistent experiment records & artifacts
├── artifacts/                  # Serialized pipelines and model metadata
├── app/                        # Streamlit web application (Phase 9)
├── .gitignore                  # Python & ML ignore patterns
├── ARCHITECTURE_RULES.md       # 13 ML Architecture & governance rules
├── PROJECT_PROGRESS.md         # Phased milestone tracker
├── ROADMAP.md                  # Comprehensive implementation roadmap
├── pyproject.toml              # Project metadata & pytest configuration
├── requirements.txt            # Pinned, tested dependencies
└── README.md                   # This project guide
```

---

## 4. Installation and Environment Setup

### Prerequisites
- Python 3.11 or Python 3.12 (Python 3.12 recommended for full pre-built wheel compatibility on Windows).
- Git.

### 1. Clone Repository & Setup
```bash
git clone https://github.com/aryanpuranik22/crop-yield-prediction.git
cd crop-yield-prediction
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Running Notebooks & Automated Tests

### Launching Jupyter
```bash
jupyter notebook notebooks/
# Or launch the data audit directly:
jupyter notebook notebooks/01_data_audit.ipynb
```

### Running Automated Tests
```bash
python -m pytest tests/ -v
```

Current test status: **12 passed**.

---

## 6. Phased Implementation Roadmap

- **Phase 1: Project Initialization & Notebook-First Architecture** *(Completed - `01_data_audit.ipynb`)*
- **Phase 2: Exploratory Data Analysis (EDA)** *(Up Next - `02_exploratory_data_analysis.ipynb`)*
- **Phase 3: Outlier Handling & Robustness Analysis** *(`03_outlier_analysis.ipynb`)*
- **Phase 4: Preprocessing & Categorical Encoding Pipelines** *(`04_preprocessing.ipynb`)*
- **Phase 5: Agricultural Feature Engineering** *(`05_feature_engineering.ipynb`)*
- **Phase 6: Independent Feature Selection Experiments** *(`06_feature_selection.ipynb`)*
- **Phase 7: Machine Learning Model Training & Optimization** *(`07_model_training.ipynb`)*
- **Phase 8: Final Benchmark Evaluation** *(`08_model_evaluation.ipynb`)*
- **Phase 9: Future Yield Prediction & Streamlit Application** *(`09_future_yield_prediction.ipynb` & `app/`)*

See [ROADMAP.md](file:///d:/crop_yield_prediction/ROADMAP.md) and [PROJECT_PROGRESS.md](file:///d:/crop_yield_prediction/PROJECT_PROGRESS.md) for details.

---

## 7. License & Attribution

This project is developed for research and educational purposes. Original agricultural records are sourced from ICRISAT District Level Data, NASA POWER Agroclimatology, and FAOSTAT.
