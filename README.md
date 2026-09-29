# Advanced Finite Element Methods

This repository contains an open graduate-level book and teaching materials for
**ME/BME 736: Advanced Finite Element Methods** at South Dakota Mines. The
material develops the mathematical formulation of finite element methods and
connects it to explicit numerical implementation and FEniCSx computations.
Heat conduction and solid mechanics are used as recurring model problems.

- [Read the book online](https://ceadpx.github.io/finite-element-methods/)
- [Download the book as a PDF](https://ceadpx.github.io/finite-element-methods/Advanced-Finite-Element-Methods.pdf)
- [See the current chapter status](https://ceadpx.github.io/finite-element-methods/status.html)

## Book

The Quarto sources are in [`book/`](book/). The current complete chapters cover:

1. introduction to the finite element method;
2. mathematical foundations;
3. partial differential equations and variational formulations;
4. model problems in heat transfer and solid mechanics;
5. the finite element method in one dimension; and
6. finite element approximation in multiple dimensions.

The book also includes appendices on real-analysis essentials and tensor
notation and index calculus. Later chapters will address error estimation,
adaptivity, constraints, mixed methods, nonlinear and transient problems, and
PDE-constrained optimization. The development status of each chapter is
maintained in [`book/status.qmd`](book/status.qmd).

To render both the HTML and PDF versions from the repository root, use:

```bash
quarto render book
```

The rendered files are written to `book/_book/`.

## Assignments and computational notebooks

The assignment sources are in [`assignments/`](assignments/):

- Assignments 1 and 2: mathematical foundations;
- Assignment 3: variational formulations and energy principles; and
- Assignment 4: finite element computation in one and two dimensions.

Assignment 4 is supported by two executable notebooks:

- [`notebooks/assembly/assembly_demo.ipynb`](notebooks/assembly/assembly_demo.ipynb)
  develops one-dimensional assembly explicitly with NumPy; and
- [`notebooks/diffusion/diffusion_2d_demo.ipynb`](notebooks/diffusion/diffusion_2d_demo.ipynb)
  solves a two-dimensional diffusion problem with FEniCSx and examines mesh
  refinement and error.

See [`assignments/README.md`](assignments/README.md) for assignment rendering
and notebook-submission instructions.

## Lecture materials and handouts

The topic-based lecture materials in [`lectures/slides/`](lectures/slides/)
currently include:

- one-dimensional finite element assembly, boundary conditions, and reactions;
  and
- multidimensional finite elements, linear triangles, basis-function support,
  matrix sparsity, and a two-dimensional diffusion example.

Each topic directory contains the LaTeX source, figures, and final PDF. Build
instructions are given in
[`lectures/slides/README.md`](lectures/slides/README.md).

Focused notes in [`handouts/`](handouts/) cover one-dimensional finite elements,
local-to-global assembly, and examples of weak derivatives.

## Course documents

The [`course/`](course/) directory contains the Fall 2026
[ME/BME 736 syllabus](course/syllabus/ME736_Syllabus_Fall2026.pdf) and
[course flyer](course/flyer/ME736_Flyer_Fall2026.pdf).

## Software environment

The book, notebooks, and assignments use a single Conda environment containing
Quarto, Python, Jupyter, FEniCSx, MPI, PETSc, and the supporting scientific
Python packages. Create it with:

```bash
conda env create -f environment/environment.yml
conda activate finite-elements
```

Complete setup, TinyTeX, Jupyter-kernel, MPI, and verification instructions are
provided in [`environment/README.md`](environment/README.md).

### Copyright and license

Copyright (C) 2026 Prashant K. Jha.

This work is free: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. It is
distributed without any warranty; see [`LICENSE`](LICENSE) for the full terms.
