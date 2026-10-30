
from pathlib import Path
import pandas as pd
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector
from src.processors import load_processor, ROOT
from src.problem import trotter_circuit, exact_z0, z0_from_counts
from src.metrics import absolute_error
from src.visualization import plot_topology, plot_comparison

FIELDS = (0.5, 1.0, 1.5)
TROTTER_STEPS = (1, 2, 4)

def ideal_z0_from_circuit(g, steps):
    qc = trotter_circuit(g, steps, measure=False)
    state = Statevector.from_instruction(qc)
    # Expectation of Z on qubit 0 using the statevector probability distribution.
    probs = state.probabilities()
    value = 0.0
    for index, probability in enumerate(probs):
        value += (1.0 if (index & 1) == 0 else -1.0) * probability
    return float(value)

def main():
    figures = ROOT / "results" / "figures"
    tables = ROOT / "results" / "tables"
    figures.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    rows = []
    for proc_name in ("A", "B", "C", "D"):
        config, coupling, noise_model = load_processor(proc_name)
        plot_topology(config, figures / f"processor_{proc_name}_topology.png")
        backend = AerSimulator(noise_model=noise_model)
        for g in FIELDS:
            for steps in TROTTER_STEPS:
                circuit = trotter_circuit(g, steps, measure=True)
                compiled = transpile(
                    circuit,
                    basis_gates=config["basis_gates"],
                    coupling_map=coupling,
                    optimization_level=config["transpile"]["optimization_level"],
                    seed_transpiler=config["transpile"]["seed_transpiler"],
                )
                ideal_compiled = transpile(
                    circuit, basis_gates=config["basis_gates"],
                    optimization_level=config["transpile"]["optimization_level"],
                    seed_transpiler=config["transpile"]["seed_transpiler"],
                )
                result = backend.run(compiled, shots=config["transpile"]["shots"],
                                     seed_simulator=42).result()
                counts = result.get_counts()
                noisy_z0 = z0_from_counts(counts)
                ideal_z0 = ideal_z0_from_circuit(g, steps)
                exact = exact_z0(g)
                cx_count = compiled.count_ops().get("cx", 0)
                unconstrained_cx = ideal_compiled.count_ops().get("cx", 0)
                rows.append({
                    "processor": proc_name,
                    "num_physical_qubits": config["num_qubits"],
                    "g": g,
                    "trotter_steps": steps,
                    "shots": config["transpile"]["shots"],
                    "compiled_depth": compiled.depth(),
                    "compiled_cx_count": int(cx_count),
                    "unconstrained_cx_count": int(unconstrained_cx),
                    "estimated_extra_cx": int(max(0, cx_count - unconstrained_cx)),
                    "ideal_trotter_z0": ideal_z0,
                    "noisy_z0": noisy_z0,
                    "exact_z0": exact,
                    "ideal_abs_error": absolute_error(ideal_z0, exact),
                    "noisy_abs_error": absolute_error(noisy_z0, exact),
                })
                print(f"Processor {proc_name} | g={g} | steps={steps} | "
                      f"depth={compiled.depth()} | noisy error={rows[-1]['noisy_abs_error']:.5f}")
    df = pd.DataFrame(rows)
    csv_path = tables / "benchmark_results.csv"
    df.to_csv(csv_path, index=False)
    plot_comparison(rows, figures / "trotter_error_comparison.png")
    print(f"\nSaved {len(df)} benchmark rows to: {csv_path}")
    print(f"Figures saved to: {figures}")

if __name__ == "__main__":
    main()
