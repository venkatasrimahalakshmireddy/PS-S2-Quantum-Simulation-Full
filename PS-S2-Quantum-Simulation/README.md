
# PS-S2 — Real-Time Non-Equilibrium Quantum Dynamics

A runnable Qiskit/Aer project for benchmarking first-order Trotterized transverse-field Ising dynamics across four synthetic processor topologies.

## Requirements
- Python 3.10 or 3.11 recommended
- Windows, macOS, or Linux

## Setup (Windows PowerShell)
```powershell
cd PS-S2-Quantum-Simulation
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python run_experiment.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Experiment
- Model: 4-qubit transverse-field Ising chain
- Initial state: `|0101>`
- Total evolution time: `t = 2.0`
- Field values: `g = 0.5, 1.0, 1.5`
- Trotter steps: `1, 2, 4`
- Shots: `4096`
- Processors: A, B, C, D

Outputs are written under `results/`:
- `tables/benchmark_results.csv`
- `figures/processor_*_topology.png`
- `figures/trotter_error_comparison.png`

## Processor topologies
- A: 5-qubit branching tree
- B: 9-qubit sparse heavy-hex-inspired graph
- C: 9-qubit 3×3 grid
- D: 12-qubit circulant graph C12(2,3), where node i connects to i±2 and i±3 modulo 12

These are synthetic benchmark models, not claims about actual hardware.

## Important
The program generates measurements from a simulator. Do not report performance improvements until you have run the code and inspected the CSV output. This package is a reconstructed, runnable project scaffold based on the described project requirements; compare it with your original repository before submitting.
