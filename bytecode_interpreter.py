import sys
from typing import List, Dict, Tuple, Optional


class BytecodeInterpreter:

    def __init__(self):
        """
        Initializes the bytecode interpreter with the following attributes:
        - stack: A list used as the operand stack for integer values.
        - variables: A dictionary mapping variable names (str) to their integer values.
        - instructions: A list of instructions (as strings) to be executed.
        - program_counter: An integer indicating the current instruction index.
        - labels: A dictionary mapping label names (str) to their corresponding instruction indices.
        - call_stack: A list used to manage return addresses for function calls.
        - halted: A boolean flag indicating whether the interpreter has halted execution.
        """
        self.stack: List[int] = []
        self.variables: Dict[str, int] = {}
        self.instructions: List[str] = []
        self.program_counter: int = 0
        self.labels: Dict[str, int] = {}
        self.call_stack: List[int] = []
        self.halted: bool = False

    def load_program(self, bytecode: str) -> None:
        """
        Loads a bytecode program into the interpreter by parsing the given bytecode string.
        Args:
            bytecode (str): The bytecode program as a string, with each instruction or label on a separate line.
        Side Effects:
            - Populates self.instructions with the parsed instructions, preserving line positions.
            - Populates self.labels with label names mapped to their corresponding line indices.
        Notes:
            - Lines that are empty or start with '#' (comments) are ignored in execution but preserved as empty strings in instructions.
            - Labels (lines ending with ':') are recorded in self.labels and also stored as empty strings in instructions to maintain line alignment.
        """
        lines = bytecode.strip().split("\n")
        self.instructions = []
        self.labels = {}

        for i, line in enumerate(lines):
            line = line.strip()

            if not line or line.startswith("#"):
                self.instructions.append("")
                continue

            if line.endswith(":"):
                label_name = line[:-1].strip()
                self.labels[label_name] = i
                self.instructions.append("")
            else:
                self.instructions.append(line)

    def parse_instruction(self, instruction: str) -> Tuple[Optional[str], List[str]]:
        """
        Parses a single instruction string into its opcode and arguments.
        Args:
            instruction (str): The instruction string to parse.
        Returns:
            tuple: A tuple containing the opcode (str or None) and a list of argument strings.
                   If the instruction is empty, returns (None, []).
        """
        if not instruction:
            return None, []

        parts = instruction.split()
        opcode = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        return opcode, args

    def execute_instruction(self, opcode: str, args: List[str]) -> None:
        """
        Executes a single bytecode instruction based on the provided opcode and arguments.

        This method uses a dispatch table to map opcodes to their corresponding handler methods.
        If the opcode is recognized, the associated handler is called with the given arguments.
        If the opcode is not recognized, a RuntimeError is raised.

        After executing the instruction, the program counter is incremented unless the instruction
        is a control flow operation (JMP, JZ, JNZ, CALL, RET), in which case the handler is responsible
        for updating the program counter as needed.

        Args:
            opcode (str): The operation code representing the instruction to execute.
            args (List[str]): A list of arguments for the instruction.

        Raises:
            RuntimeError: If the opcode is not recognized.
        """
        dispatch = {
            "PUSH": self.op_push,
            "POP": self.op_pop,
            "DUP": self.op_dup,
            "ADD": self.op_add,
            "SUB": self.op_sub,
            "MUL": self.op_mul,
            "DIV": self.op_div,
            "MOD": self.op_mod,
            "NEG": self.op_neg,
            "STORE": self.op_store,
            "LOAD": self.op_load,
            "JMP": self.op_jmp,
            "JZ": self.op_jz,
            "JNZ": self.op_jnz,
            "HALT": self.op_halt,
            "EQ": self.op_eq,
            "NEQ": self.op_neq,
            "LT": self.op_lt,
            "GT": self.op_gt,
            "LE": self.op_le,
            "GE": self.op_ge,
            "CALL": self.op_call,
            "RET": self.op_ret,
            "PRINT": self.op_print,
            "READ": self.op_read,
        }
        handler = dispatch.get(opcode)
        if handler:
            handler(args)
        else:
            raise RuntimeError(f"Unknown instruction: {opcode}")
        if opcode not in {"JMP", "JZ", "JNZ", "CALL", "RET"}:
            self.program_counter += 1

    def op_push(self, args: List[str]) -> None:
        """
        Pushes an integer value onto the stack.

        Args:
            args (list): A list where the first element is the value to be pushed onto the stack as a string.

        Side Effects:
            Appends the integer value to the instance's stack.
        """
        value = int(args[0])
        self.stack.append(value)

    def op_pop(self, args: List[str]) -> None:
        """
        Removes the top element from the stack if the stack is not empty.

        Args:
            args: Arguments for the operation (not used in this method).
        """
        if self.stack:
            self.stack.pop()

    def op_dup(self, args: List[str]) -> None:
        """
        Duplicates the top value on the stack.

        Args:
            args: Unused argument, present for interface consistency.

        Side Effects:
            If the stack is not empty, appends a copy of the top element to the stack.
        """
        if self.stack:
            self.stack.append(self.stack[-1])

    def op_add(self, args: List[str]) -> None:
        """
        Performs addition on the top two values of the stack.

        Pops the top two elements from the stack, adds them, and pushes the result back onto the stack.
        Assumes that the stack contains at least two elements.

        Args:
            args: Unused argument, present for interface compatibility.
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)

    def op_sub(self, args: List[str]) -> None:
        """
        Performs subtraction on the top two values of the stack.

        Pops the top two elements from the stack, subtracts the second popped value (b) from the first (a),
        and pushes the result back onto the stack.

        Args:
            args: Unused argument, included for opcode interface compatibility.

        Raises:
            IndexError: If there are fewer than two elements on the stack.
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)

    def op_mul(self, args: List[str]) -> None:
        """
        Performs multiplication on the top two values of the stack.

        Pops the top two elements from the stack, multiplies them, and pushes the result back onto the stack.
        If there are fewer than two elements on the stack, the operation is not performed.

        Args:
            args: Unused argument, included for interface consistency.

        Raises:
            IndexError: If there are fewer than two elements on the stack.
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)

    def op_div(self, args: List[str]) -> None:
        """
        Performs integer division on the top two values of the stack.

        Pops the top two elements from the stack, divides the second-to-top element
        by the top element using integer division, and pushes the result back onto the stack.
        Raises a RuntimeError if division by zero is attempted.

        Args:
            args: Unused argument, present for opcode interface compatibility.

        Raises:
            RuntimeError: If there are fewer than two elements on the stack or if division by zero is attempted.
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            if b != 0:
                self.stack.append(a // b)
            else:
                raise RuntimeError("Division by zero")

    def op_mod(self, args: List[str]) -> None:
        """
        Performs the modulo operation on the top two values of the stack.

        Pops the top two elements from the stack, computes the result of the first popped value modulo the second,
        and pushes the result back onto the stack. Raises a RuntimeError if the divisor is zero.

        Args:
            args: Unused argument, present for interface compatibility.

        Raises:
            RuntimeError: If there are fewer than two elements on the stack or if modulo by zero is attempted.
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            if b != 0:
                self.stack.append(a % b)
            else:
                raise RuntimeError("Modulo by zero")

    def op_neg(self, args: List[str]) -> None:
        """
        Negates the top value on the stack.

        Pops the top value from the stack, negates it, and pushes the result back onto the stack.
        If the stack is empty, the operation does nothing.

        Args:
            args: Unused argument, included for opcode interface consistency.
        """
        if self.stack:
            a = self.stack.pop()
            self.stack.append(-a)

    def op_store(self, args: List[str]) -> None:
        """
        Stores the top value from the stack into a variable.

        Args:
            args (list): A list where the first element is the variable name (str) to store the value in.

        Side Effects:
            Pops the top value from the stack and assigns it to the specified variable in self.variables.

        Notes:
            - If the stack is empty or args is empty, the method does nothing.
        """
        if self.stack and args:
            var_name = args[0]
            value = self.stack.pop()
            self.variables[var_name] = value

    def op_load(self, args: List[str]) -> None:
        """
        Loads the value of a variable onto the stack.

        Args:
            args (list): A list where the first element is the name of the variable to load.

        Raises:
            RuntimeError: If the specified variable name does not exist in the current variables dictionary.

        Side Effects:
            Appends the value of the specified variable to the stack.
        """
        if args:
            var_name = args[0]
            if var_name in self.variables:
                self.stack.append(self.variables[var_name])
            else:
                raise RuntimeError(f"Undefined variable: {var_name}")

    def op_jmp(self, args: List[str]) -> None:
        """
        Handles the 'jmp' (jump) operation in the bytecode interpreter.

        Args:
            args (list): A list where the first element is the jump target. The target can be a label name or an integer index.

        Behavior:
            - If the target is a label present in self.labels, sets the program counter to the corresponding instruction index.
            - If the target is not a label, attempts to convert it to an integer and sets the program counter to that value.
            - Raises a RuntimeError if the target is neither a valid label nor an integer.

        Raises:
            RuntimeError: If the jump target is invalid (not a known label or integer).
        """
        target = args[0]
        if target in self.labels:
            self.program_counter = self.labels[target]
        else:
            try:
                self.program_counter = int(target)
            except ValueError:
                raise RuntimeError(f"Invalid jump target: {target}")

    def op_jz(self, args: List[str]) -> None:
        """
        Implements the 'jump if zero' (JZ) operation for the bytecode interpreter.

        Pops the top value from the stack and checks if it is zero.
        - If the value is zero, sets the program counter to the target label or address specified in `args[0]`.
          - If the target is a known label, jumps to the corresponding instruction.
          - If the target is an integer, jumps to that instruction index.
          - Raises a RuntimeError if the target is invalid.
        - If the value is not zero, increments the program counter to proceed to the next instruction.
        - If the stack is empty, simply increments the program counter.

        Args:
            args (list): A list containing the jump target as the first element.
        """
        if self.stack:
            condition = self.stack.pop()
            if condition == 0:
                target = args[0]
                if target in self.labels:
                    self.program_counter = self.labels[target]
                else:
                    try:
                        self.program_counter = int(target)
                    except ValueError:
                        raise RuntimeError(f"Invalid jump target: {target}")
            else:
                self.program_counter += 1
        else:
            self.program_counter += 1

    def op_jnz(self, args: List[str]) -> None:
        """
        Implements the 'jnz' (jump if not zero) operation for the bytecode interpreter.

        Pops the top value from the stack and checks if it is not zero. If the value is not zero,
        sets the program counter to the target label or instruction index specified in `args[0]`.
        If the target is not a valid label, attempts to interpret it as an integer index.
        If the value is zero or the stack is empty, increments the program counter to proceed to the next instruction.

        Args:
            args (list): A list containing the jump target, which can be a label or an instruction index.

        Raises:
            RuntimeError: If the jump target is neither a valid label nor an integer.
        """
        if self.stack:
            condition = self.stack.pop()
            if condition != 0:
                target = args[0]
                if target in self.labels:
                    self.program_counter = self.labels[target]
                else:
                    try:
                        self.program_counter = int(target)
                    except ValueError:
                        raise RuntimeError(f"Invalid jump target: {target}")
            else:
                self.program_counter += 1
        else:
            self.program_counter += 1

    def op_halt(self, args: List[str]) -> None:
        """
        Halts the execution of the bytecode interpreter.

        This operation sets the interpreter's halted flag to True, causing the interpreter
        to stop processing further instructions.

        Args:
            args: Arguments for the halt operation (typically unused).
        """
        self.halted = True

    def op_eq(self, args: List[str]) -> None:
        """
        Compares the top two values on the stack for equality.

        Pops the top two elements from the stack, compares them for equality,
        and pushes 1 onto the stack if they are equal, or 0 otherwise.

        Args:
            args: Unused argument, present for opcode interface compatibility.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a == b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a == b else 0)

    def op_neq(self, args: List[str]) -> None:
        """
        Implements the 'not equal' (NEQ) operation for the bytecode interpreter.

        Pops the top two values from the stack, compares them for inequality,
        and pushes 1 onto the stack if they are not equal, or 0 if they are equal.

        Args:
            args: Unused argument, present for interface compatibility.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a != b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a != b else 0)

    def op_lt(self, args: List[str]) -> None:
        """
        Implements the 'less than' (<) operation for the bytecode interpreter.

        Pops the top two values from the stack, compares them, and pushes 1 onto the stack if the first popped value is less than the second; otherwise, pushes 0.

        Args:
            args: Unused argument, included for interface consistency.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a < b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a < b else 0)

    def op_gt(self, args: List[str]) -> None:
        """
        Implements the 'greater than' (>) operation for the interpreter.

        Pops the top two values from the stack, compares them, and pushes 1 onto the stack if the first popped value is greater than the second; otherwise, pushes 0.

        Args:
            args: Unused argument, included for opcode interface consistency.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a > b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a > b else 0)

    def op_le(self, args: List[str]) -> None:
        """
        Implements the 'less than or equal to' (<=) operation for the interpreter.

        Pops the top two values from the stack, compares them, and pushes 1 onto the stack if the first value is less than or equal to the second value, otherwise pushes 0.

        Args:
            args: Unused argument, included for opcode interface consistency.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a <= b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a <= b else 0)

    def op_ge(self, args: List[str]) -> None:
        """
        Implements the 'greater than or equal to' (>=) operation for the interpreter.

        Pops the top two values from the stack, compares them, and pushes 1 onto the stack if the first value is greater than or equal to the second value, otherwise pushes 0.

        Args:
            args: Unused argument, present for opcode interface compatibility.

        Stack Behavior:
            Before: [..., a, b]
            After:  [..., (1 if a >= b else 0)]
        """
        if len(self.stack) >= 2:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a >= b else 0)

    def op_call(self, args: List[str]) -> None:
        """
        Handles the 'call' operation in the bytecode interpreter.

        This method saves the current program counter to the call stack and jumps to the target instruction.
        The target can be either a label defined in the program or a direct instruction index.
        If the target is not a valid label or integer, a RuntimeError is raised.

        Args:
            args (list): A list where the first element is the call target (label name or instruction index).

        Raises:
            RuntimeError: If the call target is neither a valid label nor an integer.
        """
        target = args[0]
        self.call_stack.append(self.program_counter + 1)
        if target in self.labels:
            self.program_counter = self.labels[target]
        else:
            try:
                self.program_counter = int(target)
            except ValueError:
                raise RuntimeError(f"Invalid call target: {target}")

    def op_ret(self, args: List[str]) -> None:
        """
        Handles the 'ret' (return) operation in the bytecode interpreter.

        If the call stack is not empty, restores the program counter to the last saved value,
        effectively returning from a function call. If the call stack is empty, sets the halted
        flag to True, indicating that the program should stop execution.

        Args:
            args: Arguments for the 'ret' operation (not used in this implementation).
        """
        if self.call_stack:
            self.program_counter = self.call_stack.pop()
        else:
            self.halted = True

    def op_print(self, args: List[str]) -> None:
        """
        Prints the top value of the stack without removing it.

        If the stack is not empty, prints the value at the top of the stack.
        If the stack is empty, prints 0.

        Args:
            args: Arguments for the print operation (not used).
        """
        if self.stack:
            value = self.stack[-1]
            print(value)
        else:
            print(0)

    def op_read(self, args: List[str]) -> None:
        """
        Reads an integer value from standard input and pushes it onto the stack.

        If the input is not a valid integer or if an EOFError occurs, pushes 0 onto the stack instead.

        Args:
            args: Unused argument, present for interface compatibility.
        """
        try:
            value = int(input())
            self.stack.append(value)
        except (ValueError, EOFError):
            self.stack.append(0)

    def run(self) -> None:
        """
        Executes the loaded bytecode instructions sequentially.
        Initializes the program counter and halted flag, then iterates through the instruction list.
        For each instruction, it parses and executes the opcode and its arguments.
        Handles runtime errors by printing an error message with the current line number and halts execution.
        Skips empty instructions by advancing the program counter.
        """
        self.program_counter = 0
        self.halted = False

        while not self.halted and self.program_counter < len(self.instructions):
            instruction = self.instructions[self.program_counter]

            if instruction:
                opcode, args = self.parse_instruction(instruction)
                if opcode:
                    try:
                        self.execute_instruction(opcode, args)
                    except Exception as e:
                        print(
                            f"Runtime error at line {self.program_counter + 1}: {e}",
                            file=sys.stderr,
                        )
                        break
            else:
                self.program_counter += 1

    def debug_state(self) -> None:
        """
        Prints the current state of the bytecode interpreter for debugging purposes.

        Displays the values of the program counter, stack, variables, and call stack
        to help trace the execution and diagnose issues.
        """
        print(f"PC: {self.program_counter}")
        print(f"Stack: {self.stack}")
        print(f"Variables: {self.variables}")
        print(f"Call Stack: {self.call_stack}")
        print("---")


def main():
    """
    Main entry point for the bytecode interpreter.
    If a filename is provided as a command-line argument, attempts to read bytecode from the specified file.
    If no filename is provided, reads bytecode from standard input.
    Handles file not found and general file reading errors gracefully, printing error messages to stderr and exiting with a non-zero status code.
    After loading the bytecode, initializes a BytecodeInterpreter instance, loads the program, and executes it.
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                bytecode = f.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        bytecode = sys.stdin.read()

    interpreter = BytecodeInterpreter()
    interpreter.load_program(bytecode)
    interpreter.run()


if __name__ == "__main__":
    main()
