"""
Login Dialog Module

This module provides the login UI using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoginDialog:
    """Login dialog window for user authentication."""
    
    def __init__(self, parent, auth_manager, on_success: Callable[[Dict], None]):
        """
        Initialize login dialog.
        
        Args:
            parent: Parent tkinter window (can be None)
            auth_manager: AuthenticationManager instance
            on_success: Callback function called with user_data on successful login
        """
        self.auth_manager = auth_manager
        self.on_success = on_success
        self.user_data = None
        
        # Create toplevel window
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("ML Data Analysis - Login")
        self.window.geometry("400x350")
        self.window.resizable(False, False)
        
        # Center window on screen
        self._center_window()
        
        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Setup UI
        self._create_widgets()
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self._login())
    
    def _center_window(self):
        """Center the window on screen."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create and layout UI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Machine Learning & Data Analysis",
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Please login to continue",
            font=('Arial', 10)
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Username field
        ttk.Label(main_frame, text="Username or Email:").grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.username_entry = ttk.Entry(main_frame, width=35)
        self.username_entry.grid(row=3, column=0, columnspan=2, pady=(0, 15))
        self.username_entry.focus()
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.password_entry = ttk.Entry(main_frame, width=35, show="*")
        self.password_entry.grid(row=5, column=0, columnspan=2, pady=(0, 15))
        
        # Remember me checkbox
        self.remember_var = tk.BooleanVar()
        remember_check = ttk.Checkbutton(
            main_frame,
            text="Remember me",
            variable=self.remember_var
        )
        remember_check.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Login button
        login_btn = ttk.Button(
            main_frame,
            text="Login",
            command=self._login,
            width=15
        )
        login_btn.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        # Register link
        register_frame = ttk.Frame(main_frame)
        register_frame.grid(row=8, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Label(register_frame, text="Don't have an account?").pack(side=tk.LEFT)
        register_link = ttk.Label(
            register_frame,
            text="Sign up",
            foreground="blue",
            cursor="hand2"
        )
        register_link.pack(side=tk.LEFT, padx=(5, 0))
        register_link.bind('<Button-1>', lambda e: self._open_register())
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def _login(self):
        """Handle login button click."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username:
            messagebox.showerror("Error", "Please enter username or email")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter password")
            return
        
        # Authenticate
        success, message, user_data = self.auth_manager.authenticate_user(username, password)
        
        if success:
            self.user_data = user_data
            logger.info(f"Login successful for user: {username}")
            self.window.destroy()
            self.on_success(user_data)
        else:
            messagebox.showerror("Login Failed", message)
            self.password_entry.delete(0, tk.END)
    
    def _open_register(self):
        """Open registration dialog."""
        from ui.register_dialog import RegisterDialog
        RegisterDialog(self.window, self.auth_manager)
    
    def show(self):
        """Show the dialog and wait for it to close."""
        self.window.wait_window()
        return self.user_data
