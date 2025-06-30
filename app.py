"""
Flask web application for the Bytecode Interpreter.
Provides a web interface that mimics the GUI functionality.
"""

import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from bytecode_interpreter import BytecodeInterpreter
from bytecode_optimizer import BytecodeOptimizer
import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from config import config

app = Flask(__name__)

# Load configuration
config_name = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config.get(config_name, config["default"]))

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Ensure SECRET_KEY is always set (additional fallback for production safety)
if not app.config.get("SECRET_KEY"):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "fallback-secret-key-please-set-proper-one")

# Ensure outputs directory exists
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUTPUTS_DIR, exist_ok=True)


class WebBytecodeRunner:
    """Helper class to run bytecode and capture output safely."""

    @staticmethod
    def run_bytecode(code):
        """Run bytecode and return output and any errors."""
        interpreter = BytecodeInterpreter()

        # Capture stdout and stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            interpreter.load_program(code)

            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                interpreter.run()

            output = stdout_capture.getvalue()
            errors = stderr_capture.getvalue()

            return {
                "success": True,
                "output": output,
                "errors": errors,
                "stack": interpreter.stack,
                "variables": interpreter.variables,
                "halted": interpreter.halted,
            }

        except Exception as e:
            return {
                "success": False,
                "output": stdout_capture.getvalue(),
                "errors": f"Runtime error: {str(e)}",
                "stack": getattr(interpreter, "stack", []),
                "variables": getattr(interpreter, "variables", {}),
                "halted": True,
            }

    @staticmethod
    def optimize_bytecode(code):
        """Optimize bytecode and return the result."""
        try:
            optimizer = BytecodeOptimizer()
            optimizer.load_program(code)  # Load the program first
            optimized_code, stats = optimizer.optimize()  # Then optimize
            return {
                "success": True,
                "optimized_code": optimized_code,
                "stats": stats,
                "errors": None,
            }
        except Exception as e:
            return {
                "success": False,
                "optimized_code": code,
                "errors": f"Optimization error: {str(e)}",
            }


@app.route("/")
def index():
    """Main page with the bytecode editor."""
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_bytecode():
    """Run bytecode and return results."""
    code = request.form.get("code", "").strip()

    if not code:
        flash("Please enter some bytecode to run.", "warning")
        return redirect(url_for("index"))

    result = WebBytecodeRunner.run_bytecode(code)

    return render_template("index.html", code=code, result=result)


@app.route("/optimize", methods=["POST"])
def optimize_bytecode():
    """Optimize bytecode and return results."""
    code = request.form.get("code", "").strip()

    if not code:
        flash("Please enter some bytecode to optimize.", "warning")
        return redirect(url_for("index"))

    result = WebBytecodeRunner.optimize_bytecode(code)

    if result["success"]:
        flash("Bytecode optimized successfully!", "success")
    else:
        flash(f'Optimization failed: {result["errors"]}', "danger")

    return render_template(
        "index.html", code=result["optimized_code"], optimization_result=result
    )


@app.route("/load_example")
def load_example():
    """Load an example bytecode program."""
    example_code = """# Example: Calculate factorial of 5
PUSH 5
STORE n
PUSH 1
STORE result

loop:
    LOAD n
    JZ end
    LOAD result
    LOAD n
    MUL
    STORE result
    LOAD n
    PUSH 1
    SUB
    STORE n
    JMP loop

end:
    LOAD result
    PRINT
    HALT"""

    return render_template("index.html", code=example_code)


@app.route("/examples")
def examples():
    """Show available example programs."""
    examples_list = [
        {
            "name": "Factorial Calculator",
            "description": "Calculate factorial of 5",
            "code": """# Calculate factorial of 5
PUSH 5
STORE n
PUSH 1
STORE result

loop:
    LOAD n
    JZ end
    LOAD result
    LOAD n
    MUL
    STORE result
    LOAD n
    PUSH 1
    SUB
    STORE n
    JMP loop

end:
    LOAD result
    PRINT
    HALT""",
        },
        {
            "name": "Simple Calculator",
            "description": "Add two numbers",
            "code": """# Simple addition
PUSH 15
PUSH 25
ADD
PRINT
HALT""",
        },
        {
            "name": "Countdown",
            "description": "Count down from 5 to 1",
            "code": """# Countdown from 5
PUSH 5
STORE counter

loop:
    LOAD counter
    JZ end
    LOAD counter
    PRINT
    LOAD counter
    PUSH 1
    SUB
    STORE counter
    JMP loop

end:
    HALT""",
        },
        {
            "name": "Function Call Example",
            "description": "Function that doubles a number",
            "code": """# Function call example
PUSH 10
CALL double_func
PRINT
HALT

double_func:
    DUP
    ADD
    RET""",
        },
    ]

    return render_template("examples.html", examples=examples_list)


@app.route("/load_example/<int:example_id>")
def load_specific_example(example_id):
    """Load a specific example by ID."""
    examples = [
        """# Calculate factorial of 5
PUSH 5
STORE n
PUSH 1
STORE result

loop:
    LOAD n
    JZ end
    LOAD result
    LOAD n
    MUL
    STORE result
    LOAD n
    PUSH 1
    SUB
    STORE n
    JMP loop

end:
    LOAD result
    PRINT
    HALT""",
        """# Simple addition
PUSH 15
PUSH 25
ADD
PRINT
HALT""",
        """# Countdown from 5
PUSH 5
STORE counter

loop:
    LOAD counter
    JZ end
    LOAD counter
    PRINT
    LOAD counter
    PUSH 1
    SUB
    STORE counter
    JMP loop

end:
    HALT""",
        """# Function call example
PUSH 10
CALL double_func
PRINT
HALT

double_func:
    DUP
    ADD
    RET""",
    ]

    if 0 <= example_id < len(examples):
        return render_template("index.html", code=examples[example_id])
    else:
        flash("Example not found.", "danger")
        return redirect(url_for("index"))


@app.route("/api/run", methods=["POST"])
def api_run():
    """API endpoint to run bytecode (JSON response)."""
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    result = WebBytecodeRunner.run_bytecode(data["code"])
    return jsonify(result)


@app.route("/api/optimize", methods=["POST"])
def api_optimize():
    """API endpoint to optimize bytecode (JSON response)."""
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"error": "No code provided"}), 400

    result = WebBytecodeRunner.optimize_bytecode(data["code"])
    return jsonify(result)


@app.route("/health")
def health():
    """Health check endpoint for deployment."""
    return {"status": "healthy", "service": "bytecode-interpreter"}, 200


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # For development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
