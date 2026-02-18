import pandas as pd
import yaml
import os
import numpy as np
from sksurv.datasets import load_flchain

# Read config.yml to get project path
config_path = "config.yml"
with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

project_path = config['default']['project']

# Load data
X, y = load_flchain()

# Convert y (structured array) into a DataFrame
y_df = pd.DataFrame(y)

# Combine X and y into one DataFrame
df = pd.concat([y_df, pd.DataFrame(X, columns=X.columns)], axis=1)

# Save to CSV using project path
output_path = os.path.join(project_path, "data", "flchain_survival.csv")
df.to_csv(output_path, index=False)

# Generate dataset with reproducible missing data pattern
np.random.seed(42)

# Create a copy for the missing data version
df_missing = df.copy()

# Track missingness assignments
missing_assignments = {}

# Get predictor columns (all except 'event' and 'time')
predictor_cols = [col for col in df_missing.columns if col not in ['event', 'time']]

# 1. Age missing: bernoulli(p=0.15)
if 'age' in predictor_cols:
    missing_mask_age = np.random.binomial(1, 0.15, size=len(df_missing)) == 1
    df_missing.loc[missing_mask_age, 'age'] = np.nan
    missing_assignments['age'] = 0.15

# 2. Select 1 random predictor variable for p=0.01 missing
other_predictors = [col for col in predictor_cols if col != 'age']
selected_p01 = np.random.choice(other_predictors, size=1, replace=False)
for col in selected_p01:
    missing_mask = np.random.binomial(1, 0.01, size=len(df_missing)) == 1
    df_missing.loc[missing_mask, col] = np.nan
    missing_assignments[col] = 0.01

# 3. Select 1 random predictor variable for p=0.4 missing
remaining_predictors = [col for col in other_predictors if col not in selected_p01]
selected_p40 = np.random.choice(remaining_predictors, size=1)
missing_mask = np.random.binomial(1, 0.4, size=len(df_missing)) == 1
df_missing.loc[missing_mask, selected_p40[0]] = np.nan
missing_assignments[selected_p40[0]] = 0.4

# Save the missing data version
output_path_missing = os.path.join(project_path, "data", "flchain_survival_with_missingness.csv")
df_missing.to_csv(output_path_missing, index=False)

# Generate missingness summary
missingness_data = []

# Calculate actual missingness for all columns
for col in df_missing.columns:
    n_missing = df_missing[col].isna().sum()
    pct_missing = (n_missing / len(df_missing)) * 100
    intended_p = missing_assignments.get(col, '')
    missingness_data.append({
        'variable': col,
        'intended_p': intended_p,
        'n_missing': int(n_missing),
        'pct_missing': round(pct_missing, 2)
    })

# Create DataFrame and save to CSV
missingness_df = pd.DataFrame(missingness_data)
summary_path = os.path.join(project_path, "reports", "flchain_survival_missingness_summary.csv")
missingness_df.to_csv(summary_path, index=False)

print(f"Missingness summary saved to {summary_path}")
