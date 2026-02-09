# Machine Learning and Data Analysis Application

An open source Data Analysis application catering to IBDP Psychology Students for their Extended Essays (EE) and Internal Assessments (IA). However, it can still be used for professional analysis of both static and real-time data along with predictions and model training using logistic regression (supervised learning).

## Features

- **User Authentication System**: Secure login with password hashing using bcrypt
- **Data Analysis**: Load and analyze CSV data files
- **Statistical Analysis**: View descriptive statistics and data distributions
- **Machine Learning**: Train logistic regression models for classification
- **User-Friendly Interface**: Clean tkinter-based GUI
- **Secure Database**: SQLite database with proper security measures

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ashar-sekai/Machine-Learning-and-Data-Analysis-Application.git
cd Machine-Learning-and-Data-Analysis-Application
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### First Time Setup

1. When you first launch the application, you'll see the login screen
2. Click "Sign up" to create a new account
3. Enter your desired username (3-30 characters, alphanumeric and underscores)
4. Enter a valid email address
5. Create a strong password (minimum 8 characters, must contain uppercase, lowercase, and digit)
6. Click "Register" to create your account
7. After successful registration, login with your credentials

### Using the Application

1. **Login**: Enter your username/email and password
2. **Load Data**: Click "Load CSV Data" to import your dataset
3. **View Data**: Explore your data and check data types
4. **Show Statistics**: Get descriptive statistics and check for missing values
5. **Train Model**: Train a logistic regression model on your data
6. **Logout**: Click the logout button when done

## Project Structure

```
Machine-Learning-and-Data-Analysis-Application/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── database/
│   ├── __init__.py
│   └── db_manager.py      # Database management
├── auth/
│   ├── __init__.py
│   └── authentication.py  # User authentication and password hashing
├── ui/
│   ├── __init__.py
│   ├── login_dialog.py    # Login interface
│   ├── register_dialog.py # Registration interface
│   └── main_app.py        # Main application interface
└── models/
    └── __init__.py
```

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **SQL Injection Prevention**: Parameterized queries throughout
- **Input Validation**: Comprehensive validation for all user inputs
- **Session Management**: Proper user session handling
- **Active Account Status**: User accounts can be deactivated

## Database Schema

The application uses SQLite with the following users table:

| Column        | Type    | Description                     |
|---------------|---------|--------------------------------|
| id            | INTEGER | Primary key, auto-increment    |
| username      | TEXT    | Unique username                |
| email         | TEXT    | Unique email address           |
| password_hash | TEXT    | Bcrypt hashed password         |
| created_at    | TEXT    | Account creation timestamp     |
| last_login    | TEXT    | Last login timestamp           |
| is_active     | INTEGER | Account active status (1/0)    |

## Technical Details

- **GUI Framework**: tkinter (Python's standard GUI toolkit)
- **Database**: SQLite3 (built-in with Python)
- **Password Hashing**: bcrypt
- **Data Analysis**: pandas, numpy
- **Machine Learning**: scikit-learn (Logistic Regression)
- **Visualization**: matplotlib, seaborn

## For IBDP Psychology Students

This application is specifically designed to help you with:

- **Extended Essays (EE)**: Analyze your research data and build predictive models
- **Internal Assessments (IA)**: Process survey data and generate statistical insights
- **Data Organization**: Keep your research data organized and easily accessible
- **Statistical Analysis**: Get quick descriptive statistics for your reports
- **Predictions**: Use logistic regression for binary classification tasks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for educational purposes.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**HAVE FUN AND ENJOY!** 🎓📊🧠
