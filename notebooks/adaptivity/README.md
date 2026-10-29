# Adaptive finite element computation

[`residual_adaptivity.ipynb`](residual_adaptivity.ipynb) accompanies the closing
Chapter 8 lecture. Its first example is a localized Gaussian solution on a
square, adapted from Larson–Bengzon §4.9.3. The known solution permits direct
energy-error and effectivity calculations. An additional example solves
`-Delta u = 1` on an L-shaped domain with zero prescribed boundary values.

The notebook exposes one solve–estimate–mark–refine cycle, including the
element and interior-facet contributions, Dörfler marking, and local
refinement. A short loop repeats these steps and compares adaptive and uniform
refinement at comparable FE space sizes. Error and estimator are plotted
separately for the Gaussian example. The exact corner-domain solution is
unknown, so that example does not report true errors or effectivity.

Start JupyterLab from the repository root and select **Python (Finite Elements)**:

```bash
conda activate finite-elements
jupyter lab notebooks/adaptivity/residual_adaptivity.ipynb
```

Use **Restart Kernel and Run All Cells** to reproduce the saved outputs.
The notebook is tested with DOLFINx 0.11.0 on one MPI process. Environment and
macOS compiler instructions are maintained in
[`environment/README.md`](../../environment/README.md).

## Implementation references

Jørgen S. Dokken's
[adaptive mesh refinement tutorial](https://jsdokken.com/dolfinx-tutorial/chapter2/amr.html#error-indicator)
illustrates DG0 indicator assembly with separate half contributions from the
two sides of an interior facet. The notebook writes these contributions
explicitly, then shows their numerical values and the selected element IDs.

The tutorial uses a Laplace eigenvalue problem, NetGen, and threshold marking.
This notebook retains our Poisson problems, edge-length weights, Dörfler
marking, and built-in
[dolfinx.mesh.refine](https://docs.fenicsproject.org/dolfinx/v0.11.0/python/generated/dolfinx.mesh.html#dolfinx.mesh.refine).
No additional package is required. Both examples execute the complete
solve–estimate–mark–refine loop.

## Concentrated versus distributed force

[`elasticity_point_load_comparison.ipynb`](elasticity_point_load_comparison.ipynb)
compares a nodal point force with a fixed-width boundary traction on a
plane-stress cantilever. It includes uniform and prescribed near-load refinement,
checks force and moment balance, and compares compliance, successive-mesh energy
differences, and local energy density. This is a loading-model
comparison, not an application of the standard residual estimator to a point
force. The comparison is a worked example in Chapter 8 and forms the basis
of Assignment 5's elasticity problem. The student notebooks, with assignment
tasks, are in [`assignments/assignment-05/notebooks/`](../../assignments/assignment-05/notebooks/).

The cantilever notebook also implements residual-based adaptive refinement for
two fixed-width distributed tractions. At cycles 0, 2, and 4, it displays the
indicators, marked elements, and conforming refined mesh. All Neumann facets
are included, even where the prescribed traction is zero. This adaptive
calculation is distinct from the prescribed near-point refinement study;
no standard residual error bound is claimed for the ideal point force.
