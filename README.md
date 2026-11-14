# Crop Yield Prediction and Forecasting Using Agricultural Data and Machine Learning

**Author:** Aryan Puranik  
**Academic Project:** Bachelor of Technology / Computer Science & Engineering (Machine Learning)  
**Historical Scope:** 1966–2017 (52 years across 309 Indian districts and 21 crops)  

---

## 1. Project Overview

Accurate agricultural crop yield prediction is crucial for food security planning, agro-economic risk management, and agricultural policy formulation. This project implements a reproducible, research-grade machine learning system to predict and forecast crop yields across Indian agricultural districts.

### Key Methodological Highlights:
- **Prediction Target:** Crop Yield measured strictly in **$\text{kg/ha}$** (productivity per unit area), eliminating the acreage confounding inherent in total production volume.
- **Leakage Prevention:** Chronological data splitting (Train: 1966–2011, Validation: 2012–2014, Test: 2015–2017) ensures future technological and climatic drift does not contaminate past training data.
- **Crop-Stratified Integrity:** Outlier handling and performance evaluation are applied on a per-crop basis, acknowledging that biological baselines vary by more than an order of magnitude (Sugarcane $\sim 5,200\text{ kg/ha}$ vs. Cotton $\sim 212\text{ kg/ha}$).
- **Notebook-First Research:** Core scientific analysis is organized into 4 concise Jupyter Notebooks with detailed theory and methodology documented in `docs/`.

---

## 2. Repository Structure

```text
crop_yield_prediction/
├── app.py                      # Interactive Streamlit Web Application
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Build & test configuration
├── README.md                   # Project documentation and guide
│
├── data/
│   ├── raw/                    # Read-only original dataset (crop_yield_dataset.csv)
│   └── processed/              # Chronological splits (train.csv, val.csv, test.csv)
│
├── notebooks/                  # 4-Stage Research Notebooks
│   ├── 01_exploratory_data_analysis.ipynb     # Target distributions, climate & collinearity
│   ├── 02_data_preparation.ipynb             # Chronological split, outlier removal, export
│   ├── 03_feature_selection.ipynb            # Collinearity tests, MI, tree importances
│   └── 04_model_training_evaluation.ipynb    # Model training, test evaluation, pipeline export
│
├── docs/                       # Comprehensive Methodology & Viva Guides
│   ├── 01_data_audit.md                      # Raw data schema, provenance & limitations
│   ├── 02_exploratory_data_analysis.md       # In-depth statistical EDA tables and insights
│   ├── 03_feature_selection_guide.md         # Collinearity proofs, VIF, selection strategies
│   └── 04_model_evaluation_and_viva.md      # Metrics, crop breakdowns & viva defense Q&A
│
├── models/                     # Saved Final Fitted Machine Learning Pipeline
│   └── best_pipeline.joblib    # scikit-learn Pipeline (preprocessing + Extra Trees)
│
├── reports/
│   ├── figures/eda/            # 20 publication-grade figures from Phase 2 EDA
│   ├── tables/eda/             # 16 reproducible statistical CSV tables from Phase 2 EDA
│   └── methodological_risks.md # Methodological notes & leakage prevention safeguards
│
├── src/                        # Reusable Python Utility Modules
│   ├── __init__.py
│   ├── utils.py                # Data loading, chronological splitting, SHA-256 fingerprint
│   └── metrics.py              # Regression metrics & crop-wise breakdown calculations
│
└── tests/                      # Automated Pytest Suite
    ├── test_data.py            # Unit tests for loading and chronological splits
    └── test_metrics.py         # Unit tests for metric calculations
```

---

## 3. Dataset Attribution and Key Findings

- **Dataset File:** `data/raw/crop_yield_dataset.csv`
- **Total Records:** 198,369 observations spanning 1966 to 2017.
- **Coverage:** 309 districts across 20 Indian states and 21 major crops.
- **Integrated Sources:** ICRISAT (district agricultural statistics), NASA POWER (agroclimatology), and FAOSTAT (national pesticide consumption).

### Major Findings:
1. **Target Skewness:** Raw yield has high positive skew ($+3.74$), driven by high-yielding commercial crops like Sugarcane.
2. **Deterministic Multicollinearity:** Across 100% of rows, $\text{Fertilizer} \equiv \text{Nitrogen} + \text{Phosphorus} + \text{Potassium}$ ($|\Delta| \le 0.21\text{ kg/ha}$). Total Fertilizer must be removed from linear models to avoid infinite VIF.
3. **Data-Entry Outliers:** Two extreme Chickpea entries in Bihar (2007) recorded $>30,000\text{ kg/ha}$ (historical median is $675\text{ kg/ha}$). These are pruned strictly from the training partition.
4. **Pesticide Broadcast:** Pesticide application has only 16 unique values and zero within-year district variation, acting as a national-level macro indicator.

---

## 4. Quickstart & Installation

### Step 1: Clone and Set Up Python Environment
```bash
git clone https://github.com/aryan-puranik/crop_yield_prediction.git
cd crop_yield_prediction

# Create and activate a virtual environment (Python 3.11 or 3.12 recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Automated Tests
```bash
pytest tests/
```
*(All 5 test cases should pass in under 3 seconds)*

---

## 5. Notebook Research Workflow

The project analysis proceeds through 4 self-contained Jupyter notebooks:

1. **`notebooks/01_exploratory_data_analysis.ipynb`**
   - Inspects distributions of target and environmental predictors.
   - Plots crop-wise yield variance and tests fertilizer collinearity.
   - *Reference Guide:* [`docs/02_exploratory_data_analysis.md`](docs/02_exploratory_data_analysis.md)

2. **`notebooks/02_data_preparation.ipynb`**
   - Implements temporal holdout: Train ($\le 2011$), Val ($2012\text{–}2014$), Test ($2015\text{–}2017$).
   - Prunes training data-entry errors without touching validation/test sets.
   - Generates engineered domain features (`Rainfall_per_Temp`, `NP_Ratio`, `NK_Ratio`).
   - Exports clean datasets to `data/processed/`.

3. **`notebooks/03_feature_selection.ipynb`**
   - Benchmarks Baseline vs Collinearity-Filtered feature sets.
   - Evaluates Tree-based MDI feature importances and Mutual Information scores.
   - *Reference Guide:* [`docs/03_feature_selection_guide.md`](docs/03_feature_selection_guide.md)

4. **`notebooks/04_model_training_evaluation.ipynb`**
   - Trains Ridge, Decision Tree, Random Forest, and Extra Trees.
   - Evaluates champion model on held-out test data ($2015\text{–}2017$).
   - Computes crop-wise breakdown and diagnostic residual plots.
   - Serializes complete pipeline to `models/best_pipeline.joblib`.
   - *Reference Guide:* [`docs/04_model_evaluation_and_viva.md`](docs/04_model_evaluation_and_viva.md)

---

## 6. Experimental Results

### Model Benchmark on Validation Split (2012–2014)

| Model | Val MAE (kg/ha) | Val RMSE (kg/ha) | Val $R^2$ | Notes |
| :--- | :---: | :---: | :---: | :--- |
| **Ridge Regression** | 630.89 | 1000.47 | 0.6635 | Fast linear baseline; misses non-linear responses. |
| **Decision Tree** | 509.40 | 882.11 | 0.7384 | Captures weather interactions; prone to variance. |
| **Random Forest** | 457.18 | 755.56 | 0.8081 | Strong ensemble generalization. |
| **Extra Trees (Champion)** | **453.88** | **740.95** | **0.8155** | Best balance of variance reduction and fit. |

### Held-Out Test Evaluation (2015–2017)
- **Test $R^2$:** **0.7206**
- **Test MAE:** **520.84 kg/ha**
- **Test RMSE:** **936.24 kg/ha**

### Crop-Wise Breakdown (Selected Benchmark Crops)

| Crop | Test Samples | Mean True Yield (kg/ha) | Test MAE (kg/ha) | Test RMSE (kg/ha) | Test $R^2$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Wheat** | 714 | 2,605.42 | 583.89 | 768.17 | 0.5502 |
| **Rice** | 756 | 2,374.55 | 551.07 | 725.51 | 0.4166 |
| **Sugarcane** | 629 | 6,638.25 | 1681.93 | 2400.44 | 0.1286 |
| **Maize** | 763 | 2,714.69 | 965.66 | 1503.51 | 0.2825 |
| **Cotton** | 465 | 315.80 | 68.20 | 104.50 | 0.8120 |

---

## 7. Interactive Streamlit Web Application

The project includes an interactive web application allowing users to input district location, crop type, soil taxonomy, climate sliders, and macronutrient applications to predict expected crop yield.

### Launching the Application:
```bash
streamlit run app.py
```

### Features:
- Predicts expected yield in **kg/ha**, **Tonnes/Hectare**, and **Quintals/Acre**.
- Displays comparison against the historical national median for the selected crop.
- Explains model assumptions, agronomic context, and limitations in real-time.

---

## 8. Academic Viva Voce / Project Defense Q&A

**Q1: Why is your target Yield (kg/ha) instead of Total Production (Tonnes)?**  
*Answer:* Total production is confounded by farm area (hectares). A large district produces more tonnes simply because it has more farmland, not because farming is more productive. Modeling Yield (kg/ha) normalizes for farm size, allowing us to evaluate true agricultural productivity and climatic response.

**Q2: Why did you use chronological splitting instead of random K-fold cross-validation?**  
*Answer:* Agricultural data has strong temporal trends (e.g. Green Revolution fertilizer adoption, high-yielding seed varieties). Shuffling years randomly in $k$-fold cross-validation leaks future yield drift into past training data, creating artificially inflated accuracy that fails in real-world deployment.

**Q3: Why did you drop total Fertilizer during feature selection?**  
*Answer:* In our exploratory analysis, $\text{Fertilizer} \equiv \text{Nitrogen} + \text{Phosphorus} + \text{Potassium}$ across 100% of rows. Keeping both causes exact multicollinearity ($R^2 = 1.0$), destabilizing regression coefficients and inflating variance.

**Q4: Why is overall $R^2$ insufficient for evaluating agricultural models?**  
*Answer:* Sugarcane yields $>5,000\text{ kg/ha}$ while Cotton yields $\sim 212\text{ kg/ha}$. In a pooled dataset, high-yield crops dominate the variance, meaning a model could score high overall $R^2$ while failing on lower-yield crops. Therefore, crop-wise error metrics are mandatory.

---

## 9. License & Academic Citation

This project is developed for academic, educational, and research purposes.  
**Author:** Aryan Puranik (2026)
