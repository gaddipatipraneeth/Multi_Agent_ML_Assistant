# Feature Engineering Report

## Status: SUCCESS
## Iteration: 0

## Generated Code
```python
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# SCAFFOLD — do not modify this section
df = pd.read_csv('/home/user/cleaned_data.csv')
print(f"Loaded cleaned_data.csv: {df.shape}")

TARGET_COL = 'diagnosis'
assert TARGET_COL in df.columns, f"ERROR: target '{TARGET_COL}' missing from cleaned data"

# Split BEFORE any feature work — prevents target leakage
X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL].copy()

# Column-type lists built from X (target excluded by construction — NEVER use df.columns here)
numeric_cols = [c for c in X.columns if X[c].dtype != 'object']
categorical_cols = [c for c in X.columns if X[c].dtype == 'object']

# Profiler's strategy list — already resolved, just use it
feature_strategies = ["log_transform: ['mean area', 'mean compactness', 'mean concavity', 'mean concave points', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst perimeter', 'worst area', 'worst compactness', 'worst concavity', 'worst symmetry', 'worst fractal dimension']", 'create_interaction_terms_for_top_correlated_features', 'bin_skewed_continuous_features']

print(f"Input: {X.shape[1]} features | {len(numeric_cols)} numeric | {len(categorical_cols)} categorical")

# ══ BEGIN YOUR FEATURE ENGINEERING CODE ════════════════════════════════════════════

# Hardcoded variables
skewed_columns    = ['mean area', 'mean compactness', 'mean concavity', 'mean concave points', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst perimeter', 'worst area', 'worst compactness', 'worst concavity', 'worst symmetry', 'worst fractal dimension']
datetime_columns  = []
text_columns      = []
top_correlations = {'worst concave points': -0.794, 'worst perimeter': -0.783, 'mean concave points': -0.777, 'worst radius': -0.776, 'mean perimeter': -0.743}

# STEP 1: CAST y TO NUMERIC FOR CORRELATION COMPUTATIONS
y_numeric = pd.to_numeric(y, errors='coerce')

# STEP 2: REMOVE MULTICOLLINEAR FEATURES
if len(numeric_cols) > 1:
    corr_matrix = X[numeric_cols].corr().abs()
    dropped_multi = []
    for i, col in enumerate(numeric_cols):
        if col in dropped_multi or col not in X.columns:
            continue
        for other in numeric_cols[i+1:]:
            if other in dropped_multi or other not in X.columns:
                continue
            corr_val = float(corr_matrix.loc[col, other])
            if corr_val > 0.95:
                if col in X.columns and other in X.columns:
                    col_target_corr = abs(float(X[col].corr(y_numeric)))
                    other_target_corr = abs(float(X[other].corr(y_numeric)))
                    to_drop = col if col_target_corr < other_target_corr else other
                    X.drop(columns=[to_drop], inplace=True)
                    dropped_multi.append(to_drop)
                    print(f"DROPPED (multicollinearity): {to_drop} — corr with {col if to_drop == other else other} = {corr_val:.3f}")
    numeric_cols = [c for c in numeric_cols if c in X.columns]

# STEP 3: LOG-TRANSFORM SKEWED FEATURES
if 'log_transform' in feature_strategies:
    for col in skewed_columns:
        if col in X.columns and X[col].dtype.kind in ('i', 'f') and X[col].min() >= 0:
            actual_skew = float(X[col].skew())
            if actual_skew > 1.0:
                X[col] = np.log1p(X[col])
                print(f"LOG1P: {col} (skew={actual_skew:.2f})")

# STEP 4: CREATE MISSING INDICATOR FLAGS
if 'create_missing_indicator_flags_for_high_null_columns' in feature_strategies:
    for col in numeric_cols:
        flag_col = col + '_was_missing'
        if flag_col not in X.columns:
            X[flag_col] = 0  # already imputed — flag documents origin
            print(f"MISSING FLAG: created {flag_col}")

# STEP 5: INTERACTION TERMS
if 'create_interaction_terms_for_top_correlated_features' in feature_strategies:
    corr_with_target = {}
    for col in numeric_cols:
        if col in X.columns:
            corr_with_target[col] = abs(float(X[col].corr(y_numeric)))
    top_features = sorted(corr_with_target, key=corr_with_target.get, reverse=True)
    top_features = [f for f in top_features if corr_with_target.get(f, 0) > 0.2][:3]
    for i, col1 in enumerate(top_features):
        for col2 in top_features[i+1:]:
            if col1 in X.columns and col2 in X.columns:
                feat_name = f"{col1}_x_{col2}"
                X[feat_name] = X[col1] * X[col2]
                new_corr = float(X[feat_name].corr(y_numeric))
                print(f"INTERACTION: {feat_name} — target corr={new_corr:.3f}")

# STEP 6: POLYNOMIAL FEATURES
if 'polynomial_features' in feature_strategies or len([c for c in feature_strategies if 'poly' in c.lower()]) > 0:
    from sklearn.preprocessing import PolynomialFeatures
    corr_ranked = sorted(
        [(col, abs(float(X[col].corr(y_numeric)))) for col in numeric_cols if col in X.columns],
        key=lambda x: x[1], reverse=True
    )
    poly_candidates = [col for col, _ in corr_ranked[:3]]
    if len(poly_candidates) >= 2:
        poly = PolynomialFeatures(degree=2, include_bias=False)
        poly_data = poly.fit_transform(X[poly_candidates])
        poly_names = poly.get_feature_names_out(poly_candidates)
        new_cols = [name for name in poly_names if name not in X.columns and '^' in name or ' ' in name]
        for j, name in enumerate(poly_names):
            clean_name = name.replace(' ', '_x_').replace('^', '_sq')
            if clean_name not in X.columns and ('^' in name or ' ' in name):
                X[clean_name] = poly_data[:, j]
                print(f"POLY FEATURE: {clean_name}")

# STEP 7: BINNING
if 'bin_skewed_continuous_features' in feature_strategies:
    for col in skewed_columns:
        if col in X.columns and X[col].dtype.kind in ('i', 'f'):
            actual_skew = float(X[col].skew())
            if actual_skew > 2.0:
                bin_col = col + '_bin'
                X[bin_col] = pd.qcut(X[col], q=5, labels=False, duplicates='drop')
                print(f"BIN: {bin_col} (skew={actual_skew:.2f}, q=5)")

# STEP 8: DOMAIN-AWARE FEATURES
# No specific domain-aware features are defined for this problem

# STEP 9: FREQUENCY ENCODE REMAINING HIGH-CARDINALITY OBJECT COLUMNS
for col in categorical_cols:
    if X[col].nunique() > 10:
        X[col] = X[col].map(X[col].value_counts() / len(X))
        print(f"FREQ ENCODE: {col}")

# STEP 10: VALIDATE AND REPORT
print(f"FEATURES BEFORE: {len(numeric_cols)} numeric + {len(categorical_cols)} categorical = {X.shape[1] - len(X.columns)} original")
print(f"FEATURES AFTER: {X.shape[1]} total")
new_features = [col for col in X.columns if col not in numeric_cols and col not in categorical_cols]
print(f"NEW FEATURES CREATED: {new_features}")
for new_feat in new_features:
    if new_feat in X.columns:
        corr_val = float(X[new_feat].corr(y_numeric))
        print(f"  {new_feat}: target_corr={corr_val:.3f}")

# IMBALANCE NOTE
imbalance_ratio = 0.59
if imbalance_ratio < 0.3:
    print("NOTE: imbalanced dataset — SMOTE will be applied in modeling")

# ══ END YOUR FEATURE ENGINEERING CODE ══════════════════════════════════════════════

# SCAFFOLD — validate & save
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.median(numeric_only=True))

assert TARGET_COL not in X.columns, f"LEAKAGE: '{TARGET_COL}' ended up in feature matrix!"
_nulls = X.isnull().sum().sum()
assert _nulls == 0, f"{_nulls} null values remain after feature engineering"
_infs = np.isinf(X.select_dtypes(include='number').values).sum()
assert _infs == 0, f"{_infs} infinite values remain"

result_df = X.copy()
result_df[TARGET_COL] = y.values
result_df.to_csv('/home/user/featured_data.csv', index=False)
_new = max(0, X.shape[1] - 30)
print(f"SAVED: featured_data.csv — shape {result_df.shape} — {_new} new features added")

```

## Execution Output
```
Loaded cleaned_data.csv: (568, 31)
Input: 30 features | 30 numeric | 0 categorical
DROPPED (multicollinearity): mean concavity — corr with mean concave points = 0.978
DROPPED (multicollinearity): concavity error — corr with mean concave points = 0.976
DROPPED (multicollinearity): concave points error — corr with mean concave points = 0.960
DROPPED (multicollinearity): worst concavity — corr with mean concave points = 0.978
BIN: mean area_bin (skew=2.60, q=5)
BIN: mean compactness_bin (skew=2.57, q=5)
BIN: mean concave points_bin (skew=6.21, q=5)
BIN: radius error_bin (skew=2.76, q=5)
BIN: texture error_bin (skew=2.28, q=5)
BIN: perimeter error_bin (skew=2.30, q=5)
BIN: area error_bin (skew=2.69, q=5)
BIN: smoothness error_bin (skew=3.17, q=5)
BIN: compactness error_bin (skew=3.48, q=5)
BIN: fractal dimension error_bin (skew=3.00, q=5)
BIN: worst perimeter_bin (skew=2.01, q=5)
BIN: worst area_bin (skew=2.92, q=5)
BIN: worst compactness_bin (skew=2.15, q=5)
BIN: worst fractal dimension_bin (skew=2.38, q=5)
FEATURES BEFORE: 26 numeric + 0 categorical = 0 original
FEATURES AFTER: 40 total
NEW FEATURES CREATED: ['mean area_bin', 'mean compactness_bin', 'mean concave points_bin', 'radius error_bin', 'texture error_bin', 'perimeter error_bin', 'area error_bin', 'smoothness error_bin', 'compactness error_bin', 'fractal dimension error_bin', 'worst perimeter_bin', 'worst area_bin', 'worst compactness_bin', 'worst fractal dimension_bin']
  mean area_bin: target_corr=nan
  mean compactness_bin: target_corr=nan
  mean concave points_bin: target_corr=nan
  radius error_bin: target_corr=nan
  texture error_bin: target_corr=nan
  perimeter error_bin: target_corr=nan
  area error_bin: target_corr=nan
  smoothness error_bin: target_corr=nan
  compactness error_bin: target_corr=nan
  fractal dimension error_bin: target_corr=nan
  worst perimeter_bin: target_corr=nan
  worst area_bin: target_corr=nan
  worst compactness_bin: target_corr=nan
  worst fractal dimension_bin: target_corr=nan
SAVED: featured_data.csv — shape (568, 41) — 10 new features added
```
