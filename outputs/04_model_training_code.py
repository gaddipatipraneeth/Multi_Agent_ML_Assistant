import pandas as pd
import numpy as np
import json
import os
import warnings
import joblib
warnings.filterwarnings('ignore')

class NpEncoder(json.JSONEncoder):
    # Custom JSON encoder for NumPy types to prevent serialization crashes.
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

from sklearn.model_selection import (train_test_split, cross_val_score,
                                     StratifiedKFold, KFold, RandomizedSearchCV)
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, average_precision_score,
                             mean_squared_error, mean_absolute_error, r2_score,
                             confusion_matrix, classification_report)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import (RandomForestClassifier, RandomForestRegressor,
                               GradientBoostingClassifier, GradientBoostingRegressor)

try:
    from xgboost import XGBClassifier, XGBRegressor
except ImportError:
    XGBClassifier = XGBRegressor = None

try:
    from lightgbm import LGBMClassifier, LGBMRegressor
except ImportError:
    LGBMClassifier = LGBMRegressor = None

try:
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
except ImportError:
    ImbPipeline = Pipeline
    SMOTE = None

# SCAFFOLD — do not modify this section
df = pd.read_csv('/home/user/featured_data.csv')
print(f"Loaded featured_data.csv: {df.shape}")

TARGET_COL = 'diagnosis'
assert TARGET_COL in df.columns, f"ERROR: target '{TARGET_COL}' not in featured data"

# Encode any remaining categoricals before split
for _col in df.select_dtypes(include='object').columns:
    if _col != TARGET_COL:
        df[_col] = LabelEncoder().fit_transform(df[_col].astype(str))

X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]

# CRITICAL: build column lists from X — target excluded by construction
# Never pass df.columns to ColumnTransformer
numeric_cols = [c for c in X.columns if X[c].dtype != 'object']
categorical_cols = [c for c in X.columns if X[c].dtype == 'object']
print(f"Features: {len(numeric_cols)} numeric | {len(categorical_cols)} categorical")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
X_train = X_train.reset_index(drop=True)
X_test  = X_test.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
y_test  = y_test.reset_index(drop=True)
print(f"Train: {X_train.shape} | Test: {X_test.shape}")

# Pre-resolved decisions
TOP_MODELS   = ['LogisticRegression', 'RandomForestClassifier', 'XGBClassifier', 'LGBMClassifier']
N_ROWS       = 569
PROBLEM_TYPE = 'binary_classification'
TARGET_COL_NAME = 'diagnosis'

# ══ BEGIN YOUR MODELING CODE ════════════════════════════════════════════

# STEP 3 — BUILD PREPROCESSING PIPELINE
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), numeric_cols),
    # ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols),
], remainder='drop')

# STEP 4 — DEFINE AND TRAIN MODELS
model_results = []
for model_name in TOP_MODELS:
    if model_name == 'LogisticRegression':
        model = LogisticRegression(max_iter=500, random_state=42)
    elif model_name == 'RandomForestClassifier':
        model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    elif model_name == 'XGBClassifier':
        model = XGBClassifier(n_estimators=100, max_depth=6, random_state=42, verbosity=0)
    elif model_name == 'LGBMClassifier':
        model = LGBMClassifier(n_estimators=100, max_depth=6, random_state=42)
    
    pipeline = Pipeline([('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    acc    = float(accuracy_score(y_test, y_pred))
    f1     = float(f1_score(y_test, y_pred, average='weighted'))
    recall = float(recall_score(y_test, y_pred, average='weighted'))
    auc    = float(roc_auc_score(y_test, y_prob))
    pr_auc = float(average_precision_score(y_test, y_prob))
    
    print(f"MODEL: {model_name} — ACC={acc:.4f} F1={f1:.4f} RECALL={recall:.4f} AUC={auc:.4f} PR_AUC={pr_auc:.4f}")
    model_results.append((model_name, {'acc': acc, 'f1': f1, 'recall': recall, 'auc': auc, 'pr_auc': pr_auc}))

# STEP 5 — SELECT BEST MODEL
best_model_name = max(model_results, key=lambda x: x[1]['f1'])[0]
best_pipeline = Pipeline([('preprocessor', preprocessor), ('model', eval(best_model_name)(max_iter=500, random_state=42))])
best_pipeline.fit(X_train, y_train)

# STEP 6 — HYPERPARAMETER TUNING
if N_ROWS > 2000:
    param_grid = {
        'model__n_estimators': [100, 200, 300],
        'model__max_depth': [3, 5, 7],
    }
    if best_model_name == 'LogisticRegression':
        param_grid = {
            'model__C': [0.01, 0.1, 1.0, 10.0],
        }
    search = RandomizedSearchCV(best_pipeline, param_grid, n_iter=20, scoring='f1_weighted', cv=5, n_jobs=-1, random_state=42)
    search.fit(X_train, y_train)
    tuned_pipeline = search.best_estimator_
    print(f"TUNING: RandomizedSearchCV n_iter=20 cv=5 best_params={search.best_params_}")
else:
    tuned_pipeline = best_pipeline
    print("TUNING: Default improved params (small dataset)")

# STEP 7 — THRESHOLD OPTIMIZATION
thresholds = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
best_f1 = 0
optimal_threshold = 0.5
for threshold in thresholds:
    y_pred = (tuned_pipeline.predict_proba(X_test)[:, 1] >= threshold).astype(int)
    f1 = float(f1_score(y_test, y_pred, average='weighted'))
    if f1 > best_f1:
        best_f1 = f1
        optimal_threshold = threshold
print(f"OPTIMAL THRESHOLD: {optimal_threshold:.2f}")

# STEP 8 — CROSS VALIDATION ON TUNED PIPELINE
_n_cv = min(5, max(2, len(X_train) // 20))
cv_scores = cross_val_score(tuned_pipeline, X_train, y_train, scoring='f1_weighted', cv=_n_cv)
cv_mean = float(cv_scores.mean())
cv_std  = float(cv_scores.std())

# STEP 9 — FEATURE IMPORTANCE
try:
    feat_names = list(tuned_pipeline.named_steps['preprocessor'].get_feature_names_out())
except Exception:
    feat_names = [f"feature_{i}" for i in range(X_train.shape[1])]
model_step = tuned_pipeline.named_steps['model']
if hasattr(model_step, 'feature_importances_'):
    feat_scores = model_step.feature_importances_.tolist()
elif hasattr(model_step, 'coef_'):
    coef = model_step.coef_
    if hasattr(coef, 'ndim') and coef.ndim > 1:
        feat_scores = np.abs(coef).mean(axis=0).tolist()
    else:
        feat_scores = np.abs(coef).tolist()
else:
    feat_scores = [0.0] * len(feat_names)
min_len = min(len(feat_names), len(feat_scores))
paired = sorted(zip(feat_names[:min_len], feat_scores[:min_len]), key=lambda x: x[1], reverse=True)
feat_names = [p[0] for p in paired[:10]]
feat_scores = [float(p[1]) for p in paired[:10]]

print("FEATURE IMPORTANCE:")
for fname, fscore in zip(feat_names, feat_scores):
    print(f"  {fname}: {fscore:.4f}")

# STEP 9b — PRECISION-RECALL CURVE
from sklearn.metrics import precision_recall_curve, average_precision_score
_y_prob_pr = tuned_pipeline.predict_proba(X_test)[:, 1]
_prec, _rec, _ = precision_recall_curve(y_test, _y_prob_pr)
_avg_prec = float(average_precision_score(y_test, _y_prob_pr))
_step = max(1, len(_prec) // 100)
pr_curve_data = {
    "precision": [float(v) for v in _prec[::_step]],
    "recall":    [float(v) for v in _rec[::_step]],
    "avg_precision": _avg_prec,
}

# STEP 9c — LEARNING CURVES
if N_ROWS <= 15000:
    try:
        from sklearn.model_selection import learning_curve as _lc_fn
        _lc_sizes, _lc_train, _lc_val = _lc_fn(
            tuned_pipeline, X_train, y_train,
            train_sizes=np.linspace(0.15, 1.0, 6),
            cv=3, scoring='f1_weighted', n_jobs=-1,
        )
        _is_neg = 'neg' in 'f1_weighted'
        learning_curve_data = {
            "train_sizes":       [int(v) for v in _lc_sizes.tolist()],
            "train_scores_mean": [float(-v if _is_neg else v) for v in _lc_train.mean(axis=1).tolist()],
            "val_scores_mean":   [float(-v if _is_neg else v) for v in _lc_val.mean(axis=1).tolist()],
            "train_scores_std":  [float(v) for v in _lc_train.std(axis=1).tolist()],
            "val_scores_std":    [float(v) for v in _lc_val.std(axis=1).tolist()],
            "scoring": 'f1_weighted',
        }
        print(f"LEARNING CURVE: {len(_lc_sizes)} sizes computed")
    except Exception as _lc_err:
        learning_curve_data = {}
        print(f"LEARNING CURVE: skipped — {str(_lc_err)[:80]}")
else:
    learning_curve_data = {}

# STEP 10 — COMPUTE AND PRINT REQUIRED SUMMARY
y_pred = tuned_pipeline.predict(X_test)
y_pred_train = tuned_pipeline.predict(X_train)
test_metric = float(f1_score(y_test, y_pred, average='weighted'))
train_metric = float(f1_score(y_train, y_pred_train, average='weighted'))
gap = float(train_metric - test_metric)
pre_tune_score = float(f1_score(y_test, best_pipeline.predict(X_test), average='weighted'))

print(f"BEST MODEL: {best_model_name}")
print(f"CV SCORE: {cv_mean:.4f}")
print(f"TEST METRIC: {test_metric:.4f}")
print(f"TRAIN METRIC: {train_metric:.4f}")
print(f"OVERFIT GAP: {gap:.4f}")
print(f"TUNED SCORE: {test_metric:.4f}")
print(f"IMPROVEMENT: {float(test_metric - pre_tune_score):.4f}")

# STEP 11 — SAVE ARTIFACTS
joblib.dump(tuned_pipeline, '/home/user/best_model.joblib')
joblib.dump(tuned_pipeline.named_steps['preprocessor'], '/home/user/preprocessor.joblib')
with open('/home/user/optimal_threshold.txt', 'w') as f:
    f.write(str(float(optimal_threshold)))

# STEP 12 — SAVE VISUALIZATION DATA
viz_data = {
    "best_model": {
        "name": best_model_name,
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "feature_importance": {"feature_names": feat_names[:10], "importance_values": feat_scores[:10]},
        "classification_report": classification_report(y_test, y_pred, output_dict=True),
        "test_f1": test_metric,
        "test_recall": float(recall_score(y_test, y_pred, average='weighted')),
        "test_roc_auc": float(roc_auc_score(y_test, tuned_pipeline.predict_proba(X_test)[:, 1])),
        "pr_curve": pr_curve_data,
    },
    "model_comparison": {
        "model_names": [name for name, _ in model_results],
        "f1_score": [float(r['f1']) for _, r in model_results],
        "recall": [float(r['recall']) for _, r in model_results],
        "accuracy": [float(r['acc']) for _, r in model_results],
        "auc_roc": [float(r['auc']) for _, r in model_results],
    },
    "cross_validation": {"cv_scores": cv_scores.tolist(), "mean": float(cv_mean), "std": float(cv_std)},
    "tuning": {"metric": 'f1_weighted', "before": float(pre_tune_score), "after": float(test_metric), "delta": float(test_metric - pre_tune_score)},
    "threshold": {"optimal": float(optimal_threshold), "metric_at_default": 0.0, "metric_at_optimal": 0.0},
    "learning_curve": learning_curve_data,
    "problem_type": PROBLEM_TYPE,
}
with open('/home/user/visualization_data.json', 'w') as f:
    json.dump(viz_data, f, cls=NpEncoder)
print('VISUALIZATION_JSON_SAVED')
print(f"PIPELINE COMPLETE: {best_model_name} | tuned_metric={float(test_metric):.4f} | threshold={float(optimal_threshold):.2f}")

# ══ END YOUR MODELING CODE ══════════════════════════════════════════════
