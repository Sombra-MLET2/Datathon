from fastapi import APIRouter

from src.candidates.search_candidates import search_candidates
from src.embeddings.embeddings_service import index_single_applicant
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