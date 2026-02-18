# Example Datasets

This directory contains scripts to download, prepare, and generate example datasets for survival analysis with controlled missingness patterns. All datasets are sourced from scikit-survival.

## 📄 Scripts Overview

### [breast-cancer-survival.py](scripts/breast-cancer-survival.py)
Loads the breast cancer survival dataset from scikit-survival and generates both clean and missingness versions.

**What it does:**
- Downloads German breast cancer dataset (198 samples × 80+ features)
- Target: Binary event indicator (recurrence/death)
- Saves clean version: `data/breast_cancer_survival.csv`
- Generates missingness version with controlled patterns: `data/breast_cancer_survival_with_missingness.csv`
  - 15% missing in `age` feature (bernoulli pattern)
  - 1% missing in 2 random features
- Creates missingness summary report: `reports/breast_cancer_survival_missingness_summary.csv`

**Run:**
```bash
cd scripts
python breast-cancer-survival.py
```

---

### [flchain.py](scripts/flchain.py)
Loads the FLChain protein dataset from scikit-survival and generates both clean and missingness versions.

**What it does:**
- Downloads FLChain dataset (7,874 samples × 9 features)
- Target: Binary event indicator (death)
- Saves clean version: `data/flchain_survival.csv`
- Generates missingness version with controlled patterns: `data/flchain_survival_with_missingness.csv`
  - 15% missing in `age` feature (bernoulli pattern)
  - 1% missing in 1 random feature
- Creates missingness summary report: `reports/flchain_survival_missingness_summary.csv`

**Run:**
```bash
cd scripts
python flchain.py
```

---

## Directory Structure

```
example-datasets/
├── README.md                    ← This file
├── scripts/
│   ├── breast-cancer-survival.py
│   ├── flchain.py
│   └── config-template.yml     ← Template (copy to config.yml)
│
├── data/
│   ├── breast_cancer_survival.csv                      ← Clean data
│   ├── breast_cancer_survival_with_missingness.csv    ← With missing values
│   ├── flchain_survival.csv                           ← Clean data
│   └── flchain_survival_with_missingness.csv          ← With missing values
│
└── reports/
    ├── breast_cancer_survival_missingness_summary.csv
    └── flchain_survival_missingness_summary.csv
```
