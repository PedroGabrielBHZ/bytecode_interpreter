import sys
from typing import Tuple


class BytecodeOptimizer:
    def __init__(self):
        self.instructions = []
        self.labels = {}

    def load_program(self, bytecode: str) -> None:
        lines = bytecode.strip().split("\n")
        self.instructions = []
        self.labels = {}
        for i, line in enumerate(lines):
            line = line.strip()
            if line.endswith(":"):
                label_name = line[:-1].strip()
                self.labels[label_name] = i
            self.instructions.append(line)

    def optimize_push_pop(self) -> int:
        optimized = []
        i = 0
        removed_count = 0
        while i < len(self.instructions):
            current = self.instructions[i].strip()
            if i + 1 < len(self.instructions):
                next_instr = self.instructions[i + 1].strip()
                if current.startswith("PUSH ") and next_instr == "POP":
                    removed_count += 2
                    i += 2
                    continue
            optimized.append(self.instructions[i])
            i += 1
        self.instructions = optimized
        return removed_count

    def optimize_redundant_loads(self) -> int:
        optimized = []
        i = 0
        removed_count = 0
        while i < len(self.instructions):
            current = self.instructions[i].strip()
            if current.startswith("LOAD "):
                var_name = current.split()[1]
                j = i + 1
                consecutive_loads = 0
                while j < len(self.instructions):
                    next_instr = self.instructions[j].strip()
                    if (
                        next_instr == ""
                        or next_instr.startswith("#")
                        or next_instr.endswith(":")
                    ):
                        j += 1
                        continue
                    elif next_instr == f"LOAD {var_name}":
                        consecutive_loads += 1
                        j += 1
                    else:
                        break
                optimized.append(self.instructions[i])
                if consecutive_loads > 0:
                    for _ in range(consecutive_loads):
                        optimized.append("DUP")
                    i = j
                    removed_count += consecutive_loads
                else:
                    i += 1
            else:
                optimized.append(self.instructions[i])
                i += 1
        self.instructions = optimized
        return removed_count

    def optimize_dead_code(self) -> int:
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
