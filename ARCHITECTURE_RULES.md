# ML Architecture and Research Governance Rules

To preserve academic rigor, scientific reproducibility, and prevent data leakage, all development and automated agents working on this project must strictly comply with the following 13 golden rules:

1. **Notebook-First Research Workflow:** All core experimental analysis, exploratory data analysis, outlier investigations, feature engineering, feature selection experiments, model training, evaluation, and visualizations must be implemented in executable Jupyter Notebooks (`notebooks/01_*.ipynb` through `notebooks/09_*.ipynb`).
2. **Modular Python Backend Decoupling:** Reusable data loading, schema validation, preprocessing transformers, feature selectors, model wrappers, and evaluation metrics remain in decoupled Python modules under `src/` and are imported into notebooks. Never rewrite large utility functions inside notebooks.
3. **Never modify the original dataset:** The raw dataset located at `data/raw/crop_yield_dataset.csv` is strictly read-only. Cleaned or interim datasets must be versioned separately in `data/processed/`.
4. **Scikit-learn Transformer interface:** Every feature selector, preprocessor, and engineer must implement standard `fit` and `transform` methods (or adhere to `BaseEstimator` and `TransformerMixin`).
5. **Zero leakage in feature selection:** Never select features using validation or test labels. Supervised feature selection must occur strictly inside training folds during cross-validation.
6. **Feature-name preservation:** Track and save transformed feature names at every pipeline step to ensure full interpretability and seamless inference.
7. **No-feature-selection baseline:** Always preserve `NoFeatureSelection` as a mandatory baseline against which feature-selection techniques are evaluated.
8. **Configuration-driven experimentation:** All model hyperparameters, data partitions, feature lists, and preprocessing flags must be defined in YAML/JSON configs, not hardcoded.
9. **Append-only experiment tracking:** Never overwrite previous experiment results. Each experiment must have a unique identifier, timestamp, and saved metrics JSON/CSV.
10. **Strict holdout isolation:** Never use the final held-out test set (2015–2017) for feature selection, hyperparameter tuning, or model selection decisions. Model selection is strictly driven by the validation set (2012–2014) or temporal CV.
11. **Phase-by-phase implementation:** Never silently implement future phases without explicit instruction and approval. Complete the requested phase, test, document, and pause.
12. **Strict chronological isolation:** Maintain chronological data partitions (Train: 1966–2011, Validation: 2012–2014, Test: 2015–2017) to prevent temporal target leakage.
13. **Honest scenario forecasting:** Never claim future weather or agricultural inputs are known advance values. Distinguish between known-condition yield estimation and advance pre-season forecasting.
