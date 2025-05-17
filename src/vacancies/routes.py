from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
import math
from typing import Dict, Any

from src.infra.database import get_db
from src.candidates.applicant_service import ApplicantService
from src.vacancies.job_vacancy_service import JobVacancyService
from src.dtos.job_vacancy_dto import JobVacancyResponseDTO, JobVacancyListResponseDTO
import src.vacancies.job_vacancy_predict as predict
from src.vacancies.cv_analysis_service import CVAnalysisService

vacancies_router = APIRouter(
    prefix="/job-vacancies",
    tags=["job-vacancies"],
    responses={404: {"description": "Not found"}},
)


@vacancies_router.get("/{vacancy_id}", response_model=JobVacancyResponseDTO, summary="Get a job vacancy by ID")
def get_job_vacancy(vacancy_id: int, db: Session = Depends(get_db)):
    service = JobVacancyService(db)
    vacancy = service.get_job_vacancy(vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Job vacancy not found")
    return vacancy


@vacancies_router.get("/", response_model=JobVacancyListResponseDTO, summary="List job vacancies")
def list_job_vacancies(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    service = JobVacancyService(db)
    
    skip = (page - 1) * page_size
    
    vacancies = service.get_job_vacancies(skip=skip, limit=page_size)
    
    total = service.count_job_vacancies()
    total_pages = math.ceil(total / page_size) if total > 0 else 1
    
    return {
        "items": vacancies,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@vacancies_router.get("/{vacancy_id}/offer-inference/{applicant_id}", summary="Infer an offer for a candidate based on the given vacancy.")
def infer_offer_from_candidate(vacancy_id: int, applicant_id: int, db: Session = Depends(get_db)):
    
    if vacancy_id is None  or vacancy_id <= 0:
        raise HTTPException(status_code=400, detail="vacancy_id is required and must be greater than 0")
    
    if applicant_id is None or applicant_id <= 0:
        raise HTTPException(status_code=400, detail="applicant_id is required and must be greater than 0")  
    
    job_service = JobVacancyService(db)
    vacancy = job_service.get_job_vacancy(vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Job vacancy not found")

    applicant_service = ApplicantService(db)
    applicant = applicant_service.get_applicant(applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    
    try:
        return predict.infer_offer_from_candidate(vacancy, applicant)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction has failed: {str(e)}")

@vacancies_router.post("/{vacancy_id}/analyze-cv", summary="Analyze a candidate's CV against a job vacancy using ollama llm integration")
def analyze_cv(
    vacancy_id: int, 
    data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):

    candidate_id = data.get("candidate_id")
    if not candidate_id:
        raise HTTPException(status_code=400, detail="candidate_id is required")
    
    similarity = data.get("similarity", 0)
    acceptance_probability = data.get("acceptance_probability", 0)
    
    job_service = JobVacancyService(db)
    vacancy = job_service.get_job_vacancy(vacancy_id)
    if vacancy is None:
        raise HTTPException(status_code=404, detail="Job vacancy not found")

    applicant_service = ApplicantService(db)
    candidate = applicant_service.get_applicant(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    try:
        cv_analysis_service = CVAnalysisService()
        analysis = cv_analysis_service.analyze_cv(
            candidate=candidate,
            vacancy=vacancy,
            similarity=similarity,
            acceptance_probability=acceptance_probability
        )
        
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CV analysis failed: {str(e)}")
