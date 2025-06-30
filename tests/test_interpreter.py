import unittest
from bytecode_interpreter import BytecodeInterpreter
from unittest.mock import patch
import io
import os


class TestBytecodeInterpreter(unittest.TestCase):
    def test_push_and_pop(self):
        code = """
        PUSH 10
        PUSH 20
        POP
        """
        interp = BytecodeInterpreter()
        interp.load_program(code)
        interp.run()
        self.assertEqual(interp.stack, [10])

    def test_add(self):
        code = """
        PUSH 2
        PUSH 3
        ADD
        """
        interp = BytecodeInterpreter()
        interp.load_program(code)
        interp.run()
        self.assertEqual(interp.stack, [5])

    def test_store_and_load(self):
        code = """
        PUSH 7
        STORE x
        LOAD x
        """
        interp = BytecodeInterpreter()
        interp.load_program(code)
        interp.run()
        self.assertEqual(interp.stack, [7])
        self.assertEqual(interp.variables["x"], 7)

    def run_bc_file_and_capture(self, filename):
        path = os.path.join(os.path.dirname(__file__), filename)
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        interp = BytecodeInterpreter()
        interp.load_program(code)
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            interp.run()
            return mock_stdout.getvalue().strip()

    def test_bc_files(self):
        cases = [
            ("test1.bc", "20"),
            ("test2.bc", "1"),
            ("test3.bc", "5\n4\n3\n2\n1"),
            ("test4.bc", "7"),
            ("test5.bc", "10"),
        ]
        for fname, expected in cases:
            with self.subTest(fname=fname):
                output = self.run_bc_file_and_capture(fname)
                self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
