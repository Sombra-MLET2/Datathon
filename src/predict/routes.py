from fastapi import APIRouter
from src.predict.predict_model import PredictModel

prediction_router = APIRouter(
	prefix="/prediction",
	tags=["prediction"],
	responses={404: {"description": "Not found"}}
)