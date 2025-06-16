import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor, ExtraTreesRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle

# Loading dataset
df = pd.read_csv('flexible_tasks_dataset.csv')

df['deadline_dt'] = pd.to_datetime(df['deadline'], format='%Y-%m-%d %H:%M')
now = datetime.now()
df['hours_left'] = (df['deadline_dt'] - now).dt.total_seconds() / 3600
df['days_remaining'] = np.ceil(df['hours_left'] / 24).astype(int)

features = ['duration', 'priority', 'hours_left', 'days_remaining', 'task']
target = 'allocated_hours'
X = df[features].copy()
y = df[target]

# Encoding categorical task
le = LabelEncoder()
X['task_enc'] = le.fit_transform(X['task'])
X = X.drop(columns=['task'])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling features
numeric_feats = ['duration', 'priority', 'hours_left', 'days_remaining']
scaler = StandardScaler()
X_train[numeric_feats] = scaler.fit_transform(X_train[numeric_feats])
X_test[numeric_feats]  = scaler.transform(X_test[numeric_feats])

# Creating a list of Regression Models
models = [
    ('RandomForest', RandomForestRegressor(n_estimators=100, random_state=42)),
    ('ExtraTrees', ExtraTreesRegressor(n_estimators=100, random_state=42)),
    ('GradientBoost', GradientBoostingRegressor(n_estimators=100, random_state=42)),
    ('AdaBoost', AdaBoostRegressor(n_estimators=100, random_state=42)),
    ('Ridge', Ridge()),
    ('Lasso', Lasso()),
    ('SVR', SVR())
]

# Training and evaluating each model
results = []
for name, mod in models:
    mod.fit(X_train, y_train)
    y_pred = mod.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2  = r2_score(y_test, y_pred)
    print(f"{name} -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
    results.append((name, mae, rmse, r2))

# Saving the best model using pickle
best = min(results, key=lambda x: x[1])  # lowest error
best_name = best[0]
best_model = dict(models)[best_name]

# Building Pipeline
to_save = {
    'model': best_model,
    'scaler': scaler,
    'encoder': le
}

with open('alloc_hours_model.pkl', 'wb') as f:
    pickle.dump(to_save, f)
