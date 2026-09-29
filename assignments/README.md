# Assignments

- [Assignment 1: Mathematical Foundations](assignment-01.qmd)
- [Assignment 2: Mathematical Foundations](assignment-02.qmd)
- [Assignment 3: Variational Formulations and Energy Principles](assignment-03.qmd)
- [Assignment 4: Finite Element Computation in One and Two Dimensions](assignment-04.qmd)

The Chapter 6 lecture notebook distributed with Assignment 4 is available at
[`notebooks/diffusion/diffusion_2d_demo.ipynb`](../notebooks/diffusion/diffusion_2d_demo.ipynb).
Create and activate the repository's Conda environment, register its Jupyter
kernel, and launch JupyterLab by following
[`environment/README.md`](../environment/README.md). Use the kernel
**Python (Finite Elements)** for the assignment notebooks.

## Problem headings

Write each problem as a level-one heading with the `problem` class and a
`marks` attribute:

```markdown
# Sequences and limits {.problem marks="10"}
```

The assignment filter numbers these headings in document order and displays
the example above as `Problem 1 (10 marks): Sequences and limits`. Move the
entire problem section when reordering problems; the displayed numbers update
automatically in both HTML and PDF.

Render the assignment from the repository root with

```bash
quarto render assignments/assignment-01.qmd
```

The HTML and PDF files are written to `assignments/_output/`.
