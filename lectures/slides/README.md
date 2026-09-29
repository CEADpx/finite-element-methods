# Lecture slides

Lecture materials are grouped by topic.

## `finite-element-assembly/`

One-dimensional finite element assembly, boundary conditions, reactions, and
the accompanying NumPy demonstration. The notebook is maintained at
[`notebooks/assembly/assembly_demo.ipynb`](../../notebooks/assembly/assembly_demo.ipynb).

Build the slides from that directory with:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build fem_assembly_lecture.tex
cp build/fem_assembly_lecture.pdf fem_assembly_lecture.pdf
```

## `multidimensional-fem/`

Chapter 6 lecture on linear triangular elements, mapped integration, assembly,
and the first two-dimensional FEniCSx diffusion demonstration. The notebook
used with this lecture and Assignment 4 is maintained once at
[`notebooks/diffusion/diffusion_2d_demo.ipynb`](../../notebooks/diffusion/diffusion_2d_demo.ipynb).

Build the slides from that directory with:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter06_2d_fem_lecture.tex
cp build/chapter06_2d_fem_lecture.pdf chapter06_2d_fem_lecture.pdf
```

Each topic directory contains its own `figures/` directory. Generated LaTeX
intermediate files belong in the ignored local `build/` directory. The slide
source, figures, and final PDF are retained in the topic directory and
committed together. Shared notebooks remain under the repository-level
`notebooks/` directory rather than being duplicated with individual slide
decks.
