# Bytecode Interpreter Tests

This directory contains all test files for the bytecode interpreter.

## Test Files

### Basic Tests (based on the specification):
- `test1.bc` - Basic operations with variables (result: 20)
- `test2.bc` - If/else conditional structure (result: 1)
- `test3.bc` - While loop structure (result: 5,4,3,2,1)
- `test4.bc` - Function call with parameters (result: 7)
- `test5.bc` - Function with return (result: 10)

### Special Tests:
- `test_input.bc` - Test with user input (READ)
- `test_unoptimized.bc` - Non-optimized code to demonstrate optimizations
- `test_optimized.bc` - Result of optimization

### Test Scripts:
- `run_tests.py` - Automated script to run all tests
- `test_input_example.py` - Example of how to test interactive input

## How to Run

### Run a specific test:
```bash
cd ..
python bytecode_interpreter.py tests/test1.bc
```

### Run all tests:
```bash
cd tests
python run_tests.py
```

### Test interactive input:
```bash
cd ..
echo "5" | python bytecode_interpreter.py tests/test_input.bc
```

### Test optimizer:
```bash
cd ..
python bytecode_optimizer.py tests/test_unoptimized.bc tests/test_optimized_new.bc
```

## Expected Results

| Test | Expected Result |
|------|----------------|
| test1.bc | 20 |
| test2.bc | 1 |
| test3.bc | 5<br>4<br>3<br>2<br>1 |
| test4.bc | 7 |
| test5.bc | 10 |
| test_input.bc (input: 5) | 25 |
