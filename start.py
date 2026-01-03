"""
Football League Management System
Main Entry Point - Automated Setup and Menu System

This file automatically:
1. Checks and installs dependencies
2. Provides a menu-based interface
3. Allows running the application or tests
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print("  FOOTBALL LEAGUE MANAGEMENT SYSTEM")
    print("  Software Testing & Quality Assurance Project")
    print("=" * 70 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required dependencies from requirements.txt"""
    print("\n📦 Checking dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("⚠️  requirements.txt not found")
        return False
    
    try:
        # Try to import key packages
        import pytest
        print("✅ Dependencies already installed")
        return True
    except ImportError:
        print("📥 Installing dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"
            ])
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing dependencies: {e}")
            print("\nPlease install manually using:")
            print("   pip install -r requirements.txt")
            return False


def check_test_dependencies():
    """Check and install test dependencies"""
    try:
        import pytest
        return True
    except ImportError:
        print("\n📥 Installing test dependencies (pytest)...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-q", "pytest", "pytest-cov"
            ])
            print("✅ Test dependencies installed")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pytest. Please install manually:")
            print("   pip install pytest pytest-cov")
            return False


def run_application():
    """Run the main application"""
    print("\n" + "=" * 70)
    print("  Starting Application...")
    print("=" * 70 + "\n")
    
    # Check if CLI exists
    cli_path = Path("src/ui/cli.py")
    if cli_path.exists():
        try:
            subprocess.run([sys.executable, str(cli_path)])
        except Exception as e:
            print(f"❌ Error running application: {e}")
    else:
        # Fallback to demo script if available
        demo_files = ["quick_start.py", "member_d_demo.py"]
        for demo in demo_files:
            if Path(demo).exists():
                print(f"Running demo: {demo}")
                subprocess.run([sys.executable, demo])
                return
        
        print("⚠️  No application entry point found")
        print("\nAvailable modules:")
        print("  - member_a_Neel/league_manager.py")
        print("  - member_b_Mahir/fixture_scheduler.py")
        print("  - member_c_Abhishek/results_manager.py")
        print("  - member_d_dhawal/diagnostics_engine.py")


def run_tests():
    """Run the test suite"""
    print("\n" + "=" * 70)
    print("  TEST SUITE")
    print("=" * 70)
    
    if not check_test_dependencies():
        return
    
    print("\nTest Options:")
    print("  1. Run all tests")
    print("  2. Run Member A (Neel) tests")
    print("  3. Run Member B (Mahir) tests")
    print("  4. Run Member C (Abhishek) tests")
    print("  5. Run Member D (Dhawal) tests")
    print("  6. Run tests with coverage report")
    print("  0. Back to main menu")
    
    choice = input("\nEnter your choice (0-6): ").strip()
    
    test_commands = {
        "1": ["pytest", "tests/", "-v"],
        "2": ["pytest", "tests/member_a_neel/", "-v"],
        "3": ["pytest", "tests/member_b_mahir/", "-v"],
        "4": ["pytest", "tests/member_c_abhishek/", "-v"],
        "5": ["pytest", "tests/member_d_dhawal/", "-v"],
        "6": ["pytest", "tests/", "-v", "--cov", "--cov-report=term-missing", "--cov-report=html"]
    }
    
    if choice == "0":
        return
    
    if choice in test_commands:
        print(f"\n🧪 Running tests...\n")
        try:
            result = subprocess.run(test_commands[choice])
            if choice == "6":
                print("\n📊 Coverage report generated in: htmlcov/index.html")
            print("\n" + "=" * 70)
            if result.returncode == 0:
                print("✅ Tests completed successfully!")
            else:
                print("⚠️  Some tests failed. Check output above.")
            print("=" * 70)
        except FileNotFoundError:
            print("❌ pytest not found. Installing...")
            check_test_dependencies()
            print("Please try again.")
        except Exception as e:
            print(f"❌ Error running tests: {e}")
    else:
        print("❌ Invalid choice")
    
    input("\nPress Enter to continue...")


def show_project_info():
    """Show project information"""
    print("\n" + "=" * 70)
    print("  PROJECT INFORMATION")
    print("=" * 70)
    print("\n📚 Course: Software Testing & Quality Assurance")
    print("🎓 Project: Football League Management System")
    print("\n👥 Team Members:")
    print("   • Member A (Neel)     - League Manager Module")
    print("   • Member B (Mahir)    - Fixture Scheduler Module")
    print("   • Member C (Abhishek) - Results Manager Module")
    print("   • Member D (Dhawal)   - Diagnostics Engine Module")
    print("\n🧪 Testing Coverage:")
    print("   • Black-Box Testing (Boundary, Category, Random)")
    print("   • White-Box Testing (Basis Path, Branch Coverage)")
    print("   • Symbolic Execution & Concolic Testing")
    print("\n📂 Project Structure:")
    print("   • src/           - Source code (domain models, scheduling, UI)")
    print("   • tests/         - Comprehensive test suite (16 test files)")
    print("   • member_*/      - Individual member implementations")
    print("   • data/          - Sample data and diagnostics")
    print("   • docs/          - Documentation and sprint reports")
    print("\n📊 Test Statistics:")
    print("   • Total Test Files: 16")
    print("   • Total Test Cases: ~55")
    print("   • Testing Techniques: 7")
    print("   • All tests follow academic naming conventions")
    print("=" * 70)
    input("\nPress Enter to continue...")


def main_menu():
    """Display main menu and handle user choices"""
    while True:
        print("\n" + "=" * 70)
        print("  MAIN MENU")
        print("=" * 70)
        print("\n  1. Run Application")
        print("  2. Run Tests")
        print("  3. Project Information")
        print("  4. Exit")
        print("\n" + "=" * 70)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            run_application()
        elif choice == "2":
            run_tests()
        elif choice == "3":
            show_project_info()
        elif choice == "4":
            print("\n👋 Thank you for using Football League Management System!")
            print("=" * 70 + "\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")
            input("Press Enter to continue...")


def main():
    """Main entry point"""
    try:
        print_header()
        
        # Step 1: Check Python version
        check_python_version()
        
        # Step 2: Install dependencies
        if not install_dependencies():
            print("\n⚠️  Continuing without dependency installation...")
            print("Some features may not work properly.")
            input("\nPress Enter to continue...")
        
        # Step 3: Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
