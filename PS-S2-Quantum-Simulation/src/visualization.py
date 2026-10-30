
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

def plot_topology(config, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    graph = nx.Graph()
    graph.add_nodes_from(range(config["num_qubits"]))
    graph.add_edges_from(map(tuple, config["coupling_edges"]))
    plt.figure(figsize=(6, 4.5))
    if config["num_qubits"] == 9 and len(config["coupling_edges"]) == 12:
        pos = nx.spring_layout(graph, seed=42)
    else:
        pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx(graph, pos=pos, node_size=650, font_size=9, width=1.5)
    plt.title(config["name"] + " topology")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(str(out_path), dpi=160)
    plt.close()

def plot_comparison(rows, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    for proc in sorted({r["processor"] for r in rows}):
        subset = [r for r in rows if r["processor"] == proc]
        subset.sort(key=lambda r: (r["g"], r["trotter_steps"]))
        labels = [f'g={r["g"]}, n={r["trotter_steps"]}' for r in subset]
        values = [r["noisy_abs_error"] for r in subset]
        ax.plot(range(len(values)), values, marker="o", label=proc)
    ax.set_xlabel("Cases (ordered by g and Trotter steps)")
    ax.set_ylabel("Absolute error in <Z0>")
    ax.set_title("Noisy simulation error by processor")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(str(out_path), dpi=160)
    plt.close(fig)
