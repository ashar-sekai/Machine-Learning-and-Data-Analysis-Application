# User Guide: ML Data Analysis Application

## Table of Contents
1. [Getting Started](#getting-started)
2. [Login System](#login-system)
3. [Registration](#registration)
4. [Main Application](#main-application)
5. [Data Analysis Features](#data-analysis-features)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### First Launch

Run the application:
```bash
python main.py
```

---

## Login System

### Login Screen

When you first launch the application, you'll see the **Login Dialog**:

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║    Machine Learning & Data Analysis               ║
║    Please login to continue                       ║
║                                                   ║
║    Username or Email:                             ║
║    [____________________________________]          ║
║                                                   ║
║    Password:                                      ║
║    [____________________________________]          ║
║                                                   ║
║    ☐ Remember me                                  ║
║                                                   ║
║              [      Login      ]                  ║
║                                                   ║
║    Don't have an account? Sign up                 ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Features:**
- Enter your username OR email address
- Password field is masked for security
- "Remember me" checkbox for future convenience
- Click "Sign up" link to create a new account

**Keyboard Shortcuts:**
- Press `Enter` to login after filling the form

---

## Registration

### Registration Screen

Click "Sign up" on the login screen to open the **Registration Dialog**:

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║           Create New Account                      ║
║                                                   ║
║    Username:                                      ║
║    [____________________________________]          ║
║    (3-30 characters, alphanumeric and _)         ║
║                                                   ║
║    Email:                                         ║
║    [____________________________________]          ║
║                                                   ║
║    Password:                                      ║
║    [____________________________________]          ║
║    (Min 8 chars, 1 upper, 1 lower, 1 digit)      ║
║                                                   ║
║    Confirm Password:                              ║
║    [____________________________________]          ║
║                                                   ║
║              [    Register    ]                   ║
║              [     Cancel     ]                   ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one digit (0-9)

**Example Valid Passwords:**
- `MyPass123`
- `SecurePass1`
- `Psychology2024`

**Username Rules:**
- 3-30 characters
- Letters, numbers, and underscores only
- Must be unique

**Email Rules:**
- Valid email format
- Must be unique

---

## Main Application

### Application Layout

After successful login, the main application opens:

```
╔═══════════════════════════════════════════════════════════════════════╗
║ File    Analysis    Help           Welcome, username!    [ Logout ]   ║
╠═══════════════════╦═══════════════════════════════════════════════════╣
║                   ║                                                   ║
║   Controls        ║              Output                               ║
║ ┌───────────────┐ ║                                                   ║
║ │               │ ║  ╔══════════════════════════════════════════════╗║
║ │ Load CSV Data │ ║  ║ Machine Learning & Data Analysis             ║║
║ │               │ ║  ║ For IBDP Psychology Students (EE & IA)       ║║
║ └───────────────┘ ║  ╚══════════════════════════════════════════════╝║
║                   ║                                                   ║
║ ┌───────────────┐ ║  Welcome, username!                              ║
║ │   View Data   │ ║                                                   ║
║ └───────────────┘ ║  This application helps you analyze data...      ║
║                   ║                                                   ║
║ ┌───────────────┐ ║  Quick Start:                                    ║
║ │Show Statistics│ ║  1. Load your CSV data                           ║
║ └───────────────┘ ║  2. View and explore your data                   ║
║                   ║  3. Check statistics                              ║
║ ┌───────────────┐ ║  4. Train a logistic regression model            ║
║ │Train ML Model │ ║                                                   ║
║ └───────────────┘ ║  Features:                                       ║
║ ═════════════════ ║  • Data loading and visualization                ║
║                   ║  • Statistical analysis                           ║
║ Status:           ║  • Logistic regression model training            ║
║ No data loaded    ║  • Real-time predictions                          ║
║                   ║                                                   ║
╚═══════════════════╩═══════════════════════════════════════════════════╝
```

**Components:**

1. **Menu Bar:**
   - File: Load Data, Logout, Exit
   - Analysis: View Data, Statistics, Train Model
   - Help: About

2. **Controls Panel (Left):**
   - Load CSV Data button
   - View Data button
   - Show Statistics button
   - Train ML Model button
   - Status indicator

3. **Output Panel (Right):**
   - Displays results, data, statistics
   - Scrollable text area

---

## Data Analysis Features

### 1. Loading Data

**Steps:**
1. Click "Load CSV Data" button
2. Select your CSV file from the file dialog
3. The status will update showing rows and columns loaded

**Supported Format:**
- CSV files (.csv)
- First row should contain column headers
- Data can be numeric or categorical

**Example Data Structure:**
```csv
participant_id,stress_level,study_hours,sleep_hours,exam_anxiety,performance
1,7,3,6,8,0
2,5,5,7,6,1
3,8,2,5,9,0
```

### 2. Viewing Data

**What You'll See:**
- First 10 rows of your dataset
- Column names and data types
- Quick overview of data structure

**Example Output:**
```
============================================================
DATA VIEW
============================================================

First 10 rows:

   participant_id  stress_level  study_hours  sleep_hours  exam_anxiety  performance
0               1             7            3            6             8            0
1               2             5            5            7             6            1
2               3             8            2            5             9            0
...

Data types:

participant_id    int64
stress_level      int64
study_hours       int64
...
```

### 3. Statistical Analysis

**Provides:**
- Descriptive statistics (mean, std, min, max, quartiles)
- Missing value counts
- Data distribution insights

**Example Output:**
```
============================================================
STATISTICAL SUMMARY
============================================================

Descriptive Statistics:

       participant_id  stress_level  study_hours
count            30.0         30.00        30.00
mean             15.5          5.63         4.57
std               8.8          2.21         2.13
min               1.0          2.00         1.00
25%               8.0          4.00         3.00
50%              15.5          5.50         4.50
75%              23.0          7.25         6.25
max              30.0          9.00         9.00

Missing Values:

participant_id    0
stress_level      0
study_hours       0
...
```

### 4. Training ML Models

**Logistic Regression:**
- Automatically detects numeric columns
- Uses last column as target variable
- Splits data into training (80%) and test (20%) sets
- Reports accuracy and performance metrics

**Example Output:**
```
============================================================
LOGISTIC REGRESSION MODEL TRAINING
============================================================

⏳ Training logistic regression model...

✓ Model trained successfully!

Accuracy: 0.8333 (83.33%)

Features used: stress_level, study_hours, sleep_hours, exam_anxiety
Target variable: performance

Training samples: 24
Test samples: 6
```

---

## Troubleshooting

### Common Issues

#### "Invalid username or password"
- Check that your username/email is correct
- Verify your password (remember it's case-sensitive)
- If you forgot your password, contact support

#### "Username already exists"
- Choose a different username
- Username must be unique in the system

#### "Email already exists"
- This email is already registered
- Use a different email address
- If this is your email, login instead of registering

#### "Password must be at least 8 characters long"
- Your password is too short
- Make it at least 8 characters
- Include uppercase, lowercase, and digits

#### "Failed to load data"
- Ensure the file is in CSV format
- Check that the file is not corrupted
- Verify the file has proper column headers

#### "Data must have at least 2 numeric columns"
- Your dataset needs numeric data for ML
- Ensure at least 2 columns contain numbers
- Check that target variable is suitable for classification

### Database Location

The application stores user data in:
- **Linux/Mac:** `~/.ml_data_analysis_app/users.db`
- **Windows:** `C:\Users\<username>\.ml_data_analysis_app\users.db`

### Security Notes

- Passwords are hashed using bcrypt (never stored in plain text)
- Database uses parameterized queries (SQL injection protected)
- All inputs are validated before processing
- User sessions are managed securely

---

## Tips for Psychology Students

### For Extended Essays (EE)

1. **Data Collection:**
   - Export survey data as CSV
   - Ensure clean, properly formatted data
   - Include all relevant variables

2. **Analysis:**
   - Use statistics feature for descriptive analysis
   - Train models to find patterns
   - Include accuracy metrics in your report

3. **Reporting:**
   - Copy output directly to your report
   - Include data visualizations
   - Report model accuracy and limitations

### For Internal Assessments (IA)

1. **Quick Analysis:**
   - Load your experimental data
   - Get statistics quickly
   - Identify trends and patterns

2. **Model Training:**
   - Use logistic regression for binary outcomes
   - Report prediction accuracy
   - Discuss model performance

---

## Support

For issues or questions:
1. Check this guide first
2. Review the README.md
3. Open an issue on GitHub
4. Contact the development team

**HAVE FUN AND ENJOY YOUR RESEARCH!** 🎓📊🧠
