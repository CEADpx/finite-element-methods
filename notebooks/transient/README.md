# Transient notebooks

[Heat conduction with the theta method](heat_theta.ipynb) accompanies
[Transient FEM, Lecture 2](../../lectures/slides/transient-fem/chapter12_transient_lecture02.pdf).
It contains the problem, boundary diagram, time-step variational forms,
FEniCSx implementation, and saved results.

Use the [repository environment](../../environment/README.md), select
**Python (Finite Elements)** in Jupyter, and run the cells in order.
The example is a plate with a localized heater, a cooled left edge, and
insulated remaining edges. Material properties and thermal diffusivity are
explicit. The main calculation uses backward Euler; the final section
compares time-step sizes at a fixed final time.
