import pandas as pd
import yaml
import os
import numpy as np
from sksurv.datasets import load_breast_cancer

# Read config.yml to get project path
if '__file__' in globals():
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.yml')
else:
    # For interactive environments, use current working directory
    config_path = os.path.join(os.getcwd(), '..', 'config.yml')

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

project_path = config['default']['project']

# Load data
X, y = load_breast_cancer()

# Convert y (structured array) into a DataFrame
y_df = pd.DataFrame(y)

# Combine X and y into one DataFrame
df = pd.concat([y_df, pd.DataFrame(X, columns=X.columns)], axis=1)

# Save to CSV using project path
output_path = os.path.join(project_path, "data", "breast_cancer_survival.csv")
df.to_csv(output_path, index=False)

# Generate dataset with reproducible missing data pattern
np.random.seed(42)

# Create a copy for the missing data version
df_missing = df.copy()

# Get predictor columns (all except 'event' and 'time')
predictor_cols = [col for col in df_missing.columns if col not in ['event', 'time']]

# 1. Age missing: bernoulli(p=0.15)
if 'age' in predictor_cols:
    missing_mask_age = np.random.binomial(1, 0.15, size=len(df_missing)) == 1
    df_missing.loc[missing_mask_age, 'age'] = np.nan

# 2. Select 2 random predictor variables for p=0.01 missing
other_predictors = [col for col in predictor_cols if col != 'age']
selected_p01 = np.random.choice(other_predictors, size=2, replace=False)
for col in selected_p01:
    missing_mask = np.random.binomial(1, 0.01, size=len(df_missing)) == 1
    df_missing.loc[missing_mask, col] = np.nan

# 3. Select 1 random predictor variable for p=0.15 missing
remaining_predictors = [col for col in other_predictors if col not in selected_p01]
selected_p15 = np.random.choice(remaining_predictors, size=1)
missing_mask = np.random.binomial(1, 0.15, size=len(df_missing)) == 1
df_missing.loc[missing_mask, selected_p15[0]] = np.nan

# 4. Select 1 random predictor variable for p=0.4 missing
remaining_predictors = [col for col in remaining_predictors if col not in selected_p15]
selected_p40 = np.random.choice(remaining_predictors, size=1)
missing_mask = np.random.binomial(1, 0.4, size=len(df_missing)) == 1
df_missing.loc[missing_mask, selected_p40[0]] = np.nan

# Save the missing data version
output_path_missing = os.path.join(project_path, "data", "breast_cancer_survival_with_missingness.csv")
df_missing.to_csv(output_path_missing, index=False)
