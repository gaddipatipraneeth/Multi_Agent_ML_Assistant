# Data Cleaning Report

## Status: SUCCESS

## Generated Code
```python
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# SCAFFOLD — do not modify this section
df = pd.read_csv('/home/user/breast_cancer.csv')
print(f"Loaded: {df.shape[0]} rows x {df.shape[1]} cols")
target_col = 'diagnosis'

# ══ BEGIN YOUR CLEANING CODE ════════════════════════════════════════════

# STEP 2: DROP USELESS COLUMNS
id_columns = []
constant_columns = []
cols_before = df.shape[1]
for col in df.columns.tolist():
    if col == target_col:
        continue
    null_pct = df[col].isnull().mean()
    n_unique = df[col].nunique()
    if 'id' in col.lower() and n_unique > 0.95 * len(df):
        df.drop(columns=[col], inplace=True)
        print(f"DROPPED (ID column): {col} — {n_unique} unique values")
    elif null_pct > 0.60:
        df.drop(columns=[col], inplace=True)
        print(f"DROPPED (>{60}% missing): {col} — {null_pct:.1%} null")
    elif n_unique <= 1:
        df.drop(columns=[col], inplace=True)
        print(f"DROPPED (zero variance): {col}")
print(f"COLUMNS: {cols_before} → {df.shape[1]} (dropped {cols_before - df.shape[1]})")

# STEP 3: HANDLE MISSING VALUES
numeric_cols = ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension']
for col in numeric_cols:
    null_pct = df[col].isnull().mean()
    if null_pct > 0:
        if null_pct < 0.05:
            df[col].fillna(df[col].median(), inplace=True)
            print(f"IMPUTATION: {col} — median ({null_pct:.1%} missing)")
        elif null_pct <= 0.20:
            df[col + '_was_missing'] = df[col].isnull().astype(int)
            df[col].fillna(df[col].median(), inplace=True)
            print(f"IMPUTATION: {col} — median + indicator ({null_pct:.1%} missing)")
        else:
            df.drop(columns=[col], inplace=True)
            print(f"DROPPED (>20% missing numeric): {col} — {null_pct:.1%} null")

# STEP 4: DATA TYPE FIXES
for col in df.columns:
    if df[col].dtype == object:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"TYPE FIX: {col} → numeric")
        except:
            pass

# STEP 5: CATEGORICAL ENCODING
encoding_map = {}
for col in df.columns:
    if col not in encoding_map and col != target_col:
        if df[col].nunique() > 15:
            df[col] = df[col].map(df[col].value_counts() / len(df))
            print(f"TEXT FREQ ENCODE: {col}")
        else:
            df = pd.get_dummies(df, columns=[col], drop_first=True)

# STEP 6: TARGET ENCODING
unique_vals = df[target_col].unique()
sorted_vals = sorted([str(v).strip() for v in unique_vals])
mapping = {v: i for i, v in enumerate(sorted_vals)}
df[target_col] = df[target_col].astype(str).str.strip().map(mapping)
print(f"TARGET ENCODED: {mapping}")
print(f"TARGET ENCODED: unique={sorted(df[target_col].unique().tolist())}, dtype={df[target_col].dtype}")

# STEP 7: LOG1P TRANSFORM
skewed_columns = ['mean area', 'mean compactness', 'mean concavity', 'mean concave points', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst perimeter', 'worst area', 'worst compactness', 'worst concavity', 'worst symmetry', 'worst fractal dimension']
for col in skewed_columns:
    if col in df.columns and col != target_col and df[col].dtype.kind in ('i', 'f'):
        if df[col].min() >= 0:
            df[col] = np.log1p(df[col])
            print(f"LOG1P: applied to {col}")

# STEP 8: OUTLIER CLIPPING
for col in df.columns:
    if df[col].dtype.kind in ('i', 'f') and col != target_col:
        q1 = df[col].quantile(0.01)
        q3 = df[col].quantile(0.99)
        n = ((df[col] < q1) | (df[col] > q3)).sum()
        if n > 0:
            df[col] = df[col].clip(lower=q1, upper=q3)
            print(f"OUTLIERS: {col} — clipped {n} values to [{float(q1):.3f}, {float(q3):.3f}]")

# STEP 9: DROP DUPLICATES
before = len(df)
df.drop_duplicates(inplace=True)
if len(df) < before:
    print(f"DUPLICATES: removed {before - len(df)} rows")

# STEP 10: DROP REDUNDANT ENCODED COLUMNS
# No redundant encoded columns in this dataset

# STEP 11: PRINT SUMMARY
print(f"CLEANING SUMMARY: shape={df.shape}, nulls_remaining={df.isnull().sum().sum()}")
print(f"TARGET COLUMN: {target_col} — unique: {sorted(df[target_col].unique().tolist())}, dtype: {df[target_col].dtype}")
print(f"FINAL COLUMNS: {df.columns.tolist()}")

# ══ END YOUR CLEANING CODE ══════════════════════════════════════════════

# SCAFFOLD — final validation & save
df.fillna(df.median(numeric_only=True), inplace=True)
for _col in df.select_dtypes(include='object').columns:
    if _col != target_col:
        _mode = df[_col].mode()
        df[_col].fillna(_mode.iloc[0] if not _mode.empty else 'unknown', inplace=True)

_bool_cols = df.select_dtypes(include='bool').columns.tolist()
if _bool_cols:
    df[_bool_cols] = df[_bool_cols].astype('int8')
    print(f"BOOL→INT8: converted {len(_bool_cols)} boolean columns")

_remaining_nulls = df.isnull().sum().sum()
if _remaining_nulls > 0:
    print(f"WARNING: {_remaining_nulls} nulls remain — force-filling with 0")
    df.fillna(0, inplace=True)

print(f"FINAL SHAPE: {df.shape}")
print(f"TARGET COLUMN: {target_col} — unique: {sorted(df[target_col].unique().tolist())}, dtype: {df[target_col].dtype}")
df.to_csv('/home/user/cleaned_data.csv', index=False)
print(f"SAVED: cleaned_data.csv — shape {df.shape}")

```

## Execution Output
```
Loaded: 569 rows x 31 cols
COLUMNS: 31 → 31 (dropped 0)
TEXT FREQ ENCODE: mean radius
TEXT FREQ ENCODE: mean texture
TEXT FREQ ENCODE: mean perimeter
TEXT FREQ ENCODE: mean area
TEXT FREQ ENCODE: mean smoothness
TEXT FREQ ENCODE: mean compactness
TEXT FREQ ENCODE: mean concavity
TEXT FREQ ENCODE: mean concave points
TEXT FREQ ENCODE: mean symmetry
TEXT FREQ ENCODE: mean fractal dimension
TEXT FREQ ENCODE: radius error
TEXT FREQ ENCODE: texture error
TEXT FREQ ENCODE: perimeter error
TEXT FREQ ENCODE: area error
TEXT FREQ ENCODE: smoothness error
TEXT FREQ ENCODE: compactness error
TEXT FREQ ENCODE: concavity error
TEXT FREQ ENCODE: concave points error
TEXT FREQ ENCODE: symmetry error
TEXT FREQ ENCODE: fractal dimension error
TEXT FREQ ENCODE: worst radius
TEXT FREQ ENCODE: worst texture
TEXT FREQ ENCODE: worst perimeter
TEXT FREQ ENCODE: worst area
TEXT FREQ ENCODE: worst smoothness
TEXT FREQ ENCODE: worst compactness
TEXT FREQ ENCODE: worst concavity
TEXT FREQ ENCODE: worst concave points
TEXT FREQ ENCODE: worst symmetry
TEXT FREQ ENCODE: worst fractal dimension
TARGET ENCODED: {'0': 0, '1': 1}
TARGET ENCODED: unique=[0, 1], dtype=int64
LOG1P: applied to mean area
LOG1P: applied to mean compactness
LOG1P: applied to mean concavity
LOG1P: applied to mean concave points
LOG1P: applied to mean fractal dimension
LOG1P: applied to radius error
LOG1P: applied to texture error
LOG1P: applied to perimeter error
LOG1P: applied to area error
LOG1P: applied to smoothness error
LOG1P: applied to compactness error
LOG1P: applied to concavity error
LOG1P: applied to concave points error
LOG1P: applied to symmetry error
LOG1P: applied to fractal dimension error
LOG1P: applied to worst radius
LOG1P: applied to worst perimeter
LOG1P: applied to worst area
LOG1P: applied to worst compactness
LOG1P: applied to worst concavity
LOG1P: applied to worst symmetry
LOG1P: applied to worst fractal dimension
OUTLIERS: mean radius — clipped 4 values to [0.002, 0.005]
OUTLIERS: mean area — clipped 3 values to [0.002, 0.004]
OUTLIERS: mean smoothness — clipped 5 values to [0.002, 0.007]
OUTLIERS: mean compactness — clipped 6 values to [0.002, 0.004]
OUTLIERS: radius error — clipped 6 values to [0.002, 0.004]
OUTLIERS: perimeter error — clipped 4 values to [0.002, 0.004]
OUTLIERS: symmetry error — clipped 4 values to [0.002, 0.005]
OUTLIERS: worst radius — clipped 5 values to [0.002, 0.007]
OUTLIERS: worst texture — clipped 6 values to [0.002, 0.004]
OUTLIERS: worst compactness — clipped 6 values to [0.002, 0.004]
OUTLIERS: worst fractal dimension — clipped 3 values to [0.002, 0.004]
DUPLICATES: removed 1 rows
CLEANING SUMMARY: shape=(568, 31), nulls_remaining=0
TARGET COLUMN: diagnosis — unique: [0, 1], dtype: int64
FINAL COLUMNS: ['mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness', 'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension', 'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error', 'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error', 'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness', 'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension', 'diagnosis']
FINAL SHAPE: (568, 31)
TARGET COLUMN: diagnosis — unique: [0, 1], dtype: int64

SAVED: cleaned_data.csv — shape (568, 31)
```
