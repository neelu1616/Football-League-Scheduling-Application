"""
Test Runner for Football League Management System
Run all member tests or specific member tests
"""
import subprocess
import sys
import os

def run_member_tests(member_name=None):
    """Run tests for a specific member or all members"""
    # Change to script directory (project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Add project root to PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = script_dir + os.pathsep + env.get('PYTHONPATH', '')
    
    base_path = "tests"
    
    if member_name:
        test_path = os.path.join(base_path, f"member_{member_name}")
        if not os.path.exists(test_path):
            print(f"❌ Test directory not found: {test_path}")
            return False
        print(f"\n🧪 Running tests for Member {member_name.upper()}...\n")
        cmd = ["pytest", test_path, "-v", "--tb=short"]
    else:
        print("\n🧪 Running ALL member tests...\n")
        cmd = ["pytest", base_path, "-v", "--tb=short"]
    
    try:
        result = subprocess.run(cmd, check=False, env=env)
        return result.returncode == 0
    except FileNotFoundError:
        print("\n❌ pytest not found. Install it with: pip install pytest pytest-cov")
        return False

def run_with_coverage(member_name=None):
    """Run tests with coverage report"""
    # Change to script directory (project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Add project root to PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = script_dir + os.pathsep + env.get('PYTHONPATH', '')
    
    base_path = "tests"
    
    if member_name:
        test_path = os.path.join(base_path, f"member_{member_name}")
        module_map = {
            "a_neel": "member_a_Neel",
            "b_mahir": "member_b_Mahir",
            "c_abhishek": "member_c_Abhishek",
            "d_dhawal": "member_d_dhawal"
        }
        module = module_map.get(member_name, f"member_{member_name}")
        print(f"\n📊 Running tests with coverage for Member {member_name.upper()}...\n")
        cmd = ["pytest", test_path, "-v", "--cov", "--cov-report=term-missing", "--cov-report=html"]
    else:
        print("\n📊 Running ALL tests with coverage...\n")
        cmd = ["pytest", base_path, "-v", "--cov", "--cov-report=term-missing", "--cov-report=html"]
    
    try:
        result = subprocess.run(cmd, check=False, env=env)
        if result.returncode == 0:
            print("\n✅ Coverage report generated in htmlcov/index.html")
        return result.returncode == 0
    except FileNotFoundError:
        print("\n❌ pytest or pytest-cov not found. Install with: pip install pytest pytest-cov")
        return False

def main():
    print("=" * 60)
    print("Football League Management System - Test Runner")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python run_tests.py all              - Run all tests")
        print("  python run_tests.py a_neel           - Run Member A tests")
        print("  python run_tests.py b_mahir          - Run Member B tests")
        print("  python run_tests.py c_abhishek       - Run Member C tests")
        print("  python run_tests.py d_dhawal         - Run Member D tests")
        print("  python run_tests.py coverage         - Run all with coverage")
        print("  python run_tests.py coverage a_neel  - Run Member A with coverage")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "all":
        success = run_member_tests()
    elif command == "coverage":
        member = sys.argv[2] if len(sys.argv) > 2 else None
        success = run_with_coverage(member)
    elif command in ["a_neel", "b_mahir", "c_abhishek", "d_dhawal"]:
        success = run_member_tests(command)
    else:
        print(f"\n❌ Unknown command: {command}")
        print("Use 'all', 'coverage', or a member name (a_neel, b_mahir, c_abhishek, d_dhawal)")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ Tests completed successfully!")
    else:
        print("❌ Some tests failed. Check output above.")
    print("=" * 60 + "\n")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
