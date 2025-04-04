from fastapi import FastAPI
from src.infra.database import engine, Base
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