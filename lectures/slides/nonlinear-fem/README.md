# Nonlinear finite element methods

## Lecture 1: large deformation and reference formulation

[Lecture PDF](chapter11_large_deformation_lecture01.pdf)
and [LaTeX source](chapter11_large_deformation_lecture01.tex).

The lecture begins with a loaded body whose current geometry is unknown.
It develops the mappings needed to express the same equilibrium problem on
the known reference body: line elements, volumes, oriented surface areas,
and forces. The strain measures are introduced through changes in squared
line length, not a separate survey of strain definitions.

Slides 1–18 are the core: the loaded problem, necessary geometry, Nanson's
formula, first Piola–Kirchhoff stress, mapped equilibrium, and the closed
hyperelastic reference problem. One local numerical deformation is reused
for the geometry and force examples; it is not asserted to be the solution
of the loaded, clamped body.

Slides 19–24 provide continuation material on the variational problem and
scalar Newton illustration. Cover them if discussion leaves time; otherwise
continue with them in Lecture 2. The constitutive tangent, FE assembly,
and implementation belong to later lectures.

### References and conventions

- Course book, Chapter 4, **Finite deformation and hyperelasticity**.
- Local Belytschko notes, Chapter 2, §2.2, for material coordinates and the
  reference-area description of force.
- Local Belytschko notes, Chapter 3, §§3.2–3.4; in particular §3.4.2,
  printed p. 3-33, for the surface-area and stress transformations.
- Local Belytschko notes, Chapter 6, §§6.3.3–6.3.4, for Newton's method.

The lecture follows the book's column-vector convention:
`t_0 = P N` and `P = J sigma F^{-T}`. The nominal-stress tensor in the local
Belytschko notes uses the transpose convention. Its formulas must be
translated rather than copied directly.

All diagrams are editable TikZ objects in the lecture source. No external
figure files are required.

### Build

Run from this directory:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter11_large_deformation_lecture01.tex
cp build/chapter11_large_deformation_lecture01.pdf chapter11_large_deformation_lecture01.pdf
```
