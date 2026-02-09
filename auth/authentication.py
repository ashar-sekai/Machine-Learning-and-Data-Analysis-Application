"""
Authentication Module

This module handles user authentication, password hashing, and validation.
Uses bcrypt for secure password hashing.
"""

import bcrypt
import re
from typing import Optional, Tuple, Dict
import logging

from database.db_manager import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthenticationManager:
    """Manages user authentication and password security."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize authentication manager.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db_manager = db_manager
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password as string
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored hashed password
        
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password meets security requirements.
        
        Requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        
        Args:
            password: Password to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format.
        
        Args:
            email: Email to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not email or len(email) == 0:
            return False, "Email is required"
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username format.
        
        Requirements:
        - 3-30 characters
        - Alphanumeric and underscores only
        
        Args:
            username: Username to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 30:
            return False, "Username must be at most 30 characters long"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email address
            password: Plain text password
        
        Returns:
            Tuple of (success, message, user_id)
        """
        # Validate username
        valid, error = self.validate_username(username)
        if not valid:
            return False, error, None
        
        # Validate email
        valid, error = self.validate_email(email)
        if not valid:
            return False, error, None
        
        # Validate password
        valid, error = self.validate_password(password)
        if not valid:
            return False, error, None
        
        # Check if username already exists
        if self.db_manager.get_user_by_username(username):
            return False, "Username already exists", None
        
        # Check if email already exists
        if self.db_manager.get_user_by_email(email):
            return False, "Email already exists", None
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user
        user_id = self.db_manager.create_user(username, email, password_hash)
        
        if user_id:
            logger.info(f"User registered successfully: {username}")
            return True, "Registration successful", user_id
        else:
            return False, "Registration failed. Please try again.", None
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate a user.
        
        Args:
            username: Username or email
            password: Plain text password
        
        Returns:
            Tuple of (success, message, user_data)
        """
        # Try to find user by username
        user = self.db_manager.get_user_by_username(username)
        
        # If not found, try by email
        if not user:
            user = self.db_manager.get_user_by_email(username)
        
        if not user:
            return False, "Invalid username or password", None
        
        # Check if account is active
        if not user['is_active']:
            return False, "Account is inactive. Please contact support.", None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            return False, "Invalid username or password", None
        
        # Update last login
        self.db_manager.update_last_login(user['id'])
        
        # Remove password hash from returned data
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        
        logger.info(f"User authenticated successfully: {username}")
        return True, "Login successful", user_data
