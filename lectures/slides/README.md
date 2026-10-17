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

## `apriori-error/`

The first Chapter 7 lecture covers the continuous and discrete problem, error
norms, Galerkin orthogonality, best approximation, and C\'ea's lemma. The
second deck, `chapter07_convergence_lecture.tex`, introduces finite element
interpolation and continues through shape regularity and the energy- and
$H^1$-norm estimates. The third
deck, `chapter07_duality_verification_lecture.tex`, summarizes the duality
argument for the $L^2$ rate and emphasizes numerical verification using a
smooth linear-elasticity problem and an L-shaped body with a reentrant corner.
Its FEniCSx notebook is maintained at
[`notebooks/error-analysis/elasticity_convergence.ipynb`](../../notebooks/error-analysis/elasticity_convergence.ipynb).

Build the slides from that directory with:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter07_apriori_error_lecture.tex
cp build/chapter07_apriori_error_lecture.pdf chapter07_apriori_error_lecture.pdf

conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter07_convergence_lecture.tex
cp build/chapter07_convergence_lecture.pdf chapter07_convergence_lecture.pdf

conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter07_duality_verification_lecture.tex
cp build/chapter07_duality_verification_lecture.pdf chapter07_duality_verification_lecture.pdf
```

## `aposteriori-error/`

The first Chapter 8 lecture introduces the residual functional, mesh facets,
normal-flux jumps, and elementwise integration by parts. The second deck,
`chapter08_estimator_reliability_lecture.tex`, completes the element-and-facet
residual representation, constructs the residual estimator, and develops its
reliability bound through one- and two-dimensional examples.

Build the slides from that directory with:

```bash
conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter08_residual_estimation_lecture.tex
cp build/chapter08_residual_estimation_lecture.pdf chapter08_residual_estimation_lecture.pdf

conda run -n finite-elements latexmk -pdf \
  -interaction=nonstopmode -halt-on-error \
  -outdir=build chapter08_estimator_reliability_lecture.tex
cp build/chapter08_estimator_reliability_lecture.pdf chapter08_estimator_reliability_lecture.pdf
```
