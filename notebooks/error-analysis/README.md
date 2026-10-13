# Error-analysis notebooks

## `elasticity_convergence.ipynb`

This notebook accompanies the third Chapter 7 lecture. It first uses a smooth
manufactured displacement on the unit square to verify the predicted $P_1$
rates in the $L^2$ norm, $H^1$ seminorm, and elastic energy norm. It then solves
an L-shaped elasticity problem to show the field concentration produced by a
reentrant corner. The second problem has no known exact solution and is not
presented as an exact-error convergence study.

Run it after activating the repository environment:

```bash
conda activate finite-elements
jupyter lab notebooks/error-analysis/elasticity_convergence.ipynb
```
