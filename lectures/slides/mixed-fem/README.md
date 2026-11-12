# Mixed finite element methods

## Lecture 1: near-incompressibility, locking, and pressure

[Slides (PDF)](chapter10_mixed_methods_lecture01.pdf) ·
[LaTeX source](chapter10_mixed_methods_lecture01.tex)

The lecture develops volume change in small-strain elasticity, volumetric
locking, and the displacement–pressure formulation. A four-triangle example
shows the restriction imposed by discrete incompressibility. Computed
plane-strain examples keep the exact displacement and applied load fixed while
increasing the bulk modulus. The final part derives both mixed variational
equations and explains pressure as a Lagrange multiplier.

Stable displacement–pressure pairs, the inf–sup condition, and the discrete
block system are reserved for the next lecture.

### Local references

- Arnold, MATH 8445–8446 notes, Chapter 9, §9.4, printed pp. 155–157
  (PDF pp. 159–161).
- Jog, *Introduction to the Finite Element Method*, §5.4, printed pp. 114–115
  (PDF pp. 115–116).
- The local Belytschko nonlinear-FEM notes compilation: Chapter 5, Example 5.1
  (PDF p. 261); Chapter 8, §8.1, printed pp. 5–6 (PDF pp. 455–456).

These files are in the repository's local `references/` directory. The
four-triangle calculation and manufactured-solution test are course examples,
not reproduced reference figures.

### Build

From this directory:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter10_mixed_methods_lecture01.tex
cp build/chapter10_mixed_methods_lecture01.pdf chapter10_mixed_methods_lecture01.pdf
```

To regenerate the two computed locking plots and their data:

```bash
conda run -n finite-elements python figures/make_locking_figures.py
```

This calculation uses displacement-only linear triangular elements in
FEniCSx. It does not yet implement a mixed solver. The data are retained in
`figures/locking_results.csv`.
