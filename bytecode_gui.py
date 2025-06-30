import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys

# dpi workaround
if sys.platform == "win32":
    try:
        import ctypes

        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


class BytecodeGUI:
    def __init__(self, root):
        """
        Initializes the Bytecode GUI application.

        Args:
            root (tk.Tk): The root window of the Tkinter application.

        Attributes:
            root (tk.Tk): The main application window.
            filename (str or None): The path to the currently loaded file, if any.
            optimized_filename (str or None): The path to the optimized file, if any.

        Side Effects:
            Sets the window title and initializes the GUI widgets.
        """
        self.root = root
        self.root.title("Bytecode GUI")
        self.filename = None
        self.optimized_filename = None
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and arranges all GUI widgets for the bytecode GUI application.
        This method sets up the main interface, including:
        - A frame containing buttons for loading, optimizing, saving, running, and clearing bytecode files.
        - An input field for user program input.
        - Three main text areas: one for displaying the original code, one for the optimized code, and one for program output.
        - A status bar at the bottom for displaying messages to the user.
        All widgets are packed and configured with appropriate layout and styling options.
        """
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
            bg="#777100",
            fg="white",
        ).pack(side=tk.LEFT, padx=2)
        tk.Button(
            btn_frame,
            text="Run Optimized",
            command=self.run_optimized,
            bg="#F32121",
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
        """
        Opens a file dialog for the user to select a bytecode (.bc) file, loads its contents into the original text widget,
        updates the status bar with the loaded filename, clears the optimized text widget and output areas, and resets
        related state variables.

        Side Effects:
            - Updates self.text_original with the loaded file's content.
            - Updates self.status with the loaded filename.
            - Clears and disables self.text_optimized.
            - Resets self.optimized_filename to None.
            - Calls self.clear_outputs() to clear output widgets.
        """
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
        """
        Runs the bytecode optimizer on the currently loaded .bc file.

        This method performs the following steps:
        1. Checks if a file is loaded; if not, shows a warning message.
        2. Writes the contents of the original code text widget to a temporary input file.
        3. Invokes the bytecode optimizer script (`bytecode_optimizer.py`) as a subprocess,
           passing the temporary input and output file paths.
        4. If optimization is successful, reads the optimized code from the output file and
           displays it in the optimized code text widget (set to read-only).
        5. Updates the status label with the result of the operation.
        6. Handles and displays any errors that occur during the process.

        Side Effects:
            - Updates GUI widgets (status label, optimized code text widget).
            - Writes temporary files to the "outputs" directory.
            - Sets `self.optimized_filename` to the path of the optimized output file.
        """
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
        """
        Saves the optimized bytecode to a user-specified file.

        If there is no optimized file available, displays an informational message.
        Otherwise, opens a file dialog for the user to select the save location and filename.
        Copies the contents of the optimized bytecode file to the chosen destination.
        Updates the status label with the path where the file was saved.

        Returns:
            None
        """
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
        """
        Runs the original bytecode program loaded in the GUI.

        This method checks if a filename has been loaded. If not, it shows a warning message.
        Otherwise, it saves the current contents of the original bytecode text widget to a temporary
        file and then executes the program using that file.

        Steps:
            1. Verifies that a .bc file has been loaded.
            2. Writes the contents of the original bytecode text widget to 'outputs/temp_original.bc'.
            3. Calls the execute_program method with the temporary file and the label "Original".

        Raises:
            Shows a warning dialog if no file is loaded.
        """
        if not self.filename:
            messagebox.showwarning("Warning", "Load a .bc file first!")
            return
        temp_input = os.path.join("outputs", "temp_original.bc")
        with open(temp_input, "w", encoding="utf-8") as f:
            f.write(self.text_original.get(1.0, tk.END))
        self.execute_program(temp_input, "Original")

    def run_optimized(self):
        """
        Executes the optimized version of the program if available.

        Checks if the optimized filename is set. If not, displays a warning message prompting the user to run the optimizer first.
        If the optimized filename exists, executes the program using the optimized file.

        Returns:
            None
        """
        if not self.optimized_filename:
            messagebox.showwarning("Warning", "Run the optimizer first!")
            return
        self.execute_program(self.optimized_filename, "Optimized")

    def execute_program(self, filename, program_type):
        """
        Executes a bytecode program using an external interpreter and displays the output in the GUI.
        Args:
            filename (str): The path to the bytecode file to execute.
            program_type (str): A label indicating the type of program (e.g., "Main", "Test") for display purposes.
        Behavior:
            - Retrieves user input from the input_entry widget.
            - Runs 'bytecode_interpreter.py' with the given filename, passing user input if provided.
            - Captures and displays standard output and error in the text_output widget.
            - Updates the status label with execution results or errors.
            - Handles timeouts and unexpected exceptions gracefully.
        """
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
        """
        Clears the contents of the text output widget and updates the status label.

        This method enables the text output widget, deletes all its contents,
        disables it again to prevent user editing, and sets the status label to
        indicate that the outputs have been cleared.
        """
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.config(state=tk.DISABLED)
        self.status.config(text="Outputs cleared!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BytecodeGUI(root)
    root.mainloop()
