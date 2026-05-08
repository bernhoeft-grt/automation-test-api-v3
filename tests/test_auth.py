"""Authentication tests."""
import pytest
import allure
from utils.auth import login_and_get_token


@allure.feature("Authentication")
@allure.title("Test Login - Get Token")
class TestAuth:
    """Test authentication endpoints."""

    @allure.title("Should login and return a valid token")
    def test_login_and_get_token(self):
        """Verify login endpoint returns a bearer token."""
        token = login_and_get_token()
        
        assert token, "Token should not be empty"
        assert isinstance(token, str), "Token should be a string"
        assert len(token) > 10, "Token should have reasonable length"
        
        allure.attach(f"Token: {token[:50]}...", "Token Preview", allure.attachment_type.TEXT)
