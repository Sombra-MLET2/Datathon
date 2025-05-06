import json
import os
from sqlalchemy.orm import Session
from src.models.applicant import Applicant
from typing import List, Dict, Optional, Tuple


class ApplicantRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, applicant_data: Dict) -> Applicant:
        applicant = Applicant(applicant_data)
        self.db.add(applicant)
        self.db.commit()
        self.db.refresh(applicant)
        return applicant
    
    def get_by_id(self, applicant_id: int) -> Optional[Applicant]:
        return self.db.query(Applicant).filter(Applicant.id == applicant_id).first()
    
    def get_by_codigo_profissional(self, codigo: str) -> Optional[Applicant]:
        return self.db.query(Applicant).filter(Applicant.codigo_profissional == codigo).first()

    def get_many_by_codigo_profissional(self, codigos: List[str]) -> Optional[List[Applicant]]:
        return self.db.query(Applicant).filter(Applicant.codigo_profissional.in_(codigos)).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Applicant]:
        return self.db.query(Applicant).offset(skip).limit(limit).all()
    
    def update(self, applicant_id: int, applicant_data: Dict) -> Optional[Applicant]:
        applicant = self.get_by_id(applicant_id)
        if applicant:
            for key, value in applicant_data.items():
                setattr(applicant, key, value)
            self.db.commit()
            self.db.refresh(applicant)
        return applicant
    
    def delete(self, applicant_id: int) -> bool:
        applicant = self.get_by_id(applicant_id)
        if applicant:
            self.db.delete(applicant)
            self.db.commit()
            return True
        return False
    
    def count(self) -> int:
        return self.db.query(Applicant).count()
    
    def bootstrap_from_file(self, file_path: str) -> Tuple[int, int]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        success_count = 0
        error_count = 0
        
        for codigo, applicant_data in data.items():
            try:
                existing = self.get_by_codigo_profissional(codigo)
                if not existing:
                    if "infos_basicas" not in applicant_data:
                        applicant_data["infos_basicas"] = {}
                    applicant_data["infos_basicas"]["codigo_profissional"] = codigo
                    
                    self.create(applicant_data)
                    success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Error processing applicant {codigo}: {str(e)}")
        
        return success_count, error_count
