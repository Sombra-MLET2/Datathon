from src.vacancies.ollama_service import OllamaService
from src.models.applicant import Applicant
from src.models.job_vacancy import JobVacancy
from src.infra.configs import logger

class CVAnalysisService:

    def __init__(self):
        self.ollama_service = OllamaService()
    
    def analyze_cv(self, candidate: Applicant, vacancy: JobVacancy, similarity: float, acceptance_probability: float):

        cv_text = candidate.cv_pt or ""
        job_description = vacancy.principais_atividades or vacancy.competencia_tecnicas_e_comportamentais or ""
        
        similarity_percentage = f"{similarity:.2%}" if isinstance(similarity, float) else similarity
        acceptance_percentage = f"{acceptance_probability:.2%}" if isinstance(acceptance_probability, float) else acceptance_probability
        
        prompt = f"""
You are a HR Analyst specialized in CV Analysis and provide very insightful instructions about the candidate chances and compatibility with vacancies.

You also receive the following data from the system AI:
---
Candidate similarity: {similarity_percentage}
Applicant acceptance probability: {acceptance_percentage}
---

You should consider the candidate CV in Portuguese(Brazil):
---
{cv_text}
---

You should check the candidate CV above with the job description below:
---
{job_description}
---
"""
        
        system_message = "You are a HR Analyst specialized in CV Analysis. Provide a concise analysis in Portuguese."
        
        try:
            logger.info(f"Analyzing CV for candidate ID: {candidate.id}")
            result = self.ollama_service.generate(prompt, system=system_message)
            logger.info(f"Analysis complete. Response length: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"Error analyzing CV: {e}")
            return f"Erro na análise do CV: {str(e)}"
