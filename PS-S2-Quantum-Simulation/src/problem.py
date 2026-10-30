
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from scipy.linalg import expm

N_QUBITS = 4
TOTAL_TIME = 2.0
J_COUPLING = 1.0

def trotter_circuit(g: float, steps: int, total_time: float = TOTAL_TIME, measure: bool = True):
    """First-order product-formula circuit for a 4-qubit open TFIM chain."""
    if steps < 1:
        raise ValueError("steps must be >= 1")
    qc = QuantumCircuit(N_QUBITS)
    # |0101> in Qiskit's little-endian convention: q0 and q2 are |1>.
    qc.x(0)
    qc.x(2)
    dt = total_time / steps
    for _ in range(steps):
        # H = -J sum_i Z_i Z_(i+1) - g sum_i X_i
        # exp(-i (-J ZZ)dt) = exp(+i J dt ZZ), implemented by RZZ(-2 J dt).
        for q in range(N_QUBITS - 1):
            qc.rzz(-2.0 * J_COUPLING * dt, q, q + 1)
        for q in range(N_QUBITS):
            qc.rx(2.0 * g * dt, q)
    if measure:
        qc.measure_all()
    return qc

def hamiltonian(g: float):
    terms = []
    for q in range(N_QUBITS - 1):
        label = ["I"] * N_QUBITS
        label[N_QUBITS - 1 - q] = "Z"
        label[N_QUBITS - 1 - (q + 1)] = "Z"
        terms.append(("".join(label), -J_COUPLING))
    for q in range(N_QUBITS):
        label = ["I"] * N_QUBITS
        label[N_QUBITS - 1 - q] = "X"
        terms.append(("".join(label), -float(g)))
    return SparsePauliOp.from_list(terms)

def exact_state(g: float, total_time: float = TOTAL_TIME):
    h = hamiltonian(g).to_matrix()
    initial = np.zeros(2**N_QUBITS, dtype=complex)
    # |0101> with displayed bitstring q3 q2 q1 q0 = 0101.
    initial[int("0101", 2)] = 1.0
    return expm(-1j * h * total_time) @ initial

def exact_z0(g: float, total_time: float = TOTAL_TIME):
    state = exact_state(g, total_time)
    z0 = np.diag([1, -1])
    # Qubit 0 is the least-significant subsystem in the computational basis.
    op = np.kron(np.eye(2**(N_QUBITS-1)), z0)
    return float(np.real(np.vdot(state, op @ state)))

def z0_from_counts(counts):
    total = sum(counts.values())
    if total == 0:
        return float("nan")
    # Qiskit count keys are ordered c3 c2 c1 c0; c0 is the rightmost bit.
    return sum((1 if key.replace(" ", "")[-1] == "0" else -1) * value
               for key, value in counts.items()) / total
