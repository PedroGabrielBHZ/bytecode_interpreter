import sys
from typing import Tuple


class BytecodeOptimizer:
    def __init__(self):
        """
        Initializes a new instance of the class, setting up an empty list for instructions
        and an empty dictionary for labels.
        """
        self.instructions = []
        self.labels = {}

    def load_program(self, bytecode: str) -> None:
        """
        Loads a bytecode program into the interpreter by parsing the given bytecode string.
        Args:
            bytecode (str): The bytecode program as a string, with each instruction or label on a separate line.
        Side Effects:
            - Populates self.instructions with the parsed instructions, preserving line positions.
            - Populates self.labels with label names mapped to their corresponding line indices.
        Notes:
            - Lines that are empty or start with '#' (comments) are preserved as empty strings in instructions.
            - Labels (lines ending with ':') are recorded in self.labels and preserved in instructions.
        """
        lines = bytecode.strip().split("\n")
        self.instructions = []
        self.labels = {}

        for i, line in enumerate(lines):
            stripped = line.strip()

            if not stripped or stripped.startswith("#"):
                self.instructions.append(line)
                continue

            if stripped.endswith(":"):
                label_name = stripped[:-1].strip()
                self.labels[label_name] = i
                self.instructions.append(line)  # Preserve the actual label line
            else:
                self.instructions.append(stripped)

    def optimize_push_pop(self) -> int:
        """
        Optimizes the instruction list by removing consecutive "PUSH <value>" followed by "POP" instructions.
        Preserves all label lines and comments.

        Returns:
            int: The total number of instructions removed from the list (counting both "PUSH" and "POP" instructions).
        """
        optimized = []
        i = 0
        removed_count = 0
        while i < len(self.instructions):
            current = self.instructions[i]
            current_stripped = current.strip()
            # Always preserve labels, comments, and blank lines
            if (
                current_stripped == ""
                or current_stripped.startswith("#")
                or current_stripped.endswith(":")
            ):
                optimized.append(current)
                i += 1
                continue
            if i + 1 < len(self.instructions):
                next_instr = self.instructions[i + 1]
                next_stripped = next_instr.strip()
                if current_stripped.startswith("PUSH ") and next_stripped == "POP":
                    removed_count += 2
                    i += 2
                    continue
            optimized.append(current)
            i += 1
        self.instructions = optimized
        return removed_count

    def optimize_redundant_loads(self) -> int:
        """
        Optimizes redundant consecutive LOAD instructions in the instruction list.
        Preserves all label lines and comments.

        Returns:
            int: The number of redundant LOAD instructions removed.
        """
        optimized = []
        i = 0
        removed_count = 0
        while i < len(self.instructions):
            current = self.instructions[i]
            current_stripped = current.strip()
            # Always preserve labels, comments, and blank lines
            if (
                current_stripped == ""
                or current_stripped.startswith("#")
                or current_stripped.endswith(":")
            ):
                optimized.append(current)
                i += 1
                continue
            if current_stripped.startswith("LOAD "):
                var_name = current_stripped.split()[1]
                j = i + 1
                consecutive_loads = 0
                # Skip over comments, blank lines, and labels
                while j < len(self.instructions):
                    next_instr = self.instructions[j]
                    next_stripped = next_instr.strip()
                    if (
                        next_stripped == ""
                        or next_stripped.startswith("#")
                        or next_stripped.endswith(":")
                    ):
                        j += 1
                        continue
                    elif next_stripped == f"LOAD {var_name}":
                        consecutive_loads += 1
                        j += 1
                    else:
                        break
                optimized.append(current)
                if consecutive_loads > 0:
                    for _ in range(consecutive_loads):
                        optimized.append("DUP")
                    i = j
                    removed_count += consecutive_loads
                else:
                    i += 1
            else:
                optimized.append(current)
                i += 1
        self.instructions = optimized
        return removed_count

    def optimize_dead_code(self) -> int:
        """
        Removes dead code from the instruction list by eliminating instructions that appear after
        unconditional control flow changes (such as 'HALT', 'RET', or 'JMP') until the next label.

        Returns:
            int: The number of instructions removed as dead code.
        """
        optimized = []
        removed_count = 0
        skip_until_label = False
        for instruction in self.instructions:
            instr = instruction.strip()
            if skip_until_label:
                if instr.endswith(":"):
                    skip_until_label = False
                    optimized.append(instruction)
                else:
                    if instr and not instr.startswith("#"):
                        removed_count += 1
                continue
            optimized.append(instruction)
            if instr in ["HALT", "RET"] or instr.startswith("JMP "):
                skip_until_label = True
        self.instructions = optimized
        return removed_count

    def optimize_constant_folding(self) -> int:
        """
        Optimizes the instruction list by performing constant folding on consecutive PUSH and arithmetic operations.

        This method scans through the list of instructions and looks for patterns where two consecutive
        PUSH instructions are immediately followed by an arithmetic operation (ADD, SUB, MUL, DIV, MOD).
        If both PUSH instructions contain integer constants, the arithmetic operation is computed at
        compile-time, and the three instructions are replaced with a single PUSH instruction containing
        the result. The method skips folding for division or modulo by zero.

        Returns:
            int: The number of instructions removed from the instruction list as a result of constant folding.
        """
        optimized = []
        i = 0
        removed_count = 0
        while i < len(self.instructions):
            current = self.instructions[i].strip()
            if current.startswith("PUSH ") and i + 2 < len(self.instructions):
                next1 = self.instructions[i + 1].strip()
                next2 = self.instructions[i + 2].strip()
                if next1.startswith("PUSH ") and next2 in [
                    "ADD",
                    "SUB",
                    "MUL",
                    "DIV",
                    "MOD",
                ]:
                    try:
                        val1 = int(current.split()[1])
                        val2 = int(next1.split()[1])
                        if next2 == "ADD":
                            result = val1 + val2
                        elif next2 == "SUB":
                            result = val1 - val2
                        elif next2 == "MUL":
                            result = val1 * val2
                        elif next2 == "DIV" and val2 != 0:
                            result = val1 // val2
                        elif next2 == "MOD" and val2 != 0:
                            result = val1 % val2
                        else:
                            optimized.append(self.instructions[i])
                            i += 1
                            continue
                        optimized.append(f"PUSH {result}")
                        removed_count += 2
                        i += 3
                        continue
                    except (ValueError, IndexError):
                        pass
            optimized.append(self.instructions[i])
            i += 1
        self.instructions = optimized
        return removed_count

    def optimize(self) -> Tuple[str, dict]:
        """
        Optimizes the current list of bytecode instructions by applying optimization passes.

        The method performs the following optimizations in sequence:
            - Removes redundant push/pop instruction pairs.
            - Eliminates redundant load instructions.
            - Removes dead code that does not affect program output.
            - Performs constant folding to simplify constant expressions.

        Returns:
            Tuple[str, dict]: A tuple containing:
                - The optimized bytecode as a single string.
                - A dictionary with statistics about the number of instructions removed by each optimization pass and the total removed.
        """
        stats = {
            "push_pop_removed": 0,
            "redundant_loads_removed": 0,
            "dead_code_removed": 0,
            "constant_folding_removed": 0,
            "total_removed": 0,
        }
        original_size = len(
            [
                i
                for i in self.instructions
                if i.strip() and not i.strip().startswith("#")
            ]
        )
        stats["push_pop_removed"] = self.optimize_push_pop()
        stats["redundant_loads_removed"] = self.optimize_redundant_loads()
        stats["dead_code_removed"] = self.optimize_dead_code()
        stats["constant_folding_removed"] = self.optimize_constant_folding()
        final_size = len(
            [
                i
                for i in self.instructions
                if i.strip() and not i.strip().startswith("#")
            ]
        )
        stats["total_removed"] = original_size - final_size
        optimized_code = "\n".join(self.instructions)
        return optimized_code, stats


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python bytecode_optimizer.py <input_file> [output_file]",
            file=sys.stderr,
        )
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            bytecode = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    optimizer = BytecodeOptimizer()
    optimizer.load_program(bytecode)
    optimized_code, stats = optimizer.optimize()
    if output_file:
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(optimized_code)
            print(f"Optimized code saved to '{output_file}'")
        except Exception as e:
            print(f"Error writing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(optimized_code)
    if stats["total_removed"] > 0:
        print(f"\nOptimization Statistics:", file=sys.stderr)
        print(f"- PUSH/POP pairs removed: {stats['push_pop_removed']}", file=sys.stderr)
        print(
            f"- Redundant LOADs removed: {stats['redundant_loads_removed']}",
            file=sys.stderr,
        )
        print(
            f"- Dead code instructions removed: {stats['dead_code_removed']}",
            file=sys.stderr,
        )
        print(
            f"- Constant folding optimizations: {stats['constant_folding_removed']}",
            file=sys.stderr,
        )
        print(
            f"- Total instructions removed: {stats['total_removed']}", file=sys.stderr
        )
    else:
        print("No optimizations applied.", file=sys.stderr)


if __name__ == "__main__":
    main()
