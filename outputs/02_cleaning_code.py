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
