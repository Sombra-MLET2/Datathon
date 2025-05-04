import os
from typing import Dict, Tuple
from sqlalchemy.orm import Session
from src.candidates.applicant_service import ApplicantService
from src.vacancies.job_vacancy_service import JobVacancyService


class BootstrapService:
    def __init__(self, db: Session):
        self.applicant_service = ApplicantService(db)
        self.job_vacancy_service = JobVacancyService(db)
    
    def bootstrap_all(self) -> Dict[str, Tuple[int, int]]:

        results = {}
        
        applicants_file = os.path.join("data", "json", "applicants.json")
        if os.path.exists(applicants_file):
            applicants_success, applicants_error = self.applicant_service.bootstrap_applicants(applicants_file)
            results["applicants"] = (applicants_success, applicants_error)
        else:
            results["applicants"] = (0, 0)
            print(f"Warning: File not found: {applicants_file}")
        
        vacancies_file = os.path.join("data", "json", "vagas.json")
        if os.path.exists(vacancies_file):
            vacancies_success, vacancies_error = self.job_vacancy_service.bootstrap_job_vacancies(vacancies_file)
            results["job_vacancies"] = (vacancies_success, vacancies_error)
        else:
            results["job_vacancies"] = (0, 0)
            print(f"Warning: File not found: {vacancies_file}")
        
        return results
