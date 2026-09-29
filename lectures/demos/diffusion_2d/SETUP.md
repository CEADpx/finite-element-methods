# Running the first FEniCSx demo

## Existing classroom environment on this computer

The installed `finite-elements` environment provides DOLFINx 0.11.0. From this demo directory:

```bash
conda activate finite-elements
python -c "import dolfinx; print(dolfinx.__version__)"
python -m jupyterlab diffusion_2d.ipynb
```

Choose the kernel belonging to that environment, then Restart Kernel and Run All. If it is not listed, register it once:

```bash
python -m ipykernel install --user --name finite-elements --display-name "Python (finite-elements)"
```

Check `import sys; print(sys.executable)` in a temporary cell if the kernel is uncertain. It should point inside the chosen conda environment. Run the notebook as a single Jupyter process, not with mpiexec.

## New student environment

With conda available, from the directory containing environment.yml:

```bash
conda env create -f environment.yml
conda activate fem-diffusion-demo
python -m ipykernel install --user --name fem-diffusion-demo --display-name "Python (fem-diffusion-demo)"
python -m jupyterlab diffusion_2d.ipynb
```

Select Python (fem-diffusion-demo). This recipe pins DOLFINx to the tested API generation but is not a platform-independent lockfile. A fresh installation on every student's OS has not been tested. Do not mix pip-installed legacy FEniCS with this environment or upgrade DOLFINx immediately before class. Windows users need a supported Linux/WSL environment for these conda packages; this run validates macOS only.

The official installation route is documented by the [FEniCS Project](https://fenicsproject.org/download/). Do installations before class. The first solve may take longer because the forms are compiled. A saved executed notebook and solution image provide a classroom fallback; they must be identified as saved results, not a live solve.

## Files

- diffusion_2d.ipynb: the complete teaching sequence.
- CHAPTER6_LECTURE_PLAN.md: one-lecture timing and reading boundaries.
- PARAVIEW.md: visualizing the notebook's result.
- verify_demo.py: instructor checks using the same notebook cells.
- results/: generated XDMF/HDF5 pair and solution image.
- verification.json: measured convergence and checks from the executed test.
