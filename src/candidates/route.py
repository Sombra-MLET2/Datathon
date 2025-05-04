import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.candidates.applicant_service import ApplicantService
from src.candidates.search_candidates import search_candidates
from src.dtos import ApplicantResponseDTO, ApplicantListResponseDTO
from src.embeddings.embeddings_service import index_single_applicant
from src.infra.database import get_db
from src.models.candidate import Candidate, CandidateSearch

candidates_router = APIRouter(
    prefix="/candidates",
    tags=["candidates"],
    responses={401: {"description": "Invalid credentials"},
               500: {"description": "Internal server error"}}
)


@candidates_router.post("/", tags=["candidates"], summary="Index applicants into embeddings db")
async def index_applicants(candidate: Candidate):
    try:
        index_single_applicant(candidate)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@candidates_router.post("/search", tags=["candidates"], summary="Search candidates with embeddings")
async def candidates(request: CandidateSearch):
    try:
        hits = search_candidates(request)
        return {
            "success": True,
            "found": len(hits),
            "candidates": hits
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@candidates_router.get("/{applicant_id}", response_model=ApplicantResponseDTO, summary="Get candidate by ID")
def get_applicant(applicant_id: int, db: Session = Depends(get_db)):
    service = ApplicantService(db)
    applicant = service.get_applicant(applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


@candidates_router.get("/", response_model=ApplicantListResponseDTO, summary="List all candidates")
def list_applicants(
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(10, ge=1, le=100, description="Items per page"),
        db: Session = Depends(get_db)
):
    service = ApplicantService(db)

    skip = (page - 1) * page_size

    applicants = service.get_applicants(skip=skip, limit=page_size)

    total = service.count_applicants()
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    return {
        "items": applicants,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }