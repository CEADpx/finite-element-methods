# Assignments

- [Assignment 1: Mathematical Foundations](assignment-01/assignment-01.qmd)
- [Assignment 2: Mathematical Foundations](assignment-02/assignment-02.qmd)
- [Assignment 3: Variational Formulations and Energy Principles](assignment-03/assignment-03.qmd)
- [Assignment 4: Finite Element Computation in One and Two Dimensions](assignment-04/assignment-04.qmd)
- [Assignment 5: Adaptive Refinement of a Mounting Bracket](assignment-05/notebooks/problem1.ipynb)

Assignment 5 is provided only as a notebook. It contains the complete problem,
tasks, marks, supplied routines and submission instructions. Students implement
marking and refinement studies for a two-dimensional plane-stress bracket,
compare adaptive and uniform refinement, and assess deflection and corner
stress. They submit the completed notebook; there is no separate handout or report.

The Assignment 4 notebooks are in
[`assignment-04/notebooks/`](assignment-04/notebooks/). They build on the
lecture notebooks
[`notebooks/assembly/assembly_demo.ipynb`](../notebooks/assembly/assembly_demo.ipynb)
and
[`notebooks/diffusion/diffusion_2d_demo.ipynb`](../notebooks/diffusion/diffusion_2d_demo.ipynb).
Create and activate the repository's Conda environment, register its Jupyter
kernel, and launch JupyterLab by following
[`environment/README.md`](../environment/README.md). Use the kernel
**Python (Finite Elements)** for the assignment notebooks.

## Quarto problem headings

For `.qmd` assignment sheets, write each problem as a level-one heading with
the `problem` class and a `marks` attribute:

```markdown
# Sequences and limits {.problem marks="10"}
```

The assignment filter numbers these headings in document order and displays
the example above as `Problem 1 (10 marks): Sequences and limits`. Move the
entire problem section when reordering problems; the displayed numbers update
automatically in both HTML and PDF.

Assignments 1-4 have their own folders holding a `.qmd` source, rendered PDF
and any notebooks. Assignment 5 is notebook-only and does not need Quarto
rendering. Render the `.qmd` assignments from the repository root with

```bash
quarto render assignments
```

or one assignment with `quarto render assignments/assignment-01/assignment-01.qmd`.
The PDF is written next to the `.qmd` file and is committed to git. After each
render, `filters/move-outputs.py` moves the HTML, `.tex`, and `_files/` folder
into `assignment-NN/_output/`, which git ignores.
