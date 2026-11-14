Dataset Audit and Analysis
Project: Crop Yield Prediction Using Machine Learning
Dataset: data/raw/crop_yield_dataset.csv
Period: 1966–2017
Target: Yield (kg/ha)
1. Dataset Overview and Provenance
We use an existing compiled and processed Indian agricultural dataset from Sid's crop-yield project. It combines historical agricultural and environmental variables, some of which were derived, aggregated, or backfilled rather than measured independently for every district, crop, and year.

The dataset contains 198,369 observations, 15 original columns, 21 crop categories, 3 seasons, 6 soil types, and 309 region labels over 52 years (1966–2017). The prior audit identified coverage across 20 states.

Because this dataset was previously processed, we evaluate the dataset available for modeling. For example, finding no missing values does not establish how incomplete values may have been handled during preparation.
2. Numerical Summary and Yield Scale
Across all crops, the yield mean is 1,239.22 kg/ha and the median is 800.00 kg/ha. The overall maximum is 58,363.64 kg/ha and yield skewness is approximately +3.74, indicating a long right tail. The pooled statistics are influenced by crops with very different typical yield scales, so crop-wise comparisons are essential.

Additional numerical observations from the summary table:
- Rainfall has a mean of 1,019.97 mm, a maximum of 8,409 mm, and skewness of 2.21.
- Temperature has a mean of 25.58°C and a minimum of −2.84°C; negative temperatures require geographic context rather than automatic rejection.
- Potassium has skewness of 3.51, showing a strongly right-skewed distribution.
We interpret these figures as descriptions of the compiled dataset, not proof that every measurement is accurate.
3. Categorical Feature Summary
Feature	Unique categories	Most common category	Records	Share of all records
Crop	21	Rice	14,476	7.30%
Season	3	Kharif	108,395	54.64%
Soil Type	6	Vertisols	66,575	33.56%
Region	309	Dharwad, Karnataka	980	0.49%


Rice is the most frequently recorded crop, but represents only 7.30% of all observations. Kharif accounts for 54.64%, while Vertisols accounts for 33.56%. Dharwad, Karnataka has the highest individual region frequency, but accounts for only 0.49% of records.

These results demonstrate categorical coverage, not equal representation across categories. In the supplied dataset, Season was found to be determined by Crop, so seasonal frequencies largely reflect crop composition rather than an independently observed seasonal effect. Feature importance cannot be inferred from frequency alone.
4. Missing Values, Empty Strings, and Duplicates
The existing data audit reports no detected null values, empty strings, full-row duplicates, or duplicate combinations of Year, Region, Crop, and Season in the supplied compiled dataset.

We use these checks to verify the current CSV, while recognizing that some inputs may already have been filled or reconstructed during dataset preparation. The empty-string check does not automatically catch text cells containing only spaces.

A unique logical key supports record-level consistency, but does not by itself establish that every measurement is correct.
5. Zero and Repeated Value Analysis
A separate check counted zeros, unique numerical values, and frequently repeated values.
Feature	Zero-valued records	Unique values	Most frequent value	Its frequency
Year	0	52	1992	4,288
Temperature	0	1,107	25.85	1,553
Rainfall	0	9,718	1,234.00	236
Humidity	0	564	47.90	1,340
pH	0	65	6.80	52,166
Nitrogen	1,426	8,204	0.00	1,426
Phosphorus	1,603	4,849	0.00	1,603
Potassium	5,885	3,195	0.00	5,885
Fertilizer	1,388	9,803	0.00	1,388
Pesticide	0	16	0.44	90,282
Yield	0	87,809	1,000.00	8,718


Our observations:
- Pesticide has only 16 unique values; 0.44 appears in 90,282 records (about 45.5%). This is consistent with the documented use of national-level values applied across districts.
- Soil pH has only 65 unique values; 6.80 appears 52,166 times (about 26.3%). This is consistent with a derived or assigned pH variable rather than independent measurements for every record.
- Nitrogen, Phosphorus, Potassium, and Fertilizer contain zero-valued records (approximately 0.72%, 0.81%, 2.97%, and 0.70% of observations, respectively). These could reflect genuine zeros or data-construction conventions; the table alone cannot identify their cause.
- Yield has 87,809 distinct values, but 1,000 kg/ha appears 8,718 times (about 4.4%). Repetition could reflect rounding or reporting conventions and does not by itself prove an error.
- Temperature, Rainfall, and Humidity have many distinct values, but uniqueness does not establish that every year and district has independently observed weather data.
Our approach: We do not automatically delete records with repeated values or replace zero values. We document these patterns and assess their impact during modeling.
6. Temporal, Crop, and Seasonal Coverage
Annual record counts
The number of observations varies across the 1966–2017 period. The chart shows an increase from roughly 3,100–3,400 records per year in the earliest years to approximately 3,600–3,800 in much of the 1970s and 1980s. A noticeable increase appears around 1989–1990, with counts above 4,100 in some years. 2017 has a sharp drop to roughly 3,000 records.

Such changes can indicate shifts in source coverage, district/crop inclusion, or dataset construction. They are record counts, not measures of yield or national production. We account for the 2017 change when evaluating chronological model performance.
Crop distribution
The 21 crops are unequally represented. Rice has 14,476 records, while Safflower has 2,290. More frequent crops may provide more opportunities for models to learn reliable patterns, whereas low-sample crops may have less stable performance estimates.
Seasonal distribution
Approximately 54.6% of records are Kharif, 29.5% are Rabi, and 15.8% are Whole Year. Because the dataset assigns Season by Crop, these percentages primarily describe the crop mix, not independent seasonal productivity.

Modeling implication: We assess performance separately by crop and across years, and check whether crop/region composition changes between training and later evaluation periods.
7. Negative Temperature Investigation
The dataset contains 384 records (approximately 0.19%) with temperatures below 0°C, ranging from −2.84°C to −0.09°C. They occur in Chamoli and Uttar Kashi, Uttarakhand. The notebook lists crops including Finger Millet, Barley, Maize, Rapeseed & Mustard, Rice, and Soybean among these records.

Sub-zero temperatures are geographically plausible in Himalayan districts, so we do not automatically treat these observations as errors. We nevertheless interpret them cautiously because the temperature values may not reflect conditions over each crop's precise growing period.
8. Fertilizer and Nutrient Redundancy
The audit checked whether Fertilizer ≈ Nitrogen + Phosphorus + Potassium.
- 169,546 records (85.47%) have an absolute difference below 0.01 kg/ha.
- All 198,369 records (100.00%) have an absolute difference below 0.25 kg/ha.
- The maximum absolute discrepancy is 0.21 kg/ha.
Thus, total Fertilizer is almost completely determined by N, P, and K in this compiled dataset. The slight discrepancies may be due to rounding or construction conventions.

This represents near-deterministic predictor redundancy (multicollinearity). It can make linear-model coefficient interpretation unstable; correlated features may also complicate importance interpretation in tree-based models.

Our modeling plan: We retain the dataset columns and compare NPK-only, total-Fertilizer-only, and all-feature configurations using chronological validation.
9. Pesticide Data Investigation
The Pesticide column contains only 16 distinct values across 198,369 records. The maximum number of distinct values within any single year is one: all district/crop observations in the same year have identical Pesticide values.

Selected benchmark values from the notebook (kg/ha):
Year	Pesticide
1966	0.44
1975	0.44
1985	0.44
1995	0.36
2005	0.21
2015	0.24


We interpret this as evidence that Pesticide is a national-level annual aggregate assigned to district records, with historical backfilling. It cannot capture district-, crop-, or farm-level pesticide-use differences within a year.

The variable may behave as a proxy for historical time trends rather than a localized management input. It is not necessarily target leakage on its own, but any apparent predictive value must be interpreted cautiously.

Our modeling plan: We compare models with and without Pesticide. We do not interpret its coefficient or feature importance as a causal effect of district-level pesticide use, and we do not present it as a district-specific input in our prediction app.
10. Crop-Wise Yield Distributions
The typical yield varies greatly across crops. Selected median yields (kg/ha):
Crop	Median yield	Maximum yield
Sugarcane	5,200.00	22,062.30
Wheat	1,555.98	5,541.52
Rice	1,433.62	5,653.83
Maize	1,302.43	21,428.57
Chickpea	674.60	58,363.64
Minor Pulses	451.16	18,888.89
Cotton	212.50	5,000.00


Sugarcane's median yield is approximately 24.5 times Cotton's median. Crop identity and crop-specific yield scales therefore matter substantially. We therefore use crop-wise metrics alongside pooled metrics to avoid overlooking poor results on lower-yield crops.

Several crops have exceptionally high maximum-to-median ratios, including Chickpea (~86.5×), Minor Pulses (~41.9×), and Maize (~16.5×). We flag these extremes for analysis, but do not assume that an extreme value is incorrect.

Differences between means and medians (e.g., Maize mean 1,611.20 kg/ha versus median 1,302.43 kg/ha) are consistent with right-skewed distributions.

Our modeling plan: We begin with a global model that includes Crop, evaluate errors crop by crop, and compare raw and appropriately transformed yield targets using chronological validation.
11. Extreme Chickpea Yield Investigation
Among 13,473 Chickpea observations, only two records exceed the exploratory threshold of 5,000 kg/ha:
Year	Region	Season	Temperature (°C)	Rainfall (mm)	Fertilizer (kg/ha)	Yield (kg/ha)
2007	Muzaffarpur, Bihar	Rabi	25.23	2,624.8	145.34	58,363.64
2007	Saharsa, Bihar	Rabi	24.97	1,346.1	68.42	32,000.00


The Chickpea median is 674.60 kg/ha, and the 95th percentile is 1,321.33 kg/ha. Muzaffarpur's recorded yield is about 86.5× the median; Saharsa's is about 47.4×.

Both observations are exceptionally high relative to the historical distribution. Possible explanations include issues with production figures, harvested area, units, or data compilation; we have not verified a specific cause.

The 5,000 kg/ha threshold is exploratory, not a proven agronomic boundary. Both observations fall in the proposed training period (1966–2011).

Our approach: We flag these as suspected anomalies, preserve the raw CSV, and later compare training strategies with and without individually justified exclusions. We do not remove observations from validation or test data.
12. Main Dataset Limitations
The supplied dataset has several limitations relevant to interpretation and prediction:
1. Already processed data: We recognize that no nulls or duplicates in the compiled CSV does not mean that the data was never cleaned or backfilled.
2. Climate reconstruction: Some historical climate values were filled or reconstructed, so we interpret early-period weather patterns with caution.
3. Pesticide resolution: National annual values are assigned across districts and do not measure local use.
4. Derived soil measures: Repetition in pH is consistent with derived or assigned soil information rather than independent measurements at each observation.
5. Crop–Season dependency: Season may add little information beyond Crop in this dataset.
6. Fertilizer redundancy: Total Fertilizer nearly equals the sum of N, P, and K.
7. Unequal crop scales and sample sizes: These can distort pooled model comparisons.
8. Suspicious yield extremes: We flag unusually large yields as potential anomalies and test justified handling choices during model development.
9. Historical endpoint: Our dataset ends in 2017, so we describe later-year predictions carefully. Predictions based on assumed weather and management inputs are scenario-based estimates, not verified pre-season forecasts.
13. Implications for the Next Stages
Based on these findings, we follow the practices below while keeping the dataset unchanged:
- We split chronologically before fitting learned preprocessing or outlier treatments: training 1966–2011, validation 2012–2014, test 2015–2017.
- We flag crop-specific extreme values and examine their context before considering any training-only exclusions.
- We retain a no-feature-selection baseline when comparing selection methods.
- We compare feature variants (with/without Season, NPK-only versus total-Fertilizer-only, and with/without Pesticide) rather than permanently deleting columns.
- We fit scalers, encoders, selectors, and data-derived thresholds only on training data or within training folds.
- We compare models and raw versus transformed yield targets using validation data, keeping the final test period isolated until model selection is complete.
- We report MAE, RMSE, and R², including crop-wise errors and, where appropriate, results by year and region.
- We distinguish predictions based on assumed future conditions from genuine advance forecasts.
14. Conclusion
The compiled dataset covers 198,369 observations, 21 crops, 309 regions, and 1966–2017. The current audit found no detected missing values or duplicate records in the supplied CSV, but identified meaningful limitations: repeated or derived predictors, national-level pesticide backfilling, near-deterministic Fertilizer–NPK redundancy, different yield scales across crops, uneven sample representation, and two exceptionally high Chickpea observations in Bihar in 2007.

We consider this dataset suitable for controlled modeling experiments, while recognizing its feature-construction limits, potential anomalies, and the need for careful evaluation. We keep the CSV unchanged and test alternative, reproducible modeling strategies.