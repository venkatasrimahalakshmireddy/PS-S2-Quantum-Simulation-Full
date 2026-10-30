
import json
from pathlib import Path
from qiskit.transpiler import CouplingMap
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

ROOT = Path(__file__).resolve().parents[1]

def load_processor(name: str):
    path = ROOT / "processors" / f"processor_{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Processor configuration not found: {path}")
    config = json.loads(path.read_text(encoding="utf-8"))
    coupling = CouplingMap(couplinglist=config["coupling_edges"])
    noise = NoiseModel()
    noise_cfg = config["noise"]
    p1 = float(noise_cfg["one_qubit_depolarizing_p"])
    p2 = float(noise_cfg["cx_depolarizing_p"])
    pr = float(noise_cfg["readout_error_p"])
    if p1:
        error1 = depolarizing_error(p1, 1)
        for gate in ("x", "sx", "rz"):
            if gate != "rz":
                noise.add_all_qubit_quantum_error(error1, gate)
    if p2:
        noise.add_all_qubit_quantum_error(depolarizing_error(p2, 2), "cx")
    if pr:
        readout = ReadoutError([[1-pr, pr], [pr, 1-pr]])
        noise.add_all_qubit_readout_error(readout)
    return config, coupling, noise
