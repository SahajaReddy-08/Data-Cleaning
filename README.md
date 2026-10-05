# Data Cleaning Project

A structured and modular Python toolkit for cleaning, standardizing, and preprocessing tabular datasets.

---

## 📁 Repository Structure

```text
Data-Cleaning/
│
├── data/
│   ├── raw/                # Original, immutable datasets (e.g. CSV, Excel)
│   │   └── sample.csv      # Sample dataset for demonstration
│   └── processed/          # Cleaned, standardized datasets ready for analysis
│
├── notebooks/              # Jupyter Notebooks for exploratory data analysis (EDA)
│
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── cleaner.py          # Modular DataCleaner pipeline class
│   └── utils.py            # Data loading, inspection, and summary tools
│
├── main.py                 # Command-line entrypoint to execute cleaning pipeline
├── requirements.txt        # Required Python libraries
├── .gitignore              # Standard data science and environment ignores
└── README.md               # Project documentation
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/SahajaReddy-08/Data-Cleaning.git
cd Data-Cleaning
```

### 2. Set Up Virtual Environment (Optional but Recommended)
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Cleaning Pipeline
Run the demonstration pipeline on the sample dataset:
```bash
python main.py --input data/raw/sample.csv
```

To run on your own dataset:
```bash
python main.py --input data/raw/your_dataset.csv --output data/processed/your_cleaned_dataset.csv
```

---

## 🛠️ Features & Usage

### 1. Reusable `DataCleaner` Class (`src/cleaner.py`)
Chain cleaning operations together with a fluent API:

```python
from src.cleaner import DataCleaner
from src.utils import load_dataset

df = load_dataset("data/raw/your_dataset.csv")

cleaner = (
    DataCleaner(df)
    .clean_column_names()              # snake_case, strip unwanted characters
    .trim_whitespace()                 # remove trailing/leading whitespace
    .remove_duplicates()               # drop duplicate rows
    .handle_missing_values(strategy="mean") # strategies: 'drop', 'mean', 'median', 'mode', 'constant'
)

# Export cleaned data
cleaner.export("data/processed/cleaned_dataset.csv")
```

### 2. Dataset Quality Inspection (`src/utils.py`)
Quickly assess missing values, duplicates, and column types before and after cleaning:

```python
from src.utils import load_dataset, inspect_data, print_summary

df = load_dataset("data/raw/your_dataset.csv")
summary = inspect_data(df)
print_summary(summary)
```

---

## ⚙️ Customization

Feel free to customize the pipeline steps in `main.py` and extend `src/cleaner.py` with custom business rules, outlier detection, or encoding logic specific to your dataset.
