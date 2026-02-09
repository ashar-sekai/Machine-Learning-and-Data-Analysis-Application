"""
Register Dialog Module

This module provides the registration UI using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterDialog:
    """Registration dialog window for new users."""
    
    def __init__(self, parent, auth_manager):
        """
        Initialize registration dialog.
        
        Args:
            parent: Parent tkinter window
            auth_manager: AuthenticationManager instance
        """
        self.auth_manager = auth_manager
        
        # Create toplevel window
        self.window = tk.Toplevel(parent)
        self.window.title("ML Data Analysis - Register")
        self.window.geometry("400x450")
        self.window.resizable(False, False)
        
        # Center window on screen
        self._center_window()
        
        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Setup UI
        self._create_widgets()
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self._register())
    
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
            text="Create New Account",
            font=('Arial', 14, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Username field
        ttk.Label(main_frame, text="Username:").grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.username_entry = ttk.Entry(main_frame, width=35)
        self.username_entry.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.username_entry.focus()
        
        ttk.Label(
            main_frame,
            text="(3-30 characters, alphanumeric and underscores)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Email field
        ttk.Label(main_frame, text="Email:").grid(
            row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.email_entry = ttk.Entry(main_frame, width=35)
        self.email_entry.grid(row=5, column=0, columnspan=2, pady=(0, 15))
        
        # Password field
        ttk.Label(main_frame, text="Password:").grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.password_entry = ttk.Entry(main_frame, width=35, show="*")
        self.password_entry.grid(row=7, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(
            main_frame,
            text="(Min 8 chars, 1 uppercase, 1 lowercase, 1 digit)",
            font=('Arial', 8),
            foreground='gray'
        ).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Confirm password field
        ttk.Label(main_frame, text="Confirm Password:").grid(
            row=9, column=0, columnspan=2, sticky=tk.W, pady=(0, 5)
        )
        self.confirm_password_entry = ttk.Entry(main_frame, width=35, show="*")
        self.confirm_password_entry.grid(row=10, column=0, columnspan=2, pady=(0, 15))
        
        # Register button
        register_btn = ttk.Button(
            main_frame,
            text="Register",
            command=self._register,
            width=15
        )
        register_btn.grid(row=11, column=0, columnspan=2, pady=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(
            main_frame,
            text="Cancel",
            command=self.window.destroy,
            width=15
        )
        cancel_btn.grid(row=12, column=0, columnspan=2)
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def _register(self):
        """Handle register button click."""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate inputs
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        if not email:
            messagebox.showerror("Error", "Please enter an email")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        # Register user
        success, message, user_id = self.auth_manager.register_user(username, email, password)
        
        if success:
            logger.info(f"Registration successful for user: {username}")
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            self.window.destroy()
        else:
            messagebox.showerror("Registration Failed", message)
