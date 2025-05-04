import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

static_router = APIRouter()

REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "build")

def react_build_exists():
    return os.path.exists(REACT_BUILD_DIR)

@static_router.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    if not react_build_exists():
        return {"message": "React app not built yet. Please run 'npm run build' in the frontend directory."}
    
    file_path = os.path.join(REACT_BUILD_DIR, full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    
    index_path = os.path.join(REACT_BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    print("React application is not ready - need to build it correctly")

    return {"message": "Oooops... we forgot something here. Sombra team will fix it ASAP"}
