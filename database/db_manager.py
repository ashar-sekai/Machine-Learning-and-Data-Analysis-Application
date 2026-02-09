"""
Database Manager Module

This module handles all database operations including connection management,
table creation, and user data operations.
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for user authentication."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Use application data directory
            app_dir = os.path.expanduser("~/.ml_data_analysis_app")
            os.makedirs(app_dir, exist_ok=True)
            db_path = os.path.join(app_dir, "users.db")
        
        self.db_path = db_path
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Get a database connection.
        
        Returns:
            SQLite connection object
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _initialize_database(self):
        """Create users table if it doesn't exist."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_login TEXT,
                    is_active INTEGER DEFAULT 1
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """
        Create a new user in the database.
        
        Args:
            username: Unique username
            email: Unique email address
            password_hash: Hashed password (NOT plain text)
        
        Returns:
            User ID if successful, None if failed
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            created_at = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, created_at))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"User created: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError as e:
            logger.error(f"User creation failed (integrity): {e}")
            return None
        except Exception as e:
            logger.error(f"User creation failed: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Retrieve user by username.
        
        Args:
            username: Username to search for
        
        Returns:
            Dictionary with user data or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, created_at, last_login, is_active
                FROM users
                WHERE username = ?
            """, (username,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Retrieve user by email.
        
        Args:
            email: Email to search for
        
        Returns:
            Dictionary with user data or None if not found
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, created_at, last_login, is_active
                FROM users
                WHERE email = ?
            """, (email,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return None
    
    def update_last_login(self, user_id: int) -> bool:
        """
        Update the last login timestamp for a user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            last_login = datetime.now().isoformat()
            
            cursor.execute("""
                UPDATE users
                SET last_login = ?
                WHERE id = ?
            """, (last_login, user_id))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Updated last login for user ID: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """
        Get all users (for admin purposes).
        
        Returns:
            List of user dictionaries
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, created_at, last_login, is_active
                FROM users
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error retrieving all users: {e}")
            return []
    
    def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate a user account.
        
        Args:
            user_id: ID of the user
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users
                SET is_active = 0
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Deactivated user ID: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            return False
