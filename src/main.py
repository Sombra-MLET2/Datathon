from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from src.infra.database import engine, Base
from src.sessions.route import sessions_router
from src.candidates.route import candidates_router
from src.embeddings.route import embeddings_router
from src.vacancies.routes import vacancies_router as job_vacancy_router
from src.infra.bootstrap.route import boostrap_route as bootstrap_router
from src.static.static import static_router, react_build_exists, REACT_BUILD_DIR

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router, prefix="/api")
app.include_router(candidates_router, prefix="/api")
app.include_router(embeddings_router, prefix="/api")
app.include_router(job_vacancy_router, prefix="/api")
app.include_router(bootstrap_router, prefix="/api")

# SQLAlchemy create tables
Base.metadata.create_all(engine)

if react_build_exists():
    app.mount("/static", StaticFiles(directory=os.path.join(REACT_BUILD_DIR, "static")), name="static")

app.include_router(static_router)


@app.get("/api", tags=["root"], summary="Team & Project Info")
async def root():
    return {
        "FIAP": {
            "success": True,
            "tech_challenge": "Datathon",
            "team": "Sombra-MLET2"
        }
    }
