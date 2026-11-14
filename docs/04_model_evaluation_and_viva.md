# Model Evaluation, Limitations, and Viva Guide

## 1. Evaluation Methodology

### 1.1 Chronological Evaluation vs Random K-Fold
In time-series and agricultural modeling, standard random k-fold cross-validation is a major flaw because it randomly shuffles historical years. This leaks future technological improvements (e.g., Green Revolution yield increases, modern irrigation) into past training data, yielding artificially high test accuracy.

**Our Chronological Partition Strategy:**
- **Training Set (1966–2011, 46 years):** 176,196 records (88.82%) — Model fitting and learning.
- **Validation Set (2012–2014, 3 years):** 11,345 records (5.72%) — Feature selection and hyperparameter tuning.
- **Held-Out Test Set (2015–2017, 3 years):** 10,828 records (5.46%) — Final benchmark evaluation (unseen during development).

### 1.2 Evaluation Metrics
We report three complementary regression metrics:
1. **MAE (Mean Absolute Error):** Measures average absolute prediction error in kg/ha. Robust to extreme outliers.
2. **RMSE (Root Mean Squared Error):** Penalizes large prediction errors more severely. Essential for agricultural risk management.
3. **R-squared (Coefficient of Determination):** Proportion of target variance explained.

> **Important Caution on R-squared:**
> A high overall R-squared (e.g. 0.90) across pooled crops can be misleading because high-yield crops (Sugarcane ~5,200 kg/ha) dominate the total variance. A model could achieve a high pooled R-squared while failing drastically on lower-yield crops like Cotton (212 kg/ha). Therefore, **crop-wise error reporting is mandatory**.

---

## 2. Model Comparison and Selection

| Model | Test MAE (kg/ha) | Test RMSE (kg/ha) | Test R-squared | Training Time | Pros & Cons |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Ridge Regression** | 382.4 | 612.8 | 0.742 | Fast (<2s) | High bias; cannot capture non-linear weather response curves. |
| **Decision Tree** | 294.6 | 518.2 | 0.815 | Fast (<3s) | Captures interactions, but prone to high variance and overfitting. |
| **Random Forest** | 242.1 | 418.5 | 0.880 | Moderate | Excellent non-linear performance; averages out tree variance. |
| **Extra Trees** | 238.6 | 412.3 | 0.884 | Moderate | Randomized thresholds reduce variance further; strong generalization. |
| **HistGradientBoosting** | 235.2 | 405.7 | 0.888 | Fast (<10s) | Best overall accuracy; native binning handles non-linearities efficiently. |

---

## 3. Crop-Wise Performance Breakdown (Selected Benchmark Crops)

| Crop | Test Samples | Mean Actual Yield (kg/ha) | Test MAE (kg/ha) | Test RMSE (kg/ha) | Test R-squared |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Wheat** | 812 | 2,842.1 | 185.3 | 268.4 | 0.892 |
| **Rice** | 895 | 2,410.6 | 172.8 | 251.2 | 0.885 |
| **Sugarcane** | 824 | 5,840.2 | 485.6 | 724.1 | 0.871 |
| **Maize** | 845 | 1,980.4 | 210.4 | 312.8 | 0.864 |
| **Chickpea** | 810 | 890.2 | 112.5 | 168.2 | 0.841 |
| **Cotton** | 465 | 315.8 | 68.2 | 104.5 | 0.812 |

---

## 4. Academic Viva Voce / Project Defense Q&A

### Q1: Why is your target Yield (kg/ha) instead of Total Production?
**Answer:** Total production (in tonnes) is confounded by cultivated land area (hectares). A large district produces more tonnes simply because it has more farmland, not because farming is more productive. Modeling Yield (kg/ha) normalizes for farm size, allowing us to study true agricultural efficiency and weather response.

### Q2: Why did you not remove outliers globally across the dataset?
**Answer:** In agricultural data, different crops have fundamentally different biological yields. Sugarcane produces high-moisture fresh biomass with a median yield of 5,200 kg/ha, whereas Cotton produces dry fiber with a median yield of 212 kg/ha. A global outlier threshold across the pooled dataset would wipe out over 85% of valid Sugarcane records. Outliers must be treated on a **crop-stratified basis** on training data only.

### Q3: Why is total Fertilizer collinear with N, P, and K?
**Answer:** Our data audit revealed that in 100% of observations, Fertilizer is within 0.21 kg/ha of N + P + K. In India, official fertilizer consumption statistics report total NPK as the sum of Nitrogen, Phosphorus, and Potassium. Including all four in linear models causes severe multicollinearity.

### Q4: Why can this model not be claimed as an advance pre-season forecast?
**Answer:** The dataset includes seasonal cumulative rainfall, mean temperature, and applied fertilizer. These values are measured **during or after the growing season**. Therefore, this system performs **scenario-based yield estimation** under known weather conditions (e.g. "What will yield be if rainfall is 1,000 mm?"). A true pre-season forecast would require seasonal weather forecasts rather than observed post-season totals.

### Q5: How did you prevent data leakage during preprocessing and feature selection?
**Answer:** All preprocessing transformers (e.g. `StandardScaler`, `OneHotEncoder`) and supervised feature selectors were fitted strictly on the historical training set (1966–2011). The validation and test sets were only transformed using the fitted parameters, ensuring no future statistical distributions leaked into training.
