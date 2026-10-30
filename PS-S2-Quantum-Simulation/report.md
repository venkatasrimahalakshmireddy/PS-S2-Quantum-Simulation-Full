
# Project Report: Real-Time Non-Equilibrium Quantum Dynamics

## Objective
Benchmark first-order Trotterized evolution of a four-qubit transverse-field Ising model under several synthetic processor coupling graphs and simple noise models.

## Model and experiment
The Hamiltonian used in this implementation is
\[
H = -J \sum_{i=0}^{2} Z_i Z_{i+1} - g \sum_{i=0}^{3} X_i,\quad J=1.
\]
The initial state is `|0101>`, total evolution time is `2.0`, transverse field values are `0.5`, `1.0`, and `1.5`, and Trotter step counts are `1`, `2`, and `4`. Each noisy circuit is sampled with 4096 shots.

## Processor hypotheses

### Processor A
A five-qubit branching-tree graph is a small sparse baseline. It has low connectivity and may require routing when the logical interaction pattern does not align with its edges.

### Processor B
A nine-qubit sparse graph provides a larger, heavy-hex-inspired comparison point. The label describes the synthetic topology only; it is not a model of a specific IBM device.

### Processor C
A nine-qubit 3×3 grid offers regular nearest-neighbour connectivity. The hypothesis is that a regular two-dimensional graph may offer more predictable routing than a branching tree for some circuits. This must be checked using transpiled depth and gate counts.

### Processor D
A twelve-qubit circulant graph C12(2,3) connects each vertex `i` to `i±2` and `i±3` modulo 12. It has degree four and 24 undirected edges. The hypothesis is that increased connectivity may reduce routing overhead for some mapped circuits, while the larger synthetic device also increases the number of noisy qubits available to the compiler. The actual result must be determined from the generated metrics.

## Metrics
- Transpiled circuit depth
- Transpiled CX gate count
- Estimated extra CX gates relative to an unconstrained transpilation (a proxy, not an exact SWAP count)
- Ideal Trotter expectation value and error versus exact evolution
- Noisy sampled expectation value and error versus exact evolution

## Results
Run `python run_experiment.py` and use `results/tables/benchmark_results.csv` to report measured results. Do not claim that any processor is best until the output has been generated and checked. Synthetic depolarizing and readout noise values are illustrative, not calibrated to real hardware.

## Limitations
This is a classical simulation and a simplified synthetic benchmark. It does not demonstrate execution on physical quantum hardware. The current benchmark's measured observable is `<Z0>`; conclusions should be limited to that observable, parameter grid, and simulator noise assumptions.
