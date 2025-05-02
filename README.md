# Configuration

## Requirement

## Setup Virtual Environment

### 1. Create a Virtual Environment
```bash
    python -m venv .venv
```

### 2. Active the Virtual Environment
```bash
    source .venv/bin/activate
```

### 3. Install Dependencies
```bash
    pip install --upgrade pip
    pip install -r requirements.txt
```

### 4. Running the API
```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Note
because of the size of the files in the data directory, if you need to download them, run the following commands.
git large file storage(lfs) is required
```bash
    git lfs install
    git lfs pull
```

# Model Score

<!-- START_SCORE -->
```
Random Forest Accuracy: 0.87
XGBoost Accuracy: 0.91

Random Forest F1: 0.7
XGBoost F1: 0.74

Number of records: 33585
Random Forest Training Time: 37.51 s
XGBoost Training Time: 780.11 s

Number of records: 11195
Random Forest Inference Time: 0.67 s
XGBoost Inference Time: 0.3 s
```
<!-- END_SCORE -->