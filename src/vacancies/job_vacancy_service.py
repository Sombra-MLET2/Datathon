import os
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from src.vacancies.job_vacancy_repository import JobVacancyRepository
from src.models.job_vacancy import JobVacancy


class JobVacancyService:
    def __init__(self, db: Session):
        self.repository = JobVacancyRepository(db)
    
    def create_job_vacancy(self, vacancy_data: Dict, vaga_id: str) -> JobVacancy:
        return self.repository.create(vacancy_data, vaga_id)
    
    def get_job_vacancy(self, vacancy_id: int) -> Optional[JobVacancy]:
        return self.repository.get_by_id(vacancy_id)
    
    def get_job_vacancy_by_vaga_id(self, vaga_id: str) -> Optional[JobVacancy]:
        return self.repository.get_by_vaga_id(vaga_id)
    
    def get_job_vacancies(self, skip: int = 0, limit: int = 100) -> List[JobVacancy]:
        return self.repository.get_all(skip, limit)
    
    def update_job_vacancy(self, vacancy_id: int, vacancy_data: Dict) -> Optional[JobVacancy]:
        return self.repository.update(vacancy_id, vacancy_data)
    
    def delete_job_vacancy(self, vacancy_id: int) -> bool:
        return self.repository.delete(vacancy_id)
    
    def count_job_vacancies(self) -> int:
        return self.repository.count()
    
    def bootstrap_job_vacancies(self, file_path: str = None) -> Tuple[int, int]:
        if not file_path:
            # Use the default path
            file_path = os.path.join("data", "json", "vagas.json")
        
        return self.repository.bootstrap_from_file(file_path)
