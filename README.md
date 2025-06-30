# Bytecode Interpreter

This is a stack-based bytecode interpreter, developed as a practical assignment for the Compilers course.

## Graphical User Interface (GUI)

The project includes a user-friendly graphical interface to facilitate the use of the interpreter and optimizer.

### How to use the GUI:
```bash
python bytecode_gui.py
```

### GUI Features:

- **Load .bc file**: Opens a bytecode file and displays its content in an editable text box
- **Run Optimizer**: Processes the loaded code through the optimizer and shows the result
- **Compare**: Opens a window to compare the original and optimized code side by side
- **Save Optimized**: Saves the optimized code to a new file
- **Run Original**: Runs the original program and shows the output
- **Run Optimized**: Runs the optimized program and shows the output
- **Input Field**: Allows you to provide input for programs that use `READ`
- **Clear Outputs**: Clears the program output area

The interface is divided into three main areas:
- **Original Code** (editable)
- **Optimized Code** (read-only)
- **Program Output** (with input field)

## How to Use (Command Line)

### Run from file:
```bash
python bytecode_interpreter.py test1.bc
```

### Run from standard input:
```bash
python bytecode_interpreter.py < test1.bc
```

or

```bash
cat test1.bc | python bytecode_interpreter.py
```

## Optimizer (Extra Feature - 4pts)

The project includes an optimizer that removes redundant instructions without changing the semantics:

### How to use the optimizer:
```bash
python bytecode_optimizer.py input.bc output.bc
```

### Implemented Optimizations:

1. **Remove redundant PUSH/POP**: Removes `PUSH value` sequences immediately followed by `POP`
2. **Remove redundant LOADs**: Removes consecutive LOADs of the same variable, replacing with `DUP`
3. **Dead code elimination**: Removes code after `HALT`, `RET`, or unconditional `JMP`
4. **Constant folding**: Computes arithmetic operations with constants at compile time

### Example:
```bash
python bytecode_optimizer.py test_unoptimized.bc test_optimized.bc
```

## Project Files

- `bytecode_interpreter.py` - Main interpreter
- `bytecode_optimizer.py` - Code optimizer
- `bytecode_gui.py` - Graphical interface
- `run_tests.py` - Script to run all tests
- `tests/` - Directory with test files

## Expected Test Results

| Test | Expected Result |
|------|----------------|
| test1.bc | 20 |
| test2.bc | 1 |
| test3.bc | 5<br>4<br>3<br>2<br>1 |
| test4.bc | 7 |
| test5.bc | 10 |
| test_input.bc (input: 5) | 25 |

## Run all tests

```bash
python run_tests.py
```

## Supported Instructions

### Arithmetic and Stack Operations:
- `PUSH <val>` - Pushes a value onto the stack
- `POP` - Pops a value from the stack
- `ADD` - Adds the top two values on the stack
- `SUB` - Subtracts the top two values on the stack
- `MUL` - Multiplies the top two values on the stack
- `DIV` - Divides the top two values on the stack
- `MOD` - Modulo of the top two values on the stack
- `NEG` - Negates the top value on the stack
- `DUP` - Duplicates the top value on the stack

### Variables:
- `STORE <var>` - Stores the top value of the stack in a variable
- `LOAD <var>` - Loads the value of a variable onto the stack

### Control Flow:
- `JMP <addr>` - Jumps to the address/label
- `JZ <addr>` - Jumps if the top of the stack is zero
- `JNZ <addr>` - Jumps if the top of the stack is not zero
- `HALT` - Stops execution

### Comparison:
- `EQ` - Checks equality
- `NEQ` - Checks inequality
- `LT` - Less than
- `GT` - Greater than
- `LE` - Less than or equal
- `GE` - Greater than or equal

### Functions and I/O:
- `CALL <addr>` - Calls a function at the address/label
- `RET` - Returns from a function
- `PRINT` - Prints the top value of the stack
- `READ` - Reads a value from standard input

### Labels:
- `LABEL:` - Defines a label for jumps and calls

## Usage Examples

### Basic test:
```bash
python bytecode_interpreter.py test1.bc
```
Expected output: `20`

### Conditional test:
```bash
python bytecode_interpreter.py test2.bc
```
Expected output: `1`

### Loop test:
```bash
python bytecode_interpreter.py test3.bc
```
Expected output:
```
5
4
3
2
1
```
