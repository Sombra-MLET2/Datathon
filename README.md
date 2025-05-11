# Sombra Recruitment System

A human resource system that helps recruiters select better job candidates.

## Features

- Responsive UI
- User authentication (simple login/register)
- Applicant management
- Job vacancy management
- Candidates recommended by vacancy
- Candidates chance to receive an offer—TODO

## API Endpoints

- `/api/sessions` - User authentication
- `/api/job-vacancies` - Job vacancy management
- `/api/candidates` - Candidate search
- `/api/bootstrap` - Data initialization - Admin purposes only

## Configuration

### Requirements

- Python 3.12+
- Node.js 16+ (for frontend)
- npm 8+ (for frontend)

### Setup Virtual Environment

#### 1. Create a Virtual Environment
```bash
  python -m venv .venv
```

#### 2. Activate the Virtual Environment
```bash
  source .venv/bin/activate
```

#### 3. Install Dependencies
```bash
  pip install --upgrade pip
  pip install -r requirements.txt
```

### Build the Frontend

```bash
  ./build_frontend.sh
```

### Running the API with Frontend
```bash
  uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## Deployment - Docker

TODO

## Note
Because of the size of the files in the data directory, if you need to download them, run the following commands.
Git large file storage(lfs) is required

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
Random Forest Training Time: 53.24 s
XGBoost Training Time: 1277.3 s

Number of records: 11195
Random Forest Inference Time: 1.32 s
XGBoost Inference Time: 0.23 s
```
<!-- END_SCORE -->