"""
Verification script to ensure all components can be imported and initialized.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def verify_imports():
    """Verify all modules can be imported."""
    print("=" * 60)
    print("Verifying Module Imports")
    print("=" * 60)
    
    modules = [
        ("database.db_manager", "DatabaseManager"),
        ("auth.authentication", "AuthenticationManager"),
    ]
    
    # UI modules require tkinter which may not be available in headless environments
    ui_modules = [
        ("ui.login_dialog", "LoginDialog"),
        ("ui.register_dialog", "RegisterDialog"),
        ("ui.main_app", "MainApplication"),
    ]
    
    all_ok = True
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"✗ {module_name}.{class_name}: {e}")
            all_ok = False
    
    # Try UI modules but don't fail if tkinter is not available
    for module_name, class_name in ui_modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
        except ImportError as e:
            if "tkinter" in str(e).lower():
                print(f"⚠ {module_name}.{class_name} (tkinter not available - OK in headless)")
            else:
                print(f"✗ {module_name}.{class_name}: {e}")
                all_ok = False
        except Exception as e:
            print(f"✗ {module_name}.{class_name}: {e}")
            all_ok = False
    
    return all_ok

def verify_structure():
    """Verify project structure."""
    print("\n" + "=" * 60)
    print("Verifying Project Structure")
    print("=" * 60)
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "database/__init__.py",
        "database/db_manager.py",
        "auth/__init__.py",
        "auth/authentication.py",
        "ui/__init__.py",
        "ui/login_dialog.py",
        "ui/register_dialog.py",
        "ui/main_app.py",
        "models/__init__.py",
        "sample_data.csv",
        "test_auth.py",
    ]
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def verify_dependencies():
    """Verify required packages are installed."""
    print("\n" + "=" * 60)
    print("Verifying Dependencies")
    print("=" * 60)
    
    dependencies = [
        "bcrypt",
        "pandas",
        "numpy",
        "sklearn",
        "matplotlib",
        "seaborn",
    ]
    
    all_installed = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} (not installed)")
            all_installed = False
    
    return all_installed

def main():
    """Run all verifications."""
    results = []
    
    results.append(("Imports", verify_imports()))
    results.append(("Structure", verify_structure()))
    results.append(("Dependencies", verify_dependencies()))
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20s}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n✓ ALL VERIFICATIONS PASSED!")
        print("\nThe application is ready to use. Run with:")
        print("  python main.py")
    else:
        print("\n✗ SOME VERIFICATIONS FAILED")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
