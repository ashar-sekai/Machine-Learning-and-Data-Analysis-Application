"""
Main Entry Point

This is the main entry point for the ML Data Analysis Application.
It handles the login flow and launches the main application upon successful authentication.
"""

import tkinter as tk
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from database.db_manager import DatabaseManager
from auth.authentication import AuthenticationManager
from ui.login_dialog import LoginDialog
from ui.main_app import MainApplication

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    try:
        logger.info("Starting ML Data Analysis Application")
        
        # Initialize database
        db_manager = DatabaseManager()
        logger.info("Database initialized")
        
        # Initialize authentication
        auth_manager = AuthenticationManager(db_manager)
        logger.info("Authentication manager initialized")
        
        # Create hidden root window for login dialog
        root = tk.Tk()
        root.withdraw()
        
        # User data storage
        user_data = None
        
        def on_login_success(user_info):
            """Callback for successful login."""
            nonlocal user_data
            user_data = user_info
            logger.info(f"User {user_info['username']} logged in successfully")
        
        # Show login dialog
        logger.info("Showing login dialog")
        login_dialog = LoginDialog(root, auth_manager, on_login_success)
        login_dialog.show()
        
        # Destroy temporary root
        root.destroy()
        
        # Check if login was successful
        if user_data:
            logger.info("Launching main application")
            # Launch main application
            app = MainApplication(user_data)
            app.run()
        else:
            logger.info("Login cancelled or failed")
            return
        
        logger.info("Application closed")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
