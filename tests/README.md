# Bytecode Interpreter Tests

This directory contains all test files and unittests for the bytecode interpreter and optimizer.

## Test Files

### Bytecode Programs:
- `test1.bc` - Basic operations with variables (expected output: 20)
- `test2.bc` - If/else conditional structure (expected output: 1)
- `test3.bc` - While loop structure (expected output: 5,4,3,2,1)
- `test4.bc` - Function call with parameters (expected output: 7)
- `test5.bc` - Function with return (expected output: 10)
- `test_input.bc` - Test with user input (READ)
- `test_unoptimized.bc` - Non-optimized code for optimizer tests
- `test_optimized.bc` - Example of optimized output

### Python Test Files:
- `test_interpreter.py` - Unittests for the interpreter, including all .bc files above
- (Add more `test_*.py` files for additional tests)

## How to Run Tests

### Run all unittests (recommended):
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run a specific test file:
```bash
python -m unittest tests.test_interpreter
```

### Run a .bc file manually:
```bash
python bytecode_interpreter.py tests/test1.bc
```

### Run the optimizer:
```bash
python bytecode_optimizer.py tests/test_unoptimized.bc outputs/optimized.bc
```

## Expected Results

| Test         | Expected Output      |
|--------------|---------------------|
| test1.bc     | 20                  |
| test2.bc     | 1                   |
| test3.bc     | 5\n4\n3\n2\n1        |
| test4.bc     | 7                   |
| test5.bc     | 10                  |
| test_input.bc (input: 5) | 25      |

## Notes
- All output files are saved in the `outputs/` directory.
- The GUI can also be used to run and optimize tests interactively.
