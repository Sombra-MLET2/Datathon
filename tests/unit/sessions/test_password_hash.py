import unittest
from unittest.mock import patch, MagicMock
from src.sessions.password_hash import verify_password, bcrypt_password


class TestPasswordHash(unittest.TestCase):
    
    @patch('src.sessions.password_hash.pwd_context')
    def test_verify_password(self, mock_pwd_context):
        plain_password = "password123"
        hashed_password = "hashed_password_value"
        mock_pwd_context.verify.return_value = True
        
        result = verify_password(plain_password, hashed_password)
        
        self.assertTrue(result)
        mock_pwd_context.verify.assert_called_once_with(plain_password, hashed_password)
    
    @patch('src.sessions.password_hash.pwd_context')
    def test_verify_password_invalid(self, mock_pwd_context):
        plain_password = "wrong_password"
        hashed_password = "hashed_password_value"
        mock_pwd_context.verify.return_value = False
        
        result = verify_password(plain_password, hashed_password)
        
        self.assertFalse(result)
        mock_pwd_context.verify.assert_called_once_with(plain_password, hashed_password)
    
    @patch('src.sessions.password_hash.pwd_context')
    def test_bcrypt_password(self, mock_pwd_context):
        plain_password = "password123"
        expected_hash = "bcrypt_hashed_value"
        mock_pwd_context.hash.return_value = expected_hash
        
        result = bcrypt_password(plain_password)
        
        self.assertEqual(result, expected_hash)
        mock_pwd_context.hash.assert_called_once_with(plain_password)


if __name__ == '__main__':
    unittest.main()
