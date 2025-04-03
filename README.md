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