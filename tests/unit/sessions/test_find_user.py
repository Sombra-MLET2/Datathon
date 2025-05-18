import unittest
from unittest.mock import MagicMock
from src.sessions.find_user import find_user
from src.models.user import User as UserEntity


class TestFindUser(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock()
    
    def test_find_user_exists(self):
        test_email = "test@example.com"
        
        mock_user = UserEntity(
            id=1,
            email=test_email,
            hashed_password="hashed_password",
            is_active=True
        )
        
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_one_or_none = MagicMock(return_value=mock_user)
        
        self.mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.one_or_none.return_value = mock_one_or_none.return_value
        
        result = find_user(self.mock_db, test_email)
        
        self.assertEqual(result, mock_user)
        self.mock_db.query.assert_called_once_with(UserEntity)
    
    def test_find_user_not_exists(self):
        test_email = "nonexistent@example.com"
        
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_one_or_none = MagicMock(return_value=None)
        
        self.mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.one_or_none.return_value = mock_one_or_none.return_value
        
        result = find_user(self.mock_db, test_email)
        
        self.assertIsNone(result)
        self.mock_db.query.assert_called_once_with(UserEntity)


if __name__ == '__main__':
    unittest.main()
