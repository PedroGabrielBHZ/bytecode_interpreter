# Bytecode Interpreter

A stack-based bytecode interpreter and optimizer with a graphical interface, developed for the Compilers course.

## Features
- **Interpreter**: Executes stack-based bytecode with support for variables, arithmetic, control flow, and function calls.
- **Optimizer**: Removes redundant instructions and performs constant folding.
- **GUI**: User-friendly interface for loading, editing, optimizing, running, and saving .bc files.
- **Comprehensive Tests**: All logic is tested using Python's `unittest` framework.

## Project Structure
- `bytecode_interpreter.py`: Main interpreter logic
- `bytecode_optimizer.py`: Optimizer logic
- `bytecode_gui.py`: Tkinter GUI for the interpreter and optimizer
- `outputs/`: All generated/optimized files are saved here
- `tests/`: Contains `.bc` test files and Python unittests

## How to Use

### GUI
```bash
python bytecode_gui.py
```

### Command Line
Run a program from file:
```bash
python bytecode_interpreter.py tests/test1.bc
```
Run from standard input:
```bash
python bytecode_interpreter.py < tests/test1.bc
```

### Optimizer
```bash
python bytecode_optimizer.py tests/test_unoptimized.bc outputs/optimized.bc
```

## Running Tests

### All unittests (recommended)
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run a specific test file
```bash
python -m unittest tests.test_interpreter
```

## Test Files
See `tests/README.md` for details on all test cases and expected results.

## Requirements
- Python 3.7+
- No external dependencies required for core features

---

For more details, see the docstrings in each file and the test suite in `tests/`.
