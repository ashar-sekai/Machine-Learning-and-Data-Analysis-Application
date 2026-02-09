"""
Test script for authentication and database functionality.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from auth.authentication import AuthenticationManager
import tempfile
import os

def test_authentication():
    """Test authentication functionality."""
    print("=" * 60)
    print("Testing Authentication System")
    print("=" * 60)
    
    # Create temporary database
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        # Initialize managers
        print("\n1. Initializing database and authentication...")
        db_manager = DatabaseManager(db_path)
        auth_manager = AuthenticationManager(db_manager)
        print("✓ Initialized successfully")
        
        # Test user registration
        print("\n2. Testing user registration...")
        success, message, user_id = auth_manager.register_user(
            "testuser",
            "test@example.com",
            "TestPass123"
        )
        
        if success:
            print(f"✓ Registration successful! User ID: {user_id}")
        else:
            print(f"✗ Registration failed: {message}")
            return False
        
        # Test duplicate username
        print("\n3. Testing duplicate username prevention...")
        success, message, _ = auth_manager.register_user(
            "testuser",
            "test2@example.com",
            "TestPass123"
        )
        
        if not success and "already exists" in message:
            print(f"✓ Duplicate prevention working: {message}")
        else:
            print("✗ Duplicate prevention failed")
            return False
        
        # Test authentication with correct password
        print("\n4. Testing authentication with correct password...")
        success, message, user_data = auth_manager.authenticate_user(
            "testuser",
            "TestPass123"
        )
        
        if success:
            print(f"✓ Authentication successful!")
            print(f"  User: {user_data['username']}")
            print(f"  Email: {user_data['email']}")
        else:
            print(f"✗ Authentication failed: {message}")
            return False
        
        # Test authentication with wrong password
        print("\n5. Testing authentication with wrong password...")
        success, message, _ = auth_manager.authenticate_user(
            "testuser",
            "WrongPassword"
        )
        
        if not success:
            print(f"✓ Correctly rejected wrong password: {message}")
        else:
            print("✗ Should have rejected wrong password")
            return False
        
        # Test password validation
        print("\n6. Testing password validation...")
        valid, error = auth_manager.validate_password("short")
        if not valid:
            print(f"✓ Weak password rejected: {error}")
        else:
            print("✗ Should have rejected weak password")
            return False
        
        valid, error = auth_manager.validate_password("StrongPass123")
        if valid:
            print(f"✓ Strong password accepted")
        else:
            print(f"✗ Should have accepted strong password: {error}")
            return False
        
        # Test email validation
        print("\n7. Testing email validation...")
        valid, error = auth_manager.validate_email("invalid")
        if not valid:
            print(f"✓ Invalid email rejected: {error}")
        else:
            print("✗ Should have rejected invalid email")
            return False
        
        valid, error = auth_manager.validate_email("valid@example.com")
        if valid:
            print(f"✓ Valid email accepted")
        else:
            print(f"✗ Should have accepted valid email: {error}")
            return False
        
        # Test username validation
        print("\n8. Testing username validation...")
        valid, error = auth_manager.validate_username("ab")
        if not valid:
            print(f"✓ Short username rejected: {error}")
        else:
            print("✗ Should have rejected short username")
            return False
        
        valid, error = auth_manager.validate_username("valid_user123")
        if valid:
            print(f"✓ Valid username accepted")
        else:
            print(f"✗ Should have accepted valid username: {error}")
            return False
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return True

if __name__ == "__main__":
    try:
        success = test_authentication()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
