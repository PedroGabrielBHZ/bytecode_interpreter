import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os


class BytecodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bytecode GUI")
        self.filename = None
        self.optimized_filename = None
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Carregar .bc", command=self.load_bc).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(
            btn_frame, text="Executar Otimizador", command=self.run_optimizer
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Comparar", command=self.compare_codes).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Salvar Otimizado", command=self.save_optimized).pack(
            side=tk.LEFT, padx=2
        )

        # Segunda linha de botões para execução
        btn_frame2 = tk.Frame(frame)
        btn_frame2.pack(fill=tk.X, pady=(5, 0))

        tk.Button(
            btn_frame2,
            text="Executar Original",
            command=self.run_original,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            btn_frame2,
            text="Executar Otimizado",
            command=self.run_optimized,
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame2, text="Limpar Saídas", command=self.clear_outputs).pack(
            side=tk.LEFT, padx=2
        )

        self.status = tk.Label(frame, text="Bem-vindo!", anchor="w")
        self.status.pack(fill=tk.X, pady=(5, 0))

        text_frame = tk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Original code
        left_label = tk.Label(text_frame, text="Código Original")
        left_label.grid(row=0, column=0, sticky="w")
        self.text_original = scrolledtext.ScrolledText(text_frame, width=30, height=15)
        self.text_original.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")

        # Optimized code
        right_label = tk.Label(text_frame, text="Código Otimizado")
        right_label.grid(row=0, column=1, sticky="w")
        self.text_optimized = scrolledtext.ScrolledText(
            text_frame, width=30, height=15, state=tk.DISABLED
        )
        self.text_optimized.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        # Output area
        output_frame = tk.Frame(text_frame)
        output_frame.grid(row=0, column=2, rowspan=2, padx=5, pady=2, sticky="nsew")

        output_label = tk.Label(output_frame, text="Saída dos Programas")
        output_label.pack(anchor="w")

        # Input field for program input
        input_frame = tk.Frame(output_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(input_frame, text="Entrada:").pack(side=tk.LEFT)
        self.input_entry = tk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        self.text_output = scrolledtext.ScrolledText(
            output_frame, width=25, height=15, state=tk.DISABLED
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)

        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)
        text_frame.columnconfigure(2, weight=1)
        text_frame.rowconfigure(1, weight=1)

    def load_bc(self):
        filename = filedialog.askopenfilename(filetypes=[("Bytecode Files", "*.bc")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
            self.text_original.delete(1.0, tk.END)
            self.text_original.insert(tk.END, code)
            self.filename = filename
            self.status.config(text=f"Arquivo carregado: {os.path.basename(filename)}")
            self.text_optimized.config(state=tk.NORMAL)
            self.text_optimized.delete(1.0, tk.END)
            self.text_optimized.config(state=tk.DISABLED)
            self.optimized_filename = None
            # Limpa também a área de saída
            self.clear_outputs()

    def run_optimizer(self):
        if not self.filename:
            messagebox.showwarning("Aviso", "Carregue um arquivo .bc primeiro!")
            return
        # Salva o código original editado em um arquivo temporário
        temp_input = "temp_input.bc"
        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(self.text_original.get(1.0, tk.END))
        output_file = "temp_optimized.bc"
        try:
            result = subprocess.run(
                ["python", "bytecode_optimizer.py", temp_input, output_file],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.status.config(text="Erro ao otimizar: " + result.stderr)
                return
            with open(output_file, "r", encoding="utf-8") as f:
                optimized_code = f.read()
            self.text_optimized.config(state=tk.NORMAL)
            self.text_optimized.delete(1.0, tk.END)
            self.text_optimized.insert(tk.END, optimized_code)
            self.text_optimized.config(state=tk.DISABLED)
            self.optimized_filename = output_file
            self.status.config(text="Otimização concluída!")
        except Exception as e:
            self.status.config(text=f"Erro: {e}")

    def compare_codes(self):
        if not self.filename or not self.optimized_filename:
            messagebox.showinfo("Info", "Carregue e otimize um arquivo primeiro!")
            return
        # Abre uma janela para comparação lado a lado
        win = tk.Toplevel(self.root)
        win.title("Comparação de Códigos")
        win.geometry("900x500")
        orig = scrolledtext.ScrolledText(win, width=45, height=25)
        orig.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        opt = scrolledtext.ScrolledText(win, width=45, height=25)
        opt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        with open(self.filename, "r", encoding="utf-8") as f:
            orig.insert(tk.END, f.read())
        with open(self.optimized_filename, "r", encoding="utf-8") as f:
            opt.insert(tk.END, f.read())
        orig.config(state=tk.DISABLED)
        opt.config(state=tk.DISABLED)

    def save_optimized(self):
        if not self.optimized_filename:
            messagebox.showinfo("Info", "Nenhum código otimizado para salvar!")
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".bc", filetypes=[("Bytecode Files", "*.bc")]
        )
        if save_path:
            with open(self.optimized_filename, "r", encoding="utf-8") as src, open(
                save_path, "w", encoding="utf-8"
            ) as dst:
                dst.write(src.read())
            self.status.config(text=f"Arquivo otimizado salvo em: {save_path}")

    def run_original(self):
        if not self.filename:
            messagebox.showwarning("Aviso", "Carregue um arquivo .bc primeiro!")
            return

        # Salva o código original editado em um arquivo temporário
        temp_input = "temp_original.bc"
        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(self.text_original.get(1.0, tk.END))

        self.execute_program(temp_input, "Original")

    def run_optimized(self):
        if not self.optimized_filename:
            messagebox.showwarning("Aviso", "Execute o otimizador primeiro!")
            return

        self.execute_program(self.optimized_filename, "Otimizado")

    def execute_program(self, filename, program_type):
        user_input = self.input_entry.get()

        try:
            # Executa o interpretador
            if user_input:
                # Se há entrada do usuário, fornece via stdin
                result = subprocess.run(
                    ["python", "bytecode_interpreter.py", filename],
                    input=user_input,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            else:
                # Execução sem entrada
                result = subprocess.run(
                    ["python", "bytecode_interpreter.py", filename],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

            # Atualiza a área de saída
            self.text_output.config(state=tk.NORMAL)
            self.text_output.insert(tk.END, f"\n--- Execução {program_type} ---\n")

            if result.stdout:
                self.text_output.insert(tk.END, f"Saída: {result.stdout}\n")
            if result.stderr:
                self.text_output.insert(tk.END, f"Erro: {result.stderr}\n")
            if result.returncode != 0:
                self.text_output.insert(
                    tk.END, f"Código de retorno: {result.returncode}\n"
                )

            self.text_output.insert(tk.END, "--- Fim ---\n")
            self.text_output.see(tk.END)
            self.text_output.config(state=tk.DISABLED)

            self.status.config(text=f"Programa {program_type.lower()} executado!")

        except subprocess.TimeoutExpired:
            self.status.config(
                text=f"Timeout na execução do programa {program_type.lower()}"
            )
        except Exception as e:
            self.status.config(
                text=f"Erro ao executar programa {program_type.lower()}: {e}"
            )

    def clear_outputs(self):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.config(state=tk.DISABLED)
        self.status.config(text="Saídas limpas!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BytecodeGUI(root)
    root.mainloop()
