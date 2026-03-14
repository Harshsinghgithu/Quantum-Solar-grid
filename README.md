# Quantum Solar Grid AI

This repository contains a simple quantum-inspired solar grid optimization project.

## Structure

- `quantum-solar-grid-ai/`
  - `app.py` - Entry point for running the simulator.
  - `energy_simulator.py` - Energy simulation logic.
  - `qiskit_optimizer.py` - Qiskit-based optimization logic.
  - `frontend/` - Static frontend files (HTML/CSS/JS).
  - `netlify/`, `netlify-static/` - Additional deployment/static site templates.
  - `requirements.txt` - Python dependencies.

## Setup

1. Create a Python virtual environment and activate it:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r quantum-solar-grid-ai\requirements.txt
   ```

## Running

From the repository root:

```powershell
python quantum-solar-grid-ai\app.py
```

## Notes

- Ensure you have a compatible version of Python (3.10+ recommended).
- The frontend is served as static files; you can open `quantum-solar-grid-ai/frontend/index.html` in a browser for the UI.
