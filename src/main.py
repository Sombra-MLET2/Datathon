from fastapi import FastAPI

from src.services.embeddings_service import index_all_applicants, reset_candidates_collection, search_candidates
from src.infra.database import engine, Base
from src.models.candidate import CandidateSearch
from src.sessions.route import sessions_router


app = FastAPI()
app.include_router(sessions_router)

# SQLAlchemy create tables
Base.metadata.create_all(engine)


@app.get("/", tags=["root"], summary="Team & Project Info")
async def root():
    return {
        "FIAP": {
            "success": True,
            "tech_challenge": "Datathon",
            "team": "Sombra-MLET2"
        }
    }


@app.post("/embeddings/database", tags=["embeddings"], summary="Bootstrap the database with embeddings")
async def bootstrap_embeddings():
    try:
        index_all_applicants()
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


@app.delete("/embeddings/database", tags=["embeddings"], summary="Delete the database")
async def delete_embeddings():
    try:
        reset_candidates_collection()
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


@app.post("/candidates", tags=["candidates"], summary="Search candidates with embeddings")
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
