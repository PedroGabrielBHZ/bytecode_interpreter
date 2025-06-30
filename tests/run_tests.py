import subprocess
import sys
import os


def run_test(test_file, expected_output):
    try:
        interpreter_path = os.path.join("..", "bytecode_interpreter.py")

        result = subprocess.run(
            [sys.executable, interpreter_path, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        actual_output = result.stdout.strip()
        expected_output = expected_output.strip()

        if actual_output == expected_output:
            print(f"✓ {test_file}: PASSED")
            return True
        else:
            print(f"✗ {test_file}: FAILED")
            print(f"  Expected: {expected_output}")
            print(f"  Actual:   {actual_output}")
            return False

    except Exception as e:
        print(f"✗ {test_file}: ERROR - {e}")
        return False


def main():
    """Runs all tests"""
    tests = [
        ("test1.bc", "20"),
        ("test2.bc", "1"),
        ("test3.bc", "5\n4\n3\n2\n1"),
        ("test4.bc", "7"),
        ("test5.bc", "10"),
    ]

    print("Running bytecode interpreter tests...")
    print("=" * 50)

    passed = 0
    total = len(tests)

    for test_file, expected in tests:
        if run_test(test_file, expected):
            passed += 1

    print("=" * 50)
    print(f"Result: {passed}/{total} tests passed")

    if passed == total:
        print("all tests pass")
        return 0
    else:
        print("some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
