from fastapi import APIRouter

prediction_router = APIRouter(
	prefix="/prediction",
	tags=["prediction"],
	responses={404: {"description": "Not found"}}
)