from pydantic import BaseModel


class CandidateSearch(BaseModel):
    top_candidates: int = 5
    job_description: str
