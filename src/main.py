from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
	return {
        "FIAP": {
            "success": True,
            "tech_challenge": "Datathon",
            "team": "Sombra-MLET2"
        }
    }