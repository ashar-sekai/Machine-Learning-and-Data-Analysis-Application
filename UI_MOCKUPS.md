# UI Screenshots and Mockups

This document provides visual representations of the application's user interface.

## Login Screen

```
┌─────────────────────────────────────────────────────────┐
│  ML Data Analysis - Login                         [ × ] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│                                                         │
│        Machine Learning & Data Analysis                 │
│        Please login to continue                         │
│                                                         │
│                                                         │
│    Username or Email:                                   │
│    ┌─────────────────────────────────────────────┐    │
│    │                                              │    │
│    └─────────────────────────────────────────────┘    │
│                                                         │
│    Password:                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ ••••••••                                     │    │
│    └─────────────────────────────────────────────┘    │
│                                                         │
│    ☐ Remember me                                        │
│                                                         │
│              ┌──────────────────┐                      │
│              │      Login       │                      │
│              └──────────────────┘                      │
│                                                         │
│    Don't have an account? Sign up                      │
│                          ────────                       │
│                                                         │
└─────────────────────────────────────────────────────────┘

Features:
• Clean, centered design
• Password masking for security
• Remember me functionality
• Clickable "Sign up" link (blue, underlined)
• Enter key submits the form
```

## Registration Screen

```
┌─────────────────────────────────────────────────────────┐
│  ML Data Analysis - Register                      [ × ] │
├─────────────────────────────────────────────────────────┤
│                                                         │
│             Create New Account                          │
│                                                         │
│                                                         │
│    Username:                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │                                              │    │
│    └─────────────────────────────────────────────┘    │
│    (3-30 characters, alphanumeric and underscores)     │
│                                                         │
│    Email:                                               │
│    ┌─────────────────────────────────────────────┐    │
│    │                                              │    │
│    └─────────────────────────────────────────────┘    │
│                                                         │
│    Password:                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ ••••••••                                     │    │
│    └─────────────────────────────────────────────┘    │
│    (Min 8 chars, 1 uppercase, 1 lowercase, 1 digit)    │
│                                                         │
│    Confirm Password:                                    │
│    ┌─────────────────────────────────────────────┐    │
│    │ ••••••••                                     │    │
│    └─────────────────────────────────────────────┘    │
│                                                         │
│              ┌──────────────────┐                      │
│              │    Register      │                      │
│              └──────────────────┘                      │
│              ┌──────────────────┐                      │
│              │     Cancel       │                      │
│              └──────────────────┘                      │
│                                                         │
└─────────────────────────────────────────────────────────┘

Features:
• Clear input requirements shown below fields
• Password confirmation field
• Cancel button to return to login
• Visual feedback on requirements (gray text)
```

## Main Application Window

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  ML Data Analysis Application                                              [ _ ][ □ ][ × ] │
├──────────────────────────────────────────────────────────────────────────────────────┤
│ File    Analysis    Help                        Welcome, username!      [ Logout ]   │
├──────────────────────┬───────────────────────────────────────────────────────────────┤
│                      │                                                               │
│   Controls           │                        Output                                 │
│ ┌──────────────────┐ │  ╔═══════════════════════════════════════════════════════╗  │
│ │                  │ │  ║ Machine Learning & Data Analysis Application          ║  │
│ │  Load CSV Data   │ │  ║ For IBDP Psychology Students (EE & IA)                ║  │
│ │                  │ │  ╚═══════════════════════════════════════════════════════╝  │
│ └──────────────────┘ │                                                               │
│                      │  Welcome, username!                                           │
│ ┌──────────────────┐ │                                                               │
│ │                  │ │  This application helps you analyze data and build            │
│ │   View Data      │ │  machine learning models using logistic regression            │
│ │                  │ │  for your psychology research.                                │
│ └──────────────────┘ │                                                               │
│                      │  Quick Start:                                                 │
│ ┌──────────────────┐ │  1. Load your CSV data using "Load CSV Data" button          │
│ │                  │ │  2. View and explore your data                                │
│ │ Show Statistics  │ │  3. Check statistics and distributions                        │
│ │                  │ │  4. Train a logistic regression model for predictions         │
│ └──────────────────┘ │                                                               │
│                      │  Features:                                                    │
│ ┌──────────────────┐ │  • Data loading and visualization                             │
│ │                  │ │  • Statistical analysis                                       │
│ │ Train ML Model   │ │  • Logistic regression model training                         │
│ │                  │ │  • Real-time predictions                                      │
│ └──────────────────┘ │  • Export results                                             │
│ ──────────────────── │                                                               │
│                      │  Get started by loading your data!                            │
│ Status:              │                                                               │
│ No data loaded       │                                                               │
│                      │                                                               │
│                      │                                                               │
│                      │                                                               │
│                      │                                                               │
├──────────────────────┴───────────────────────────────────────────────────────────────┤
│ Ready                                                                                 │
└──────────────────────────────────────────────────────────────────────────────────────┘

Layout:
• Menu bar at top (File, Analysis, Help)
• User welcome message and logout button
• Left panel: Control buttons
• Right panel: Scrollable output area
• Status indicator at bottom of left panel
```

## Application Flow Diagram

```
┌─────────────────┐
│  Application    │
│     Start       │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Show Login     │
│     Dialog      │
└────────┬────────┘
         │
         ├─────────────────┐
         │                 │
         v                 v
    ┌─────────┐      ┌──────────┐
    │  Login  │      │  Sign Up │
    └────┬────┘      └─────┬────┘
         │                 │
         │    ┌────────────┘
         │    │
         v    v
    ┌─────────────┐
    │ Authenticate│
    │   User      │
    └──────┬──────┘
           │
     ┌─────┴─────┐
     │           │
     v           v
  Success      Fail
     │           │
     v           └──────┐
┌─────────────┐         │
│    Main     │         │
│ Application │         │
└──────┬──────┘         │
       │                │
       v                │
  ┌─────────┐          │
  │ Logout? │          │
  └────┬────┘          │
       │               │
    ┌──┴──┐            │
    │ Yes │            │
    └──┬──┘            │
       │               │
       v               │
  Back to Login ◄──────┘
```

## Sample Data Loading

```
After clicking "Load CSV Data" and selecting a file:

╔═══════════════════════════════════════════════════════════╗
║                        Output                             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║ ✓ Data loaded successfully from: sample_data.csv         ║
║   Rows: 30, Columns: 6                                    ║
║   Column names: participant_id, stress_level,             ║
║   study_hours, sleep_hours, exam_anxiety, performance     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Status updates to: "Loaded: 30 rows, 6 columns"
```

## Sample Statistics Output

```
After clicking "Show Statistics":

╔═══════════════════════════════════════════════════════════╗
║ STATISTICAL SUMMARY                                       ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║ Descriptive Statistics:                                   ║
║                                                           ║
║        participant_id  stress_level  study_hours  ...     ║
║ count          30.000        30.000       30.000         ║
║ mean           15.500         5.633        4.567         ║
║ std             8.803         2.211        2.134         ║
║ min             1.000         2.000        1.000         ║
║ 25%             8.000         4.000        3.000         ║
║ 50%            15.500         5.500        4.500         ║
║ 75%            23.000         7.250        6.250         ║
║ max            30.000         9.000        9.000         ║
║                                                           ║
║ Missing Values:                                           ║
║                                                           ║
║ participant_id    0                                       ║
║ stress_level      0                                       ║
║ study_hours       0                                       ║
║ sleep_hours       0                                       ║
║ exam_anxiety      0                                       ║
║ performance       0                                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## Sample Model Training Output

```
After clicking "Train ML Model":

╔═══════════════════════════════════════════════════════════╗
║ LOGISTIC REGRESSION MODEL TRAINING                        ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║ ⏳ Training logistic regression model...                  ║
║                                                           ║
║ ✓ Model trained successfully!                            ║
║                                                           ║
║ Accuracy: 0.8333 (83.33%)                                ║
║                                                           ║
║ Features used: stress_level, study_hours, sleep_hours,   ║
║                exam_anxiety                               ║
║ Target variable: performance                              ║
║                                                           ║
║ Training samples: 24                                      ║
║ Test samples: 6                                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Status updates to: "Model trained: 83.33% accuracy"
```

## Color Scheme (Conceptual)

- **Background**: White/Light Gray
- **Text**: Dark Gray/Black
- **Buttons**: Green (#4CAF50) with white text
- **Links**: Blue (#0066CC), underlined on hover
- **Input Fields**: White with gray border
- **Headers**: Bold, dark text
- **Hints**: Light gray text (smaller font)

## Typography

- **Headers**: Arial, 14pt, Bold
- **Subheaders**: Arial, 12pt, Bold
- **Body Text**: Arial, 10pt
- **Hints**: Arial, 8pt
- **Output**: Courier, 10pt (monospace for data)

## Responsive Elements

All dialogs:
- Centered on screen at launch
- Modal (block interaction with parent)
- Non-resizable for consistent layout
- Appropriate default focus (username/email field)
- Enter key submits form
- ESC key cancels (where applicable)

---

## Notes for Developers

When running the application:
1. Login dialog appears first (modal)
2. User must login or register
3. Main application only opens after successful authentication
4. Logout returns to login dialog
5. All windows are properly centered
6. Tab navigation works between fields
7. Enter key shortcuts are implemented

**The UI is built with tkinter for maximum compatibility across Windows, Mac, and Linux systems.**
