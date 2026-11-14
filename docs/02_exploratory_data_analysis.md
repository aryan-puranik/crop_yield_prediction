# Exploratory Data Analysis — Crop Yield Prediction

## 1. Purpose and Scope

We perform exploratory data analysis (EDA) to understand the distribution of agricultural yield and its associations with crop identity, season, year, geography, climate, soil, and agricultural inputs. The analysis is based on the compiled `data/raw/crop_yield_dataset.csv` used throughout our project. We preserve that CSV unchanged: aggregations, temporary bins, transformations, and charts are produced in memory or saved to the `reports/` directory.

The dataset contains **198,369 observations**, **15 original columns**, **21 crops**, **20 states**, and records from **1966–2017**. The accompanying data audit is documented in `docs/data_analysis.md`; this EDA focuses on distributions, comparisons, relationships, and their implications for modeling rather than repeating the audit.

We distinguish **descriptive associations** from causal conclusions. In particular, pooled comparisons can reflect different combinations of crops, locations, and years. None of the curves in this notebook, on its own, establishes the effect of changing a single agricultural input.

## 2. Target Variable: Yield

Yield is recorded in **kg/ha**. We compare its original distribution with the transformed target `log1p(Yield)`, which is the natural logarithm of `1 + Yield`.

| Statistic | Original Yield | Log1p Yield |
|---|---:|---:|
| Mean | 1,239.22 kg/ha | 6.67 |
| Median | 800.00 kg/ha | 6.69 |
| Standard deviation | 1,515.32 kg/ha | 0.95 |
| Skewness | 3.74 | -0.10 |
| Excess kurtosis | 26.38 | 0.96 |

The untransformed target is substantially right-skewed: its mean exceeds its median and its upper tail contains high yield observations. After applying `log1p`, the overall distribution becomes much more symmetric, as indicated by the change in skewness from **3.74 to -0.10**. Excess kurtosis also decreases markedly, though the transformed distribution is **not perfectly normal**.

**Figure 1 — Target distribution diagnostics** combines a raw-yield histogram (displayed only through the 99th percentile for readability), the full log-transformed histogram, a full-range raw-yield boxplot, and a Q–Q plot of log-transformed yield. The Q–Q plot follows the reference line relatively closely in the middle but departs from it in the tails. The raw boxplot shows numerous high-valued statistical outliers. These do not all represent incorrect records, because crops have very different natural yield scales.

**Modeling implications.** We retain Yield on its original scale in the dataset and compare raw-target with log-target training strategies. We assess predictions after converting log-scale predictions back to **kg/ha**. Greater symmetry in the pooled target alone does not guarantee better predictive performance for every crop.

## 3. Crop-Wise Yield Distribution and Representation

We summarize each of the 21 crops using record counts, minimum and maximum yield, mean, median, quartiles, 95th percentile, standard deviation, interquartile range (IQR), and coefficient of variation (CV). IQR describes the middle 50% of yields; CV expresses standard deviation relative to the mean.

| Crop | Records | Median yield (kg/ha) | CV |
|---|---:|---:|---:|
| Sugarcane | 13,264 | 5,200.00 | 49.63% |
| Wheat | 13,227 | 1,555.98 | 54.36% |
| Rice | 14,476 | 1,433.62 | 55.92% |
| Maize | 13,615 | 1,302.43 | 70.68% |
| Chickpea | 13,473 | 674.60 | 89.55% |
| Cotton | 7,600 | 212.50 | 90.62% |

Sugarcane has the highest crop median, while Cotton has the lowest. Sugarcane's median is approximately **24.5 times** Cotton's median. These are different crops with different harvested-product characteristics, so a single pooled target distribution can obscure important differences. The relatively high CV values for Chickpea, Cotton, and Minor Pulses also indicate substantial within-crop variability; CV is affected by extreme observations and does not directly measure model difficulty.

**Figure 2 — Crop observation counts and median yields** shows uneven representation. Rice has **14,476** observations, while Safflower has **2,290**. The number of records and the size of the crop's yield are distinct attributes: the crop with the most records is not the crop with the highest median.

**Figure 3 — Crop-wise log-scale boxplots** displays all 21 crop distributions using a logarithmic **axis**, not a transformation of the underlying stored values. The figure makes the distributions visually comparable despite their large differences in scale and reveals long tails for several crops. The plot also makes extremely low positive yields visible. Statistical outliers are interpreted within crop groups rather than treated as universally invalid.

**Modeling implications.** We retain `Crop` as a central predictive feature and evaluate model errors separately by crop. We also inspect whether lower-representation crops show less stable performance. We avoid relying exclusively on a single aggregate error metric that could conceal poor results for specific crops.

## 4. Season and Crop–Season Dependency

We compare Kharif, Rabi, and Whole Year observations using counts, means, medians, standard deviations, IQR, and log-scale density curves.

| Season | Records | Mean yield (kg/ha) | Median yield (kg/ha) | IQR (kg/ha) |
|---|---:|---:|---:|---:|
| Kharif | 108,395 | 951.61 | 777.78 | 797.56 |
| Rabi | 58,562 | 1,021.94 | 796.88 | 780.30 |
| Whole Year | 31,412 | 2,636.78 | 1,000.00 | 4,093.46 |

Kharif accounts for the largest number of records. Whole Year has a much higher pooled mean and a considerably wider IQR. We do not conclude that growing a crop in the Whole Year category *causes* higher yields: the categories contain different crops, and these crops have different typical yield scales.

**Figure 4 — Seasonal yield analysis** compares seasonal means and medians and displays the `log1p` yield densities. Kharif and Rabi substantially overlap; Whole Year exhibits a more visibly multi-peaked shape, consistent with a mixture of crop yield scales. KDE peaks depend somewhat on smoothing and cannot independently identify the crops responsible for them.

We additionally examine a `Crop × Season` cross-tabulation for **all 21 crops**. The exclusivity check confirms:

- Crops belonging to exactly one season: **21**
- Crops belonging to multiple seasons: **0**

Thus, **Season is fully determined by Crop within this dataset**. It supplies no independent distinction among observations once the full crop category is known, although including it may affect the behavior of particular learning algorithms.

**Modeling implications.** We treat `Season` as a potentially redundant feature and compare models with and without it rather than dropping it without evaluation.

## 5. Historical Yield Trends (1966–2017)

We aggregate annual record counts, pooled mean and median yields, yield standard deviations, and average fertilizer and rainfall values. The complete analysis covers **52 years**.

| Year | Mean yield (kg/ha) | Median yield (kg/ha) | Mean fertilizer (kg/ha) |
|---|---:|---:|---:|
| 1966 | 812.23 | 493.15 | 5.16 |
| 1976 | 1,015.17 | 632.81 | 20.98 |
| 1986 | 1,127.23 | 714.29 | 50.78 |
| 1996 | 1,313.46 | 894.92 | 72.11 |
| 2006 | 1,345.34 | 883.61 | 114.05 |
| 2016 | 1,691.70 | 1,112.08 | 131.49 |

Between these two endpoints, the pooled mean yield increases by approximately **108%**. Mean fertilizer values also increase considerably. The simultaneous trends do **not** establish that fertilizer caused the yield increase: crop composition, geography, time, and unmeasured agricultural changes may influence both. Mean annual rainfall fluctuates rather than following the same steady pattern across the selected years.

**Figure 5 — Temporal trends** has three panels:

1. Annual observation volume varies noticeably, with shifts around the 1970s and late 1980s and a sharp reduction in 2017. We do not infer the reason for these coverage changes solely from the chart.
2. Pooled mean and median yield generally rise over time, with shorter-term fluctuations. Mean yield remains above median yield.
3. Separate trends for **Wheat, Rice, Maize, Groundnut, and Chickpea** show that crops differ in the magnitude and trajectory of their historical yield changes.

We describe this chart as **crop-specific historical yield trends**; it does not isolate the causal impact of any named agricultural policy or technology.

**Modeling implications.** We retain `Year` as a candidate predictor and use chronological evaluation. Changes in the mix or number of observations, particularly in 2017, remain relevant when interpreting model performance on later years.

## 6. Geographic Variation

We derive `State` from the district–state string in `Region` for grouping and visualization, while keeping `Region` unchanged. We standardize the displayed spelling `AndhraPradesh` to `Andhra Pradesh` in the derived state field.

The state-level summary includes record counts, distinct district counts, pooled mean and median yields, mean rainfall, and mean fertilizer values.

| State | Records | Districts |
|---|---:|---:|
| Uttar Pradesh | 31,885 | 46 |
| Madhya Pradesh | 26,538 | 37 |
| Maharashtra | 19,767 | 26 |
| Rajasthan | 17,401 | 26 |
| Karnataka | 14,496 | 19 |
| Kerala | 2,047 | 10 |

Geographic representation is uneven. Uttar Pradesh contributes the most observations and Kerala the fewest among the 20 states in this dataset.

**Figure 6 — State-level counts and median yield** shows this imbalance alongside different state-level pooled yield medians. Punjab has the highest pooled state median in the displayed comparison (approximately **1,082.53 kg/ha**); Telangana is among the lowest (approximately **555.89 kg/ha**). These are **not direct rankings of state agricultural efficiency or productivity**, because each state contains a different mix of crops and observations.

The state summary also shows marked differences in average rainfall and fertilizer values, such as high mean rainfall in Kerala and high mean fertilizer values in Punjab. These comparisons are descriptive rather than causal.

**Figure 7 — Wheat and Rice across selected states** narrows the geographic comparison to two named crops in Punjab, Haryana, Uttar Pradesh, Bihar, West Bengal, Madhya Pradesh, and Rajasthan. Comparing distributions *within a crop* is more informative than comparing pooled state yields, though differences in year and district coverage remain possible.

**Modeling implications.** We retain geographic identity as a candidate source of predictive information. Because `Region` already includes state identity, we use the derived `State` primarily for EDA and subgroup evaluation and assess any additional model feature separately.

## 7. Climate Feature Distributions and Associations

We examine three climate variables: `Temperature`, `Rainfall`, and `Humidity`. The notebook calculates descriptive statistics, including tail percentiles, and plots individual distributions.

**Figure 8 — Climate feature distributions** displays histograms and smoothed density estimates for all three variables. These show how the observed climate features are distributed in the dataset; they do not by themselves establish which conditions are best for crop yield.

**Figure 9 — Binned climate–yield curves** divides each climate feature into quantile-based groups and plots the **median** Yield in each bin. For readability, the rainfall plot uses observations at or below **3,500 mm**. The displayed curves are pooled across crops and years, so their shapes can reflect changes in the composition of observations as well as possible climate associations. They are not experimentally measured crop-response functions.

**Figure 10 — Crop-specific rainfall comparisons** repeats a binned median-yield analysis separately for **Rice** and **Pearl Millet**. This provides a more crop-aware comparison of rainfall associations than the pooled plot. Even within a crop, observations may still differ by district, soil characteristics, and year.

**Modeling implications.** We retain the climate variables as candidate predictors. We allow for the possibility of nonlinear and crop-dependent relationships rather than assuming every predictor acts linearly or identically across crops. We do not infer precise optimal rainfall, humidity, or temperature settings from these exploratory curves.

## 8. Soil Type and pH

The notebook summarizes the six soil categories with observation counts, pooled mean and median yields, and pH statistics (mean, median, standard deviation, minimum, and maximum).

**Figure 11 — Soil and pH diagnostics** combines:

- Counts by `Soil Type`;
- pH distributions within each soil category;
- Pooled median Yield across quantile-based pH bins.

This lets us examine whether soil categories have different pH distributions and whether pooled yields vary over the observed pH spectrum. Because soil type, geography, crop choice, and pH may be associated with one another, we do not treat the pooled pH curve as evidence of an independently optimal pH value.

**Modeling implications.** We retain `Soil Type` and `pH` as candidate predictors while recognizing that they may contain overlapping information. We compare their usefulness during chronological validation rather than selecting features solely on their pooled relationships with Yield.

## 9. Nutrient Inputs and Fertilizer Trends

We examine distributions of `Nitrogen`, `Phosphorus`, `Potassium`, and total `Fertilizer` and their annual historical averages.

**Figure 12 — Nutrient distributions** presents the four input variables side by side. **Figure 14 — Historical nutrient trends** traces the annual mean of the same variables across 1966–2017. These plots describe recorded inputs and how they vary across observations and years.

The data audit established that total `Fertilizer` is approximately the sum of N, P, and K: **169,546 records (85.47%)** differ by no more than **0.01 kg/ha**, and all records differ by no more than approximately **0.21 kg/ha**. We therefore avoid treating the four columns as independent measures of different processes.

**Modeling implications.** We compare alternative nutrient feature groups, especially **N/P/K components versus total Fertilizer**, without automatically dropping or combining columns in the source CSV. We do not interpret observational fertilizer–yield patterns as proof of an optimal application rate.

## 10. Correlations and Feature Redundancy

We compute **Pearson** (linear association) and **Spearman** (rank-based monotonic association) matrices for the numeric predictors and Yield:

`Year`, `Temperature`, `Rainfall`, `Humidity`, `pH`, `Nitrogen`, `Phosphorus`, `Potassium`, `Fertilizer`, `Pesticide`, and `Yield`.

The notebook extracts pairs with **absolute Pearson correlation of at least 0.70**, saves correlation tables, and produces two main visualizations:

- **Figure 16 — Pearson and Spearman heatmaps:** compares the overall dependency patterns among numeric features.
- **Figure 17 — Correlations with Yield:** compares Pearson and Spearman coefficients for each numeric predictor against the target.

We interpret high pairwise correlations as possible redundancy or association, not as proof of causation. Conversely, low global correlation with Yield does not establish that a feature is unhelpful: relationships may be nonlinear or differ across crops. The known near-algebraic overlap between Fertilizer and its N/P/K components requires particular attention.

The previously audited `Pesticide` field is a **year-level national value repeated across districts** rather than an independently varying district-level measurement. It has only **16 distinct values** in the dataset. We avoid interpreting it as a precise local pesticide application feature and compare models with and without it.

**Modeling implications.** We use correlations to identify candidate feature dependencies, then make retention decisions through time-aware model evaluation rather than correlation thresholds alone. Numerical correlation is only one part of feature assessment and does not cover categorical variables such as Crop and Region.

## 11. Climate and Fertilizer Interactions

**Figure 18 — Temperature × Rainfall median-yield heatmap** groups both climate features into quantile-based bins (eight groups per variable) and displays pooled median Yield for each combination. This reveals how target distributions vary across joint climate categories rather than examining one variable at a time. Individual cells may represent different mixtures of crops, regions, and years.

**Figure 19 — Fertilizer versus Yield by crop** constructs separate binned median-yield curves for **Sugarcane, Wheat, Rice, and Groundnut**. Crop-specific views reduce one important source of pooled-scale confounding, but do not remove differences in weather, soil, location, or historical period.

We do not label peaks in these plots as experimentally verified optimal fertilizer doses or climatic conditions.

**Modeling implications.** These analyses support testing models capable of learning interactions and nonlinear associations. We assess any benefit on held-out years rather than relying on the appearance of EDA curves.

## 12. Crop-Specific Outlier Candidates

We compute crop-specific lower and upper quartiles and define two **upper-tail** screening thresholds:

- **Mild candidate:** above `Q75 + 1.5 × IQR`;
- **Extreme candidate:** above `Q75 + 3 × IQR`.

For each crop, the notebook records both thresholds, counts above them, the maximum reported yield, and the ratio of maximum to median. The resulting table ranks crops by maximum-to-median ratio. This is an **exploratory screening rule**; it is not a classifier of erroneous observations, and the selected code checks upper-tail extremes rather than lower-tail anomalies.

Our earlier data audit identified two especially unusual Chickpea records:

| Year | Region | Reported yield (kg/ha) |
|---|---|---:|
| 2007 | Muzaffarpur, Bihar | 58,363.64 |
| 2007 | Saharsa, Bihar | 32,000.00 |

These represent approximately **86.5×** and **47.4×** the Chickpea median of **674.60 kg/ha**, respectively. We **flag them as suspected anomalies**, not confirmed errors. All original observations remain in the CSV.

**Modeling implications.** We preserve the dataset unchanged and later compare training strategies with and without individually justified exclusions or robust treatments. We do not automatically remove observations from validation or test data.

## 13. Modeling Decisions Informed by EDA

Our EDA supports the following working decisions, which will be tested rather than assumed to be optimal:

1. **Chronological evaluation:** training on **1966–2011**, validation on **2012–2014**, and testing on **2015–2017**. This better represents prediction on later years than a random split across the entire history.
2. **Crop-aware evaluation:** we report both overall errors and crop-specific performance because crop frequencies, typical yields, and variability differ substantially.
3. **Target comparison:** we compare original Yield and `log1p(Yield)` targets; performance is reported after predictions are placed back on the original kg/ha scale.
4. **Feature redundancy checks:** we compare models with and without `Season`, with alternative nutrient representations (`N/P/K` versus `Fertilizer`), and with and without `Pesticide`.
5. **Geographic and temporal features:** we retain `Year`, `Crop`, and location-related information as candidates, while assessing whether derived `State` adds value beyond `Region`.
6. **Nonlinear relationships and interactions:** we investigate models that can represent crop-dependent climate, soil, and nutrient associations rather than assuming global linear relationships.
7. **Conservative handling of anomalies:** we retain the source observations; suspicious crop-specific values are flagged and assessed through controlled training comparisons rather than silently removed.
8. **Prediction scope:** weather and agricultural input values measured over a completed growing period can support retrospective yield estimation or scenarios. A genuine *advance* yield forecast requires these predictors to be available or forecast at the intended prediction time.

## 14. Limitations of the Analysis

This notebook describes patterns in a compiled historical dataset. Several limitations affect interpretation:

- **Uneven coverage:** crops, states, districts, and years contribute different numbers of observations.
- **Mixed crop scales:** pooled yields blend biologically and economically different crop outputs.
- **Observational confounding:** crop, location, season, year, climate, and inputs can change together; visual associations do not identify independent causal effects.
- **Feature overlap:** `Season` is determined by `Crop`; `Fertilizer` is nearly the sum of N/P/K; `State` is embedded in `Region`.
- **Coarse input resolution:** `Pesticide` varies by year nationally rather than district, restricting its interpretation as local exposure.
- **Extreme reported values:** unusual yield observations may influence the mean, CV, correlations, and squared-error model training.
- **Prediction-time availability:** not every variable in a historical record will necessarily be known before harvest.

The **reviewed notebook does not contain saved plot outputs or numerical results for all later sections**. Therefore, this report deliberately does not assign unobserved climate optima, numeric correlation strengths, soil-effect rankings, or detailed fertilizer-response shapes. Those findings require inspection of the figures and tables from a successful full run.

## 15. Generated Analysis Artifacts

The reviewed notebook saves its outputs under:

- `reports/figures/eda/` — distribution plots, crop/season/year/state comparisons, climate and soil diagnostics, nutrient trends, correlation visualizations, and interaction figures.
- `reports/tables/eda/` — target statistics, crop summaries, crop–season composition, annual trends, state and soil summaries, correlation tables, and crop-specific outlier-candidate counts.

Figure numbering in the reviewed notebook follows the retained original numbering and is **not consecutive** because some redundant analyses were removed. These files are generated artifacts; their filenames do not imply that every number in the original longer notebook is still present.

## 16. Summary

We observe that **crop identity, time, and geography** are central to understanding the variation in recorded agricultural yields. The target is strongly skewed on the original scale and becomes substantially more symmetric under `log1p`. Crop groups vary greatly in typical yield and representation; Season is completely determined by Crop in the supplied data. Historical yields rise overall but with crop-specific trajectories and uneven annual coverage. Climate, soil, and agricultural inputs exhibit observational associations that require careful, crop-aware interpretation.

Our next phase uses these findings to prepare features and evaluate predictive models chronologically, without altering the original CSV or assuming that exploratory associations establish causal effects.
