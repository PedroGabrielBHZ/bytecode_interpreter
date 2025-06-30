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

### Edge Case Tests:
- `test_stack_underflow.bc` - Arithmetic with insufficient stack operands
- `test_division_by_zero.bc` - Division by zero error handling
- `test_modulo_by_zero.bc` - Modulo by zero error handling
- `test_undefined_variable.bc` - Loading undefined variables
- `test_undefined_label.bc` - Jumping to undefined labels
- `test_jz_empty_stack.bc` - Conditional jump with empty stack
- `test_undefined_function.bc` - Calling undefined functions
- `test_return_without_call.bc` - Return without matching call
- `test_dup_empty_stack.bc` - Duplicate operation on empty stack
- `test_print_empty_stack.bc` - Print operation on empty stack
- `test_no_halt.bc` - Program without HALT instruction
- `test_empty_stack_arithmetic.bc` - Arithmetic on completely empty stack
- `test_negative_numbers.bc` - Operations with negative numbers (should work)
- `test_large_numbers.bc` - Operations with large numbers (should work)
- `test_nested_calls.bc` - Nested function calls (should work)
- `test_empty_program.bc` - Empty program test
- `test_infinite_loop.bc` - Infinite loop detection test
- `test_deep_stack.bc` - Deep stack operations test
- `test_invalid_opcodes.bc` - Invalid opcode handling test  
- `test_whitespace_cases.bc` - Whitespace and formatting edge cases

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

### Edge Case Test Results:
| Test                         | Expected Behavior        |
|------------------------------|-------------------------|
| test_stack_underflow.bc      | Error handling          |
| test_division_by_zero.bc     | Error handling          |
| test_modulo_by_zero.bc       | Error handling          |
| test_undefined_variable.bc   | Error handling          |
| test_undefined_label.bc      | Error handling          |
| test_jz_empty_stack.bc       | Error handling          |
| test_undefined_function.bc   | Error handling          |
| test_return_without_call.bc  | Error handling          |
| test_dup_empty_stack.bc      | Error handling          |
| test_print_empty_stack.bc    | Prints 0 or handles     |
| test_no_halt.bc              | Runs to completion      |
| test_empty_stack_arithmetic.bc | Error handling        |
| test_negative_numbers.bc     | Output: 300             |
| test_large_numbers.bc        | Large number result     |
| test_nested_calls.bc         | Output: 15              |
| test_empty_program.bc        | Handles empty program   |
| test_infinite_loop.bc        | Detects/prevents loops  |
| test_deep_stack.bc           | Handles deep operations |
| test_invalid_opcodes.bc      | Reports invalid opcodes |
| test_whitespace_cases.bc     | Handles formatting      |

## Notes
- All output files are saved in the `outputs/` directory.
- The GUI can also be used to run and optimize tests interactively.
