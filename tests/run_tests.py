#!/usr/bin/env python3
"""
Script de teste para o interpretador bytecode
"""

import subprocess
import sys
import os


def run_test(test_file, expected_output):
    """Executa um teste e verifica o resultado"""
    try:
        # Caminho para o interpretador no diretório pai
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
    """Executa todos os testes"""
    tests = [
        ("test1.bc", "20"),
        ("test2.bc", "1"),
        ("test3.bc", "5\n4\n3\n2\n1"),
        ("test4.bc", "7"),
        ("test5.bc", "10"),
    ]

    print("Executando testes do interpretador bytecode...")
    print("=" * 50)

    passed = 0
    total = len(tests)

    for test_file, expected in tests:
        if run_test(test_file, expected):
            passed += 1

    print("=" * 50)
    print(f"Resultado: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 Todos os testes passaram!")
        return 0
    else:
        print("❌ Alguns testes falharam.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
