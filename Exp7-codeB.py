import urllib.request
import os
import sys

so_url = "https://github.com/Lab2Phys/Experiment-7-B/raw/refs/heads/main/module_RLC_inverse.so"
so_filename = "module_RLC_inverse.so"

try:
    print("Downloading compiled module...")
    urllib.request.urlretrieve(so_url, so_filename)
    print("Module downloaded successfully.")
    
    if '.' not in sys.path:
        sys.path.insert(0, '.')
    
    import module_RLC_inverse
    from module_RLC_inverse import CircuitSolver, FrequencyAnalyzer, PDFReportGenerator, CircuitUI
    
    print("Compiled module loaded successfully.")
    
except Exception as e:
    print(f"Error loading compiled module: {e}")
    print("Fallback: Please ensure the module file is available.")
    sys.exit(1)

import math
import numpy as np
from scipy import linalg, optimize
import ipywidgets as widgets
from IPython.display import display, clear_output
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

DECIMAL_PRECISION = 4

np.set_printoptions(precision=DECIMAL_PRECISION)

f_start = 1
f_end = 10000
f_points = 5000

N = 6
R = 1000
L = 10e-3
c1 = 680e-9
c2 = 220e-9
i = 1j

source_branch_nodes = (2, 4)

def _quiet_pip_install(packages):
    import subprocess
    cmd = [sys.executable, "-m", "pip", "install"] + packages
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

_quiet_pip_install(["ipywidgets", "tabulate", "matplotlib", "scipy"])

def build_edges(f):
    w = 2 * np.pi * f
    x = i * L * w
    x1 = 1 / (i * c1 * w)
    x2 = 1 / (i * c2 * w)
    edges = [
        (1, 2, x + x1), (1, 3, R + x1), (1, 4, R + x2), (2, 3, R + x2),
        (2, 4, R), (2, 5, R + x1), (2, 6, x + x2), (3, 5, R + x),
        (4, 6, x1 + x2), (5, 6, R)
    ]
    return edges

collected_data = {"frequencies": [], "node_pairs": [], "target_voltages": [], "veff": None}
node_pairs = [(i, j) for i in range(1, N+1) for j in range(i+1, N+1)]
node_pairs_str = [f"({i},{j})" for i, j in node_pairs]
final_results = []

circuit_ui = CircuitUI(
    N=N,
    f_start=f_start,
    f_end=f_end,
    f_points=f_points,
    DECIMAL_PRECISION=DECIMAL_PRECISION,
    build_edges=build_edges,
    source_branch_nodes=source_branch_nodes,
    collected_data=collected_data,
    node_pairs=node_pairs,
    node_pairs_str=node_pairs_str,
    final_results=final_results
)

print("\nNote: Keep the same veff for all measurements!")
display(circuit_ui.input_row1, circuit_ui.input_row2, circuit_ui.button_row, circuit_ui.output_area)