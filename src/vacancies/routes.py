from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from src.infra.database import get_db
from src.vacancies.job_vacancy_service import JobVacancyService
from src.dtos.job_vacancy_dto import JobVacancyResponseDTO, JobVacancyListResponseDTO

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
