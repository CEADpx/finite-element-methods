"""Execute the notebook cells and verify the computed finite element results."""

import json
import os
from itertools import pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import nbformat
import numpy as np

demo_dir = Path(__file__).resolve().parent
os.chdir(demo_dir)
notebook = nbformat.read(demo_dir / "diffusion_2d.ipynb", as_version=4)

rows = []
for num_subdivisions in [8, 16, 32]:
    scope = {}
    for cell in notebook.cells:
        if cell.cell_type != "code":
            continue

        source = cell.source
        if "parameters" in cell.metadata.get("tags", []):
            source = source.replace("N = 16", f"N = {num_subdivisions}")
        exec(compile(source, "diffusion_2d.ipynb", "exec"), scope)  # noqa: S102
        plt.close("all")

    assert scope["problem"].solver.getConvergedReason() > 0
    assert np.max(np.abs(scope["u_h"].x.array[scope["boundary_dofs"]])) < 1e-12
    assert scope["balance_relative"] < 1e-10
    rows.append(
        {
            "N": num_subdivisions,
            "h_max": np.sqrt(2) / num_subdivisions,
            "L2": scope["error_L2"],
            "energy": scope["error_energy"],
            "balance": scope["balance_relative"],
        }
    )

for previous, current in pairwise(rows):
    current["L2_rate"] = float(np.log2(previous["L2"] / current["L2"]))
    current["energy_rate"] = float(
        np.log2(previous["energy"] / current["energy"])
    )

assert 1.9 < rows[-1]["L2_rate"] < 2.1
assert 0.9 < rows[-1]["energy_rate"] < 1.1

(demo_dir / "verification.json").write_text(json.dumps(rows, indent=2) + "\n")
print(json.dumps(rows, indent=2))
