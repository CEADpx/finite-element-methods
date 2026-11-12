# Nonlinear finite element methods

[Hyperelastic cantilever](hyperelasticity_newton.ipynb) accompanies Lecture 3.
It uses UFL derivatives and DOLFINx's
`NonlinearProblem` to solve a sequence of load increments. The outputs show
the load-displacement response and check the final deformation determinant.

[Nonlinear diffusion and reaction](nonlinear_diffusion_reaction.ipynb)
accompanies Lecture 4. It gives the residual and tangent explicitly and
compares the finite element solution with a known exact solution.

Use the **Python (Finite Elements)** kernel. Run the cells in order.
The saved outputs provide a completed run. Environment setup is described in
the [environment guide](../../environment/README.md).
