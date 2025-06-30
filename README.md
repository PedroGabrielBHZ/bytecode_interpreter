# Bytecode Interpreter

[![Test and Deploy](https://github.com/PedroGabrielBHZ/bytecode-interpreter/actions/workflows/python-tests.yml/badge.svg)](https://github.com/PedroGabrielBHZ/bytecode_interpreter/blob/main/.github/workflows/python-tests.yml)
[![Deploy Status](https://img.shields.io/badge/deployment-automatic-brightgreen)](https://fly.io)

A stack-based bytecode interpreter and optimizer with a graphical interface, developed for the Compilers course.

## Features
- **Interpreter**: Executes stack-based bytecode with support for variables, arithmetic, control flow, and function calls.
- **Optimizer**: Removes redundant instructions and performs constant folding.
- **GUI**: User-friendly interface for loading, editing, optimizing, running, and saving .bc files.
- **Web Interface**: Modern web-based interface that can be deployed to the cloud.
- **Comprehensive Tests**: All logic is tested using Python's `unittest` framework.

## Project Structure
- `bytecode_interpreter.py`: Main interpreter logic
- `bytecode_optimizer.py`: Optimizer logic
- `bytecode_gui.py`: Tkinter GUI for the interpreter and optimizer
- `app.py`: Flask web application
- `templates/`: HTML templates for the web interface
- `outputs/`: All generated/optimized files are saved here
- `tests/`: Contains `.bc` test files and Python unittests

## How to Use

### Web Interface
```bash
pip install -r requirements.txt
python app.py
```
Open your browser to `http://localhost:5000`

### GUI
```bash
python bytecode_gui.py
```

### Command Line
Run a program from file:
```bash
python bytecode_interpreter.py tests/test1.bc
```
Run from standard input:
```bash
python bytecode_interpreter.py < tests/test1.bc
```

### Optimizer
```bash
python bytecode_optimizer.py tests/test_unoptimized.bc outputs/optimized.bc
```

## Running Tests

### All unittests (recommended)
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Run a specific test file
```bash
python -m unittest tests.test_interpreter
```

## Deployment

### Automatic Deployment to Fly.io
This project is configured for automatic deployment to Fly.io on every commit to the main branch.

**Setup Instructions**: See `DEPLOYMENT_AUTOMATION.md` for detailed setup guide.

Quick setup:
1. Get Fly.io API token: `flyctl auth token`
2. Add `FLY_API_TOKEN` to GitHub repository secrets
3. Commit to main branch → Automatic deployment! 🚀

### Manual Deployment
```bash
flyctl launch
flyctl deploy
```

### Web Interface to Fly.io
See `WEB_DEPLOYMENT.md` for detailed deployment instructions.

Quick deploy:
```bash
flyctl launch
flyctl deploy
```

## Web API Endpoints

- `POST /api/run` - Execute bytecode and return JSON results
- `POST /api/optimize` - Optimize bytecode and return JSON results  
- `GET /health` - Health check endpoint

## Test Files
See `tests/README.md` for details on all test cases and expected results.

## Requirements
- Python 3.7+
- No external dependencies required for core features

---

For more details, see the docstrings in each file and the test suite in `tests/`.
