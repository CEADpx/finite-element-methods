# A posteriori error estimation

## Closing lecture and demonstration

The [closing lecture](chapter08_adaptive_fem_lecture.pdf)
([source](chapter08_adaptive_fem_lecture.tex)) completes the key mathematical
steps from quasi-interpolation to the computable residual estimator and
reliability bound, then introduces the FEniCSx demonstration. Allow approximately
20 minutes to collect the theory and explain the loop, 40 minutes for the first
notebook example, 10 minutes for the additional corner example if time permits,
and five minutes for discussion. The figure slides provide saved-run results
for discussion or a fallback; they need not be presented before the live code.

The [companion notebook](../../../notebooks/adaptivity/residual_adaptivity.ipynb)
first solves a localized Gaussian problem on a square, adapted from
Larson–Bengzon §4.9.3, printed pp. 90–92. The solution is normalized and
boundary-corrected to satisfy homogeneous Dirichlet data exactly. It shows
element and facet indicators, one explicit marking/refinement step, repeated
adaptation, true energy errors, effectivity, and a comparison with uniform
refinement. An additional L-shaped-domain example illustrates refinement near
a reentrant corner without claiming knowledge of the exact error.

The longer reading decks below retain the extended derivations and examples.

## Supporting reading decks

The [introductory lecture](chapter08_residual_estimation_lecture.pdf) develops
the residual functional, facets, normal-flux jumps, and elementwise integration
by parts. Its [source](chapter08_residual_estimation_lecture.tex) is unchanged.

The continuation is divided into three parts.

| Part | Slides | Content |
| --- | --- | --- |
| [1: Residual representation and quasi-interpolation](chapter08_estimator_reliability_lecture.pdf) | 24 | Residual representation, nonuniform 1D example, Galerkin subtraction, patches, and the Clément averaging construction and example |
| [2: Estimator and reliability](chapter08_estimator_independent_study.pdf) | 27 | Local approximation estimates, mesh-size weights, local/global indicators, a two-triangle calculation, the reliability proof, and the 1D error comparison |
| [3: Interpretation and adaptive refinement](chapter08_adaptivity_independent_study.pdf) | 14 | Reliability versus efficiency, data oscillation, effectivity, marking, refinement, the adaptive loop, and stopping criteria |

Sources: [Part 1](chapter08_estimator_reliability_lecture.tex),
[Part 2](chapter08_estimator_independent_study.tex), and
[Part 3](chapter08_adaptivity_independent_study.tex).

## Reading order

1. Finish Part 1 through the averaging construction and its worked example.
2. Read Part 2 in order. The local estimates for the quasi-interpolant are
   assumed; the subsequent slides derive the weights and reliability bound
   from them. The two-triangle example retains the facet residuals. The later
   1D argument explains why nodal terms vanish after subtracting the nodal
   interpolant in that special case.
3. Read Part 3 to interpret the estimator and use the indicators in an adaptive
   calculation. It includes a worked bulk-marking and refinement step for the
   same nonuniform 1D example.

The corresponding book reading is
[Chapter 8: A residual-based a posteriori estimate](https://ceadpx.github.io/finite-element-methods/chapters/08-aposteriori-adaptivity.html#sec-c8-estimator)
and
[Marking elements and refining the mesh](https://ceadpx.github.io/finite-element-methods/chapters/08-aposteriori-adaptivity.html#sec-c8-marking).
Efficiency and data oscillation are summarized under
[Additional considerations](https://ceadpx.github.io/finite-element-methods/chapters/08-aposteriori-adaptivity.html#sec-c8-extensions).
Marking and the adaptive loop are covered in Part 3 and the corresponding
sections of Chapter 8. Arnold's lecture notes, Chapter 4, Section 9.4, printed p. 73
(PDF p. 77), provide the supporting marking/refinement discussion.

## Scope

The module proves reliability under the stated local approximation hypothesis
and gives an explicit 1D bound. Local efficiency is explained as a property,
not claimed as a proved theorem for the general mixed-boundary problem.
The general efficiency proof, convergence/optimality of the adaptive algorithm,
elasticity estimators, and goal-oriented estimation are not developed here.
The companion notebook implements adaptive refinement for the two scalar
diffusion examples above.

## Build

Use the commands in the [lecture-slide README](../README.md#aposteriori-error).
Run them from this directory. Intermediate files belong in the ignored
`build/` directory; the final PDFs remain beside their sources.
