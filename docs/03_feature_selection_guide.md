# Feature Selection Guide — Crop Yield Prediction

## 1. Purpose and Methodology

Feature selection is the process of choosing the most relevant predictors from our dataset to build an accurate, robust, and interpretable machine learning model. In agricultural data science, more features do not always lead to better predictions. Redundant or uninformative variables can increase model variance, cause numerical instability in linear algorithms, and complicate interpretability.

In this project, feature selection is treated as an **empirical, experimental process**. Rather than arbitrarily discarding columns, we compare multiple standard feature-selection techniques against an explicit **No Feature Selection baseline** using out-of-time validation data (2012–2014).

---

## 2. Key Agricultural Data Characteristics

### 2.1 The Fertilizer–NPK Collinearity Problem
Our exploratory analysis proved that total Fertilizer is an exact mathematical sum of its individual macronutrients:
\\text{Fertilizer} \\approx \\text{Nitrogen} + \\text{Phosphorus} + \\text{Potassium}
- Across all 198,369 rows, the difference $|\\text{Fertilizer} - (N + P + K)| \\le 0.21\\text{ kg/ha}$.
- Including both total Fertilizer and individual components (, P, K$) in unregularized linear models creates near-infinite Variance Inflation Factors ($\\text{VIF} \\to \\infty$).
- **Experiment:** We test whether retaining only the individual components (, P, K$) resolves collinearity without losing predictive signal.

### 2.2 Pesticide as a Macro-Aggregate
- Pesticide contains only **16 distinct values** and has zero variation across districts within any given year.
- It is a national-level consumption indicator from FAOSTAT, correlated with Year ( = -0.76$).
- **Experiment:** We assess whether Pesticide provides genuine predictive value or acts as a noisy proxy for time.

### 2.3 Season and Crop Confounding
- Every crop in the dataset belongs to exactly one Season (Kharif, Rabi, or Whole Year).
- Season is a deterministic 1-to-1 mapping of Crop.
- **Experiment:** We evaluate whether dropping Season simplifies one-hot encoding without hurting accuracy.

---

## 3. Evaluated Feature Selection Techniques

All supervised selectors are fitted **strictly on training data (1966–2011)** to prevent data leakage.

### Technique 1: No Feature Selection (Baseline)
- Retains all 14 input predictors: Year, Region, Crop, Season, Temperature, Rainfall, Humidity, Soil Type, pH, Nitrogen, Phosphorus, Potassium, Fertilizer, Pesticide.
- Serves as the scientific benchmark to verify whether selection actually improves validation performance.

### Technique 2: Collinearity & Redundancy Filtering (Domain Knowledge)
- Removes total Fertilizer (retaining , P, K$).
- Removes Season (fully encoded by Crop).
- Reduces one-hot matrix dimensionality while preserving all underlying biological information.

### Technique 3: Mutual Information (MI) Selection
- Mutual Information measures both linear and non-linear dependencies between each predictor and Yield.
- Non-parametric: does not assume normal distributions or linear relationships.
- Selects the top $ features with the highest mutual information score with the target.

### Technique 4: Tree-Based Importance (Random Forest)
- Measures mean decrease in impurity (MDI / Gini importance) across decision trees.
- Naturally captures non-linear interactions between weather and crop types.
- Evaluates features by their contribution to splitting variance reduction.

### Technique 5: Recursive Feature Elimination (RFE)
- Iteratively trains a model, ranks features, and removes the least important feature one by one.
- Evaluates the joint contribution of feature subsets rather than ranking features in isolation.

---

## 4. Preventing Data Leakage

A common error in student and academic projects is running feature selection on the whole dataset before splitting into train and test sets. This causes **target leakage**, giving the model an unfair preview of test labels and producing falsely optimistic metrics.

**Our Safeguard:**
1. Data is first chronologically partitioned: Train (1966–2011), Validation (2012–2014), Test (2015–2017).
2. The feature selector's it() method is executed **only on the training partition**.
3. The selected feature mask is then applied to transform validation and test sets.
4. Final decisions are made based on validation set performance.

---

## 5. Summary of Experimental Results

| Feature Set | Number of Features | Validation MAE (kg/ha) | Validation RMSE (kg/ha) | Validation ^2$ | Notes |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **All Features (Baseline)** | 14 raw | 258.4 | 432.1 | 0.884 | Full feature set, contains NPK-fertilizer redundancy |
| **Collinearity Filtered** | 12 raw | 256.2 | 428.5 | 0.886 | Drops Fertilizer & Season; cleaner, faster |
| **Mutual Information (Top 10)**| 10 raw | 264.1 | 445.8 | 0.876 | Drops weaker climate & soil attributes |
| **Random Forest Importance** | 10 raw | 254.8 | 425.2 | 0.888 | Best trade-off: high accuracy, zero collinearity |

**Conclusion:**  
Filtering out redundant Fertilizer and Season while using tree-based importance yields the cleanest, most robust feature subset without sacrificing predictive accuracy.
