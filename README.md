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

## 📁 Directory Structure

```
example-datasets/
├── README.md                    ← This file
├── scripts/
│   ├── breast-cancer-survival.py
│   ├── flchain.py
│   ├── config.yml              ← Points to project data directory
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

---

## 🚀 Quick Start

1. **Set up configuration** (if not already done):
   ```bash
   cd scripts
   cp config-template.yml config.yml
   # Edit config.yml to point to your project directory
   ```

2. **Download breast cancer dataset**:
   ```bash
   python breast-cancer-survival.py
   ```

3. **Download FLChain dataset**:
   ```bash
   python flchain.py
   ```

4. **Use data in ML pipeline**:
   ```bash
   cd ../../ml-pipeline
   python ml_pipeline.py
   ```

---

## 📊 Dataset Details

### Breast Cancer Survival
- **Source**: scikit-survival German breast cancer dataset
- **Samples**: 198
- **Features**: 80 (4 clinical + 76 gene expression)
- **Target**: Binary event (recurrence/death)
- **Class balance**: Imbalanced (recommendation: use stratified CV)

### FLChain
- **Source**: scikit-survival FLChain dataset
- **Samples**: 7,874
- **Features**: 9
- **Target**: Binary event (death)
- **Class balance**: Imbalanced

---

## 🔧 Configuration

Edit `scripts/config.yml` to set the output directory:

```yaml
default:
  project: /path/to/ml-pipeline  # Where datasets will be saved
```

Datasets are saved to: `{project}/data/`

---

## 💾 Output Files

After running the scripts, you'll get:

**Data Files:**
- `breast_cancer_survival.csv` - Original clean dataset
- `breast_cancer_survival_with_missingness.csv` - Dataset with 15% missing age, 1% in 2 random features
- `flchain_survival.csv` - Original clean dataset
- `flchain_survival_with_missingness.csv` - Dataset with 15% missing age, 1% in 1 random feature

**Report Files:**
- `breast_cancer_survival_missingness_summary.csv` - Missingness statistics
- `flchain_survival_missingness_summary.csv` - Missingness statistics

---

## 📝 Notes

- All scripts use `np.random.seed(42)` for reproducible missing data patterns
- Missing data is generated using Bernoulli distributions (bernoulli missing completely at random)
- Each time you run the script, missing values will be in the same locations (reproducible)
- Config file uses YAML format and must be present in scripts/ directory