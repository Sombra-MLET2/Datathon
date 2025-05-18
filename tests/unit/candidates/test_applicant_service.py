import os
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session

from src.candidates.applicant_service import ApplicantService
from src.models.applicant import Applicant


class TestApplicantService(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=Session)
        self.mock_repository = MagicMock()
        
        with patch('src.candidates.applicant_service.ApplicantRepository', return_value=self.mock_repository):
            self.service = ApplicantService(self.mock_db)
    
    def test_create_applicant(self):
        applicant_data = {
            "infos_basicas": {
                "codigo_profissional": "ABC123",
                "nome": "Test User",
                "email": "test@example.com"
            }
        }
        mock_applicant = MagicMock(spec=Applicant)
        self.mock_repository.create.return_value = mock_applicant

        result = self.service.create_applicant(applicant_data)
        
        self.mock_repository.create.assert_called_once_with(applicant_data)
        self.assertEqual(result, mock_applicant)
    
    def test_get_applicant(self):
        applicant_id = 1
        mock_applicant = MagicMock(spec=Applicant)
        self.mock_repository.get_by_id.return_value = mock_applicant
        
        result = self.service.get_applicant(applicant_id)
        
        self.mock_repository.get_by_id.assert_called_once_with(applicant_id)
        self.assertEqual(result, mock_applicant)
    
    def test_get_applicant_by_codigo(self):
        codigo = "ABC123"
        mock_applicant = MagicMock(spec=Applicant)
        self.mock_repository.get_by_codigo_profissional.return_value = mock_applicant
        
        result = self.service.get_applicant_by_codigo(codigo)
        
        self.mock_repository.get_by_codigo_profissional.assert_called_once_with(codigo)
        self.assertEqual(result, mock_applicant)
    
    def test_get_applicants_by_codigo(self):
        codigos = ["ABC123", "DEF456"]
        mock_applicants = [MagicMock(spec=Applicant), MagicMock(spec=Applicant)]
        self.mock_repository.get_many_by_codigo_profissional.return_value = mock_applicants
        
        result = self.service.get_applicants_by_codigo(codigos)
        
        self.mock_repository.get_many_by_codigo_profissional.assert_called_once_with(codigos)
        self.assertEqual(result, mock_applicants)
    
    def test_get_applicants(self):
        skip = 10
        limit = 20
        mock_applicants = [MagicMock(spec=Applicant), MagicMock(spec=Applicant)]
        self.mock_repository.get_all.return_value = mock_applicants
        
        result = self.service.get_applicants(skip, limit)
        
        self.mock_repository.get_all.assert_called_once_with(skip, limit)
        self.assertEqual(result, mock_applicants)
    
    def test_update_applicant(self):
        applicant_id = 1
        applicant_data = {"nome": "Updated Name"}
        mock_applicant = MagicMock(spec=Applicant)
        self.mock_repository.update.return_value = mock_applicant
        
        result = self.service.update_applicant(applicant_id, applicant_data)
        
        self.mock_repository.update.assert_called_once_with(applicant_id, applicant_data)
        self.assertEqual(result, mock_applicant)
    
    def test_delete_applicant(self):
        applicant_id = 1
        self.mock_repository.delete.return_value = True
        
        result = self.service.delete_applicant(applicant_id)
        
        self.mock_repository.delete.assert_called_once_with(applicant_id)
        self.assertTrue(result)
    
    def test_count_applicants(self):
        self.mock_repository.count.return_value = 42
        
        result = self.service.count_applicants()
        
        self.mock_repository.count.assert_called_once()
        self.assertEqual(result, 42)
    
    def test_bootstrap_applicants_with_default_path(self):
        success_count, error_count = 10, 2
        self.mock_repository.bootstrap_from_file.return_value = (success_count, error_count)
        
        result = self.service.bootstrap_applicants()
        
        expected_path = os.path.join("data", "json", "applicants.json")
        self.mock_repository.bootstrap_from_file.assert_called_once_with(expected_path)
        self.assertEqual(result, (success_count, error_count))
    
    def test_bootstrap_applicants_with_custom_path(self):
        custom_path = "/custom/path/applicants.json"
        success_count, error_count = 10, 2
        self.mock_repository.bootstrap_from_file.return_value = (success_count, error_count)
        
        result = self.service.bootstrap_applicants(custom_path)
        
        self.mock_repository.bootstrap_from_file.assert_called_once_with(custom_path)
        self.assertEqual(result, (success_count, error_count))


if __name__ == '__main__':
    unittest.main()
