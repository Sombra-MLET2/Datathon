import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import jwt
from src.sessions.create_token import create_access_token


class TestCreateToken(unittest.TestCase):
    
    @patch('src.sessions.create_token.datetime')
    @patch('src.sessions.create_token.data_config')
    def test_create_access_token(self, mock_config, mock_datetime):
        mock_config.JWT_EXPIRY = 30
        mock_config.JWT_SECRET = "test_secret"
        mock_config.JWT_ALGORITHM = "HS256"
        
        fixed_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = fixed_datetime
        
        expected_expiry = fixed_datetime + timedelta(minutes=30)
        
        test_data = {"sub": "test@example.com"}
        
        token = create_access_token(test_data)
        
        decoded = jwt.decode(
            token, 
            mock_config.JWT_SECRET, 
            algorithms=[mock_config.JWT_ALGORITHM],
            options={"verify_exp": False}  # Skip expiration verification
        )
        
        self.assertEqual(decoded["sub"], "test@example.com")
        self.assertEqual(decoded["exp"], int(expected_expiry.timestamp()))
    
    @patch('src.sessions.create_token.datetime')
    @patch('src.sessions.create_token.data_config')
    def test_create_access_token_with_custom_expiry(self, mock_config, mock_datetime):
        mock_config.JWT_EXPIRY = 60  # Different expiry time
        mock_config.JWT_SECRET = "test_secret"
        mock_config.JWT_ALGORITHM = "HS256"
        
        fixed_datetime = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        mock_datetime.now.return_value = fixed_datetime
        
        expected_expiry = fixed_datetime + timedelta(minutes=60)
        
        test_data = {"sub": "test@example.com", "role": "admin"}
        
        token = create_access_token(test_data)
        
        decoded = jwt.decode(
            token, 
            mock_config.JWT_SECRET, 
            algorithms=[mock_config.JWT_ALGORITHM],
            options={"verify_exp": False}  # Skip expiration verification
        )
        
        self.assertEqual(decoded["sub"], "test@example.com")
        self.assertEqual(decoded["role"], "admin")
        self.assertEqual(decoded["exp"], int(expected_expiry.timestamp()))


if __name__ == '__main__':
    unittest.main()
