import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys

if sys.platform == "win32":
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


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

        tk.Button(btn_frame, text="Load .bc", command=self.load_bc).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Run Optimizer", command=self.run_optimizer).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(btn_frame, text="Save Optimized", command=self.save_optimized).pack(
            side=tk.LEFT, padx=2
        )
        tk.Button(
            btn_frame,
            text="Run Original",
            command=self.run_original,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            btn_frame,
            text="Run Optimized",
            command=self.run_optimized,
            bg="#2196F3",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Clear Output", command=self.clear_outputs).pack(
            side=tk.LEFT, padx=2
        )

        # Input field for program input
        tk.Label(btn_frame, text="Input:").pack(side=tk.LEFT, padx=(20, 2))
        self.input_entry = tk.Entry(btn_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))

        text_frame = tk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Original code
        left_label = tk.Label(text_frame, text="Original Code")
        left_label.grid(row=0, column=0, sticky="w")
        self.text_original = scrolledtext.ScrolledText(text_frame, width=30, height=15)
        self.text_original.grid(row=1, column=0, padx=5, pady=2, sticky="nsew")

        # Optimized code
        right_label = tk.Label(text_frame, text="Optimized Code")
        right_label.grid(row=0, column=1, sticky="w")
        self.text_optimized = scrolledtext.ScrolledText(
            text_frame, width=30, height=15, state=tk.DISABLED
        )
        self.text_optimized.grid(row=1, column=1, padx=5, pady=2, sticky="nsew")

        # Output area
        output_frame = tk.Frame(text_frame)
        output_frame.grid(row=0, column=2, rowspan=2, padx=5, pady=2, sticky="nsew")

        output_label = tk.Label(output_frame, text="Program Output")
        output_label.pack(anchor="w")

        self.text_output = scrolledtext.ScrolledText(
            output_frame, width=25, height=15, state=tk.DISABLED
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)

        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)
        text_frame.columnconfigure(2, weight=1)
        text_frame.rowconfigure(1, weight=1)

        self.status = tk.Label(
            frame, text="Welcome!", anchor="center", justify="center"
        )
        self.status.pack(fill=tk.X, pady=(10, 0), side=tk.BOTTOM)
        self.status.configure(font=(None, 11))

    def load_bc(self):
        filename = filedialog.askopenfilename(filetypes=[("Bytecode Files", "*.bc")])
        if filename:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
            self.text_original.delete(1.0, tk.END)
            self.text_original.insert(tk.END, code)
            self.filename = filename
            self.status.config(text=f"File loaded: {os.path.basename(filename)}")
            self.text_optimized.config(state=tk.NORMAL)
            self.text_optimized.delete(1.0, tk.END)
            self.text_optimized.config(state=tk.DISABLED)
            self.optimized_filename = None
            self.clear_outputs()

    def run_optimizer(self):
        if not self.filename:
            messagebox.showwarning("Warning", "Load a .bc file first!")
            return
        temp_input = os.path.join("outputs", "temp_input.bc")
        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(self.text_original.get(1.0, tk.END))
        output_file = os.path.join("outputs", "temp_optimized.bc")
        try:
            result = subprocess.run(
                ["python", "bytecode_optimizer.py", temp_input, output_file],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                self.status.config(text="Error optimizing: " + result.stderr)
                return
            with open(output_file, "r", encoding="utf-8") as f:
                optimized_code = f.read()
            self.text_optimized.config(state=tk.NORMAL)
            self.text_optimized.delete(1.0, tk.END)
            self.text_optimized.insert(tk.END, optimized_code)
            self.text_optimized.config(state=tk.DISABLED)
            self.optimized_filename = output_file
            self.status.config(text="Optimization complete!")
        except Exception as e:
            self.status.config(text=f"Error: {e}")

    def save_optimized(self):
        if not self.optimized_filename:
            messagebox.showinfo("Info", "No optimized code to save!")
            return
        save_path = filedialog.asksaveasfilename(
            initialdir=os.path.abspath("outputs"),
            defaultextension=".bc",
            filetypes=[("Bytecode Files", "*.bc")],
        )
        if save_path:
            with open(self.optimized_filename, "r", encoding="utf-8") as src, open(
                save_path, "w", encoding="utf-8"
            ) as dst:
                dst.write(src.read())
            self.status.config(text=f"Optimized file saved to: {save_path}")

    def run_original(self):
        if not self.filename:
            messagebox.showwarning("Warning", "Load a .bc file first!")
            return
        temp_input = os.path.join("outputs", "temp_original.bc")
        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(self.text_original.get(1.0, tk.END))
        self.execute_program(temp_input, "Original")

    def run_optimized(self):
        if not self.optimized_filename:
            messagebox.showwarning("Warning", "Run the optimizer first!")
            return
        self.execute_program(self.optimized_filename, "Optimized")

    def execute_program(self, filename, program_type):
        user_input = self.input_entry.get()

        try:
            if user_input:
                result = subprocess.run(
                    ["python", "bytecode_interpreter.py", filename],
                    input=user_input,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            else:
                result = subprocess.run(
                    ["python", "bytecode_interpreter.py", filename],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

            self.text_output.config(state=tk.NORMAL)
            self.text_output.insert(tk.END, f"\n--- {program_type} Execution ---\n")

            if result.stdout:
                self.text_output.insert(tk.END, f"Output: {result.stdout}\n")
            if result.stderr:
                self.text_output.insert(tk.END, f"Error: {result.stderr}\n")
            if result.returncode != 0:
                self.text_output.insert(tk.END, f"Return code: {result.returncode}\n")

            self.text_output.insert(tk.END, "--- End ---\n")
            self.text_output.see(tk.END)
            self.text_output.config(state=tk.DISABLED)

            self.status.config(text=f"{program_type} program executed!")

        except subprocess.TimeoutExpired:
            self.status.config(
                text=f"Timeout while executing {program_type.lower()} program"
            )
        except Exception as e:
            self.status.config(
                text=f"Error while executing {program_type.lower()} program: {e}"
            )

    def clear_outputs(self):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.config(state=tk.DISABLED)
        self.status.config(text="Outputs cleared!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BytecodeGUI(root)
    root.mainloop()
