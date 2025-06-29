#!/usr/bin/env python3
"""
Interpretador Bytecode - Trabalho Prático Compiladores
Universidade: Pontifícia Universidade Católica de Minas Gerais
Disciplina: Compiladores
Professor: Pedro Ramos
"""

import sys
from typing import List, Dict, Any, Optional
import re


class BytecodeInterpreter:
    """Interpretador para linguagem bytecode baseada em pilha"""

    def __init__(self):
        self.stack: List[int] = []  # Pilha principal
        self.variables: Dict[str, int] = {}  # Memória das variáveis
        self.instructions: List[str] = []  # Lista de instruções
        self.program_counter: int = 0  # Contador de programa (PC)
        self.labels: Dict[str, int] = {}  # Mapeamento de labels para endereços
        self.call_stack: List[int] = []  # Pilha de chamadas para funções
        self.halted: bool = False

    def load_program(self, bytecode: str) -> None:
        """Carrega o programa bytecode e processa labels"""
        lines = bytecode.strip().split("\n")
        self.instructions = []
        self.labels = {}

        for i, line in enumerate(lines):
            line = line.strip()

            # Ignora linhas vazias e comentários
            if not line or line.startswith("#"):
                self.instructions.append("")
                continue

            # Processa labels
            if line.endswith(":"):
                label_name = line[:-1].strip()
                self.labels[label_name] = i
                self.instructions.append("")  # Label não é uma instrução executável
            else:
                self.instructions.append(line)

    def parse_instruction(self, instruction: str) -> tuple:
        """Parse uma instrução em opcode e argumentos"""
        if not instruction:
            return None, []

        parts = instruction.split()
        opcode = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        return opcode, args

    def execute_instruction(self, opcode: str, args: List[str]) -> None:
        """Executa uma instrução específica"""

        # Operações aritméticas e de pilha
        if opcode == "PUSH":
            value = int(args[0])
            self.stack.append(value)

        elif opcode == "POP":
            if self.stack:
                self.stack.pop()

        elif opcode == "DUP":
            if self.stack:
                self.stack.append(self.stack[-1])

        elif opcode == "ADD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)

        elif opcode == "SUB":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)

        elif opcode == "MUL":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)

        elif opcode == "DIV":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a // b)  # Divisão inteira
                else:
                    raise RuntimeError("Division by zero")

        elif opcode == "MOD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a % b)
                else:
                    raise RuntimeError("Modulo by zero")

        elif opcode == "NEG":
            if self.stack:
                a = self.stack.pop()
                self.stack.append(-a)

        # Variáveis
        elif opcode == "STORE":
            if self.stack and args:
                var_name = args[0]
                value = self.stack.pop()
                self.variables[var_name] = value

        elif opcode == "LOAD":
            if args:
                var_name = args[0]
                if var_name in self.variables:
                    self.stack.append(self.variables[var_name])
                else:
                    raise RuntimeError(f"Undefined variable: {var_name}")

        # Fluxo de controle
        elif opcode == "JMP":
            target = args[0]
            if target in self.labels:
                self.program_counter = self.labels[target]
                return  # Não incrementa PC
            else:
                try:
                    self.program_counter = int(target)
                    return
                except ValueError:
                    raise RuntimeError(f"Invalid jump target: {target}")

        elif opcode == "JZ":
            if self.stack:
                condition = self.stack.pop()
                if condition == 0:
                    target = args[0]
                    if target in self.labels:
                        self.program_counter = self.labels[target]
                        return
                    else:
                        try:
                            self.program_counter = int(target)
                            return
                        except ValueError:
                            raise RuntimeError(f"Invalid jump target: {target}")

        elif opcode == "JNZ":
            if self.stack:
                condition = self.stack.pop()
                if condition != 0:
                    target = args[0]
                    if target in self.labels:
                        self.program_counter = self.labels[target]
                        return
                    else:
                        try:
                            self.program_counter = int(target)
                            return
                        except ValueError:
                            raise RuntimeError(f"Invalid jump target: {target}")

        elif opcode == "HALT":
            self.halted = True

        # Comparação
        elif opcode == "EQ":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a == b else 0)

        elif opcode == "NEQ":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a != b else 0)

        elif opcode == "LT":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a < b else 0)

        elif opcode == "GT":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a > b else 0)

        elif opcode == "LE":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a <= b else 0)

        elif opcode == "GE":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(1 if a >= b else 0)

        # Funções e E/S
        elif opcode == "CALL":
            target = args[0]
            # Empilha endereço de retorno
            self.call_stack.append(self.program_counter + 1)
            if target in self.labels:
                self.program_counter = self.labels[target]
                return
            else:
                try:
                    self.program_counter = int(target)
                    return
                except ValueError:
                    raise RuntimeError(f"Invalid call target: {target}")

        elif opcode == "RET":
            if self.call_stack:
                self.program_counter = self.call_stack.pop()
                return
            else:
                self.halted = True  # Se não há mais calls, termina programa

        elif opcode == "PRINT":
            if self.stack:
                value = self.stack[-1]  # PRINT não remove da pilha
                print(value)
            else:
                print(0)  # Se pilha vazia, imprime 0

        elif opcode == "READ":
            try:
                value = int(input())
                self.stack.append(value)
            except (ValueError, EOFError):
                self.stack.append(0)  # Se erro na leitura, empilha 0

        else:
            raise RuntimeError(f"Unknown instruction: {opcode}")

        # Incrementa program counter
        self.program_counter += 1

    def run(self) -> None:
        """Executa o programa bytecode"""
        self.program_counter = 0
        self.halted = False

        while not self.halted and self.program_counter < len(self.instructions):
            instruction = self.instructions[self.program_counter]

            if instruction:  # Ignora instruções vazias
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
        """Imprime estado atual para debug"""
        print(f"PC: {self.program_counter}")
        print(f"Stack: {self.stack}")
        print(f"Variables: {self.variables}")
        print(f"Call Stack: {self.call_stack}")
        print("---")


def main():
    """Função principal do interpretador"""
    if len(sys.argv) > 1:
        # Lê de arquivo
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
        # Lê da entrada padrão
        bytecode = sys.stdin.read()

    # Cria e executa interpretador
    interpreter = BytecodeInterpreter()
    interpreter.load_program(bytecode)
    interpreter.run()


if __name__ == "__main__":
    main()
