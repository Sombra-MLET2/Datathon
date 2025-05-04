from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.infra.database import get_db
from src.infra.bootstrap.bootstrap_service import BootstrapService
from src.dtos.bootstrap_dto import BootstrapResponseDTO

boostrap_route = APIRouter(
    prefix="/bootstrap",
    tags=["bootstrap"],
    responses={500: {"description": "Internal server error"}},
)


@boostrap_route.post("/sql", response_model=BootstrapResponseDTO, summary="Bootstrap SQL data")
def bootstrap_data(db: Session = Depends(get_db)):
    try:
        service = BootstrapService(db)
        results = service.bootstrap_all()
        
        applicants_success, applicants_error = results.get("applicants", (0, 0))
        vacancies_success, vacancies_error = results.get("job_vacancies", (0, 0))
        
        message = (
            f"Bootstrap completed. "
            f"Applicants: {applicants_success} imported, {applicants_error} errors. "
            f"Job Vacancies: {vacancies_success} imported, {vacancies_error} errors."
        )
        
        return {
            "results": results,
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bootstrap failed: {str(e)}")
