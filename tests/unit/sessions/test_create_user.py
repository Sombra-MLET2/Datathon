import unittest
from unittest.mock import patch, MagicMock
from src.sessions.create_user import create_user
from src.dtos.session_dto import User as UserDTO
from src.models.user import User as UserEntity


class TestCreateUser(unittest.TestCase):
    
    def setUp(self):
        self.mock_db = MagicMock()
        
        self.test_user = UserDTO(
            email="test@example.com",
            password="password123"
        )
    
    @patch('src.sessions.create_user.bcrypt_password')
    def test_create_user_success(self, mock_bcrypt):
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_one_or_none = MagicMock(return_value=None)
        
        self.mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.one_or_none.return_value = mock_one_or_none.return_value
        
        mock_bcrypt.return_value = "hashed_password123"
        
        result = create_user(self.test_user, self.mock_db)
        
        self.assertTrue(result)
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_called_once()
        
        call_args = self.mock_db.add.call_args[0][0]
        self.assertIsInstance(call_args, UserEntity)
        self.assertEqual(call_args.email, "test@example.com")
        self.assertEqual(call_args.hashed_password, "hashed_password123")
        self.assertTrue(call_args.is_active)
    
    def test_create_user_already_exists(self):
        existing_user = UserEntity(
            email="test@example.com",
            hashed_password="existing_hash",
            is_active=True
        )
        
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_one_or_none = MagicMock(return_value=existing_user)
        
        self.mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.one_or_none.return_value = mock_one_or_none.return_value
        
        result = create_user(self.test_user, self.mock_db)
        
        self.assertFalse(result)
        self.mock_db.add.assert_not_called()
        self.mock_db.commit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
