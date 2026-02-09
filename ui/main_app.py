"""
Main Application Window

This module provides the main ML and Data Analysis application interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, Optional
import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainApplication:
    """Main application window for ML and Data Analysis."""
    
    def __init__(self, user_data: Dict):
        """
        Initialize main application.
        
        Args:
            user_data: Dictionary containing user information
        """
        self.user_data = user_data
        self.df = None
        self.model = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("ML Data Analysis Application")
        self.root.geometry("1000x700")
        
        # Setup UI
        self._create_menu()
        self._create_widgets()
        
        # Welcome message
        self._show_welcome()
    
    def _create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Data", command=self._load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Analysis menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="View Data", command=self._view_data)
        analysis_menu.add_command(label="Statistics", command=self._show_statistics)
        analysis_menu.add_command(label="Train Model", command=self._train_model)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create and layout UI widgets."""
        # Top frame with user info
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        user_label = ttk.Label(
            top_frame,
            text=f"Welcome, {self.user_data['username']}!",
            font=('Arial', 12, 'bold')
        )
        user_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(
            top_frame,
            text="Logout",
            command=self._logout
        )
        logout_btn.pack(side=tk.RIGHT)
        
        # Main content frame
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = ttk.LabelFrame(content_frame, text="Controls", padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        ttk.Button(
            left_panel,
            text="Load CSV Data",
            command=self._load_data,
            width=20
        ).pack(pady=5)
        
        ttk.Button(
            left_panel,
            text="View Data",
            command=self._view_data,
            width=20
        ).pack(pady=5)
        
        ttk.Button(
            left_panel,
            text="Show Statistics",
            command=self._show_statistics,
            width=20
        ).pack(pady=5)
        
        ttk.Button(
            left_panel,
            text="Train ML Model",
            command=self._train_model,
            width=20
        ).pack(pady=5)
        
        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            left_panel,
            text="No data loaded",
            wraplength=180,
            justify=tk.LEFT
        )
        self.status_label.pack(pady=5)
        
        # Right panel - Output
        right_panel = ttk.LabelFrame(content_frame, text="Output", padding="10")
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Text widget with scrollbar
        text_scroll = ttk.Scrollbar(right_panel)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output_text = tk.Text(
            right_panel,
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            font=('Courier', 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        text_scroll.config(command=self.output_text.yview)
    
    def _show_welcome(self):
        """Display welcome message."""
        welcome_msg = f"""
╔═══════════════════════════════════════════════════════════╗
║  Machine Learning & Data Analysis Application             ║
║  For IBDP Psychology Students (EE & IA)                   ║
╚═══════════════════════════════════════════════════════════╝

Welcome, {self.user_data['username']}!

This application helps you analyze data and build machine learning models
using logistic regression for your psychology research.

Quick Start:
1. Load your CSV data using "Load CSV Data" button
2. View and explore your data
3. Check statistics and distributions
4. Train a logistic regression model for predictions

Features:
• Data loading and visualization
• Statistical analysis
• Logistic regression model training
• Real-time predictions
• Export results

Get started by loading your data!
"""
        self._append_output(welcome_msg)
    
    def _append_output(self, text: str):
        """Append text to output area."""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def _clear_output(self):
        """Clear output area."""
        self.output_text.delete(1.0, tk.END)
    
    def _load_data(self):
        """Load CSV data."""
        filename = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.df = pd.read_csv(filename)
                self.status_label.config(
                    text=f"Loaded: {len(self.df)} rows, {len(self.df.columns)} columns"
                )
                self._append_output(f"\n✓ Data loaded successfully from: {filename}")
                self._append_output(f"  Rows: {len(self.df)}, Columns: {len(self.df.columns)}")
                self._append_output(f"  Column names: {', '.join(self.df.columns)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {e}")
                logger.error(f"Data load error: {e}")
    
    def _view_data(self):
        """Display loaded data."""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        self._clear_output()
        self._append_output("=" * 60)
        self._append_output("DATA VIEW")
        self._append_output("=" * 60)
        self._append_output(f"\nFirst 10 rows:\n")
        self._append_output(str(self.df.head(10)))
        self._append_output(f"\n\nData types:\n")
        self._append_output(str(self.df.dtypes))
    
    def _show_statistics(self):
        """Show statistical summary."""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        self._clear_output()
        self._append_output("=" * 60)
        self._append_output("STATISTICAL SUMMARY")
        self._append_output("=" * 60)
        self._append_output(f"\nDescriptive Statistics:\n")
        self._append_output(str(self.df.describe()))
        self._append_output(f"\n\nMissing Values:\n")
        self._append_output(str(self.df.isnull().sum()))
    
    def _train_model(self):
        """Train a logistic regression model."""
        if self.df is None:
            messagebox.showwarning("Warning", "Please load data first")
            return
        
        self._clear_output()
        self._append_output("=" * 60)
        self._append_output("LOGISTIC REGRESSION MODEL TRAINING")
        self._append_output("=" * 60)
        
        try:
            # Example: assumes last column is target, others are features
            # This is a simplified example - real implementation would need user input
            if len(self.df.columns) < 2:
                messagebox.showerror("Error", "Data must have at least 2 columns (features and target)")
                return
            
            # Select numeric columns only
            numeric_df = self.df.select_dtypes(include=[np.number])
            
            if len(numeric_df.columns) < 2:
                messagebox.showerror("Error", "Data must have at least 2 numeric columns")
                return
            
            X = numeric_df.iloc[:, :-1]
            y = numeric_df.iloc[:, -1]
            
            # Check if target is suitable for classification
            if len(y.unique()) > 10:
                messagebox.showwarning(
                    "Warning",
                    "Target variable has many unique values. Logistic regression works best with categorical targets."
                )
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self._append_output("\n⏳ Training logistic regression model...")
            self.model = LogisticRegression(max_iter=1000, random_state=42)
            self.model.fit(X_train, y_train)
            
            # Predictions
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self._append_output(f"\n✓ Model trained successfully!")
            self._append_output(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            self._append_output(f"\nFeatures used: {', '.join(X.columns)}")
            self._append_output(f"Target variable: {numeric_df.columns[-1]}")
            self._append_output(f"\nTraining samples: {len(X_train)}")
            self._append_output(f"Test samples: {len(X_test)}")
            
            self.status_label.config(text=f"Model trained: {accuracy*100:.2f}% accuracy")
            
        except Exception as e:
            messagebox.showerror("Error", f"Model training failed: {e}")
            logger.error(f"Model training error: {e}")
    
    def _logout(self):
        """Logout and return to login screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            logger.info(f"User {self.user_data['username']} logged out")
            self.root.destroy()
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """Machine Learning & Data Analysis Application
Version 1.0

For IBDP Psychology Students
EE & IA Research Support

Features:
• Data loading and analysis
• Statistical summaries
• Logistic regression modeling
• Data visualization

Developed with Python, tkinter, pandas, and scikit-learn
"""
        messagebox.showinfo("About", about_text)
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
