import json
import os
from sqlalchemy.orm import Session
from src.models.job_vacancy import JobVacancy
from typing import List, Dict, Optional, Tuple


class JobVacancyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, vacancy_data: Dict, vaga_id: str) -> JobVacancy:
        vacancy = JobVacancy(vacancy_data, vaga_id)
        self.db.add(vacancy)
        self.db.commit()
        self.db.refresh(vacancy)
        return vacancy
    
    def get_by_id(self, vacancy_id: int) -> Optional[JobVacancy]:
        return self.db.query(JobVacancy).filter(JobVacancy.id == vacancy_id).first()
    
    def get_by_vaga_id(self, vaga_id: str) -> Optional[JobVacancy]:
        return self.db.query(JobVacancy).filter(JobVacancy.vaga_id == vaga_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[JobVacancy]:
        return self.db.query(JobVacancy).offset(skip).limit(limit).all()
    
    def update(self, vacancy_id: int, vacancy_data: Dict) -> Optional[JobVacancy]:
        vacancy = self.get_by_id(vacancy_id)
        if vacancy:
            for key, value in vacancy_data.items():
                setattr(vacancy, key, value)
            self.db.commit()
            self.db.refresh(vacancy)
        return vacancy
    
    def delete(self, vacancy_id: int) -> bool:
        vacancy = self.get_by_id(vacancy_id)
        if vacancy:
            self.db.delete(vacancy)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        return self.db.query(JobVacancy).count()
    
    def bootstrap_from_file(self, file_path: str) -> Tuple[int, int]:
        """
        Load job vacancies from a JSON file and save them to the database
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        success_count = 0
        error_count = 0
        
        for vaga_id, vacancy_data in data.items():
            try:
                # Check if vacancy already exists
                existing = self.get_by_vaga_id(vaga_id)
                if not existing:
                    # Create the job vacancy
                    self.create(vacancy_data, vaga_id)
                    success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing job vacancy {vaga_id}: {str(e)}")
        
        return success_count, error_count
