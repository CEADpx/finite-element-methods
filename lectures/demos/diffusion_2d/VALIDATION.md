# Classroom-demo validation

Validated locally in the existing finite-elements conda environment with
DOLFINx 0.11.0 and Python 3.12.13. A fresh kernel executed all 10 code cells
successfully. The supplied environment.yml is a reproducibility recipe;
creation of a separate clean environment was not tested.

The variable-coefficient manufactured problem uses k=1+x and u=sin(pi*x)sin(pi*y), with a derived source and homogeneous boundary data. On 8, 16 and 32 subdivisions, L2 errors were 0.0210398703, 0.0053535062 and 0.0013444175; energy errors were 0.52878047, 0.266418085 and 0.133466017. Final rates were 1.9935 and 0.9972, as expected for P1 approximation. Solver, boundary and discrete balance assertions passed; balance residuals were below 6e-15. See verification.json and verify_demo.py.

The exercise doubling conductivity while holding the source fixed was independently executed and agreed with half the baseline discrete solution to floating-point precision (reported maximum difference zero). See doubling-verification.json. The executed notebook and exported solution were then restored to the original conductivity.

ParaView 6.1 pvpython read the XDMF/HDF5 export using Xdmf3ReaderS and rendered the scalar field with mesh edges; results/paraview.png was visually inspected. The default reader did not expose the field, which is why the instructions specify the reader explicitly. GUI clicks were not separately automated.

Warm the notebook kernel and complete its first run before class to avoid live
compilation delays. No timing guarantee is claimed.
