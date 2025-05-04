import os
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from src.candidates.applicant_repository import ApplicantRepository
from src.models.applicant import Applicant


class ApplicantService:
    def __init__(self, db: Session):
        self.repository = ApplicantRepository(db)
    
    def create_applicant(self, applicant_data: Dict) -> Applicant:
        """Create a new applicant"""
        return self.repository.create(applicant_data)

    def get_applicant(self, applicant_id: int) -> Optional[Applicant]:
        """Get an applicant by ID"""
        return self.repository.get_by_id(applicant_id)
    
    def get_applicant_by_codigo(self, codigo: str) -> Optional[Applicant]:
        """Get an applicant by codigo_profissional"""
        return self.repository.get_by_codigo_profissional(codigo)
    
    def get_applicants(self, skip: int = 0, limit: int = 100) -> List[Applicant]:
        """Get all applicants with pagination"""
        return self.repository.get_all(skip, limit)
    
    def update_applicant(self, applicant_id: int, applicant_data: Dict) -> Optional[Applicant]:
        """Update an applicant"""
        return self.repository.update(applicant_id, applicant_data)
    
    def delete_applicant(self, applicant_id: int) -> bool:
        """Delete an applicant"""
        return self.repository.delete(applicant_id)
    
    def count_applicants(self) -> int:
        """Count total number of applicants"""
        return self.repository.count()
    
    def bootstrap_applicants(self, file_path: str = None) -> Tuple[int, int]:
        """
        Bootstrap applicants from a JSON file
        If file_path is not provided, it will use the default path
        """
        if not file_path:
            # Use the default path
            file_path = os.path.join("data", "json", "applicants.json")
        
        return self.repository.bootstrap_from_file(file_path)
