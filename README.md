# Configuration

## Requirement

Python version 3.10.16

## Setup Virtual Environment

1. Create a Virtual Environment
```bash
    python -m venv .venv
```

2. Active the Virtual Environment
```bash
    source .venv/bin/activate
```

3. Install Dependencies
```bash
    pip install -r requirements.txt
```

4. Running the API
```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000
```