import unittest
from unittest.mock import MagicMock
from src.sessions.list_users import list_users
from src.models.user import User as UserEntity


class TestListUsers(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock()
    
    def test_list_users_with_data(self):
        mock_users = [
            UserEntity(id=1, email="user1@example.com", hashed_password="hash1", is_active=True),
            UserEntity(id=2, email="user2@example.com", hashed_password="hash2", is_active=True),
            UserEntity(id=3, email="user3@example.com", hashed_password="hash3", is_active=False)
        ]
        
        mock_query = MagicMock()
        mock_query.all.return_value = mock_users
        self.mock_db.query.return_value = mock_query
        
        users, total = list_users(self.mock_db)
        
        self.assertEqual(users, mock_users)
        self.assertEqual(total, 3)
        self.mock_db.query.assert_called_once_with(UserEntity)
        mock_query.all.assert_called_once()
    
    def test_list_users_empty(self):
        mock_query = MagicMock()
        mock_query.all.return_value = []
        self.mock_db.query.return_value = mock_query
        
        users, total = list_users(self.mock_db)
        
        self.assertEqual(users, [])
        self.assertEqual(total, 0)
        self.mock_db.query.assert_called_once_with(UserEntity)
        mock_query.all.assert_called_once()


if __name__ == '__main__':
    unittest.main()
