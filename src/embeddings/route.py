from fastapi import APIRouter

from src.embeddings.embeddings_service import index_all_applicants, reset_candidates_collection

embeddings_router = APIRouter(
    prefix="/boostrap",
    tags=["embeddings"],
    responses={401: {"description": "Invalid credentials"},
               500: {"description": "Internal server error"}}
)

@embeddings_router.post("/embeddings", tags=["embeddings"], summary="Bootstrap the database with embeddings")
async def bootstrap_embeddings():
    try:
        index_all_applicants()
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


@embeddings_router.delete("/embeddings", tags=["embeddings"], summary="Delete the embeddings from the database")
async def delete_embeddings():
    try:
        reset_candidates_collection()
    except Exception as e:
        return {"success": False, "error": str(e)}

    return {"success": True}


