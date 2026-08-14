# Conda environment

The `finite-elements` environment contains Quarto, Python, Jupyter, FEniCSx,
and the supporting scientific-computing and visualization packages used by the
book and course materials.

The specification includes `python-gmsh` in addition to `gmsh` because the
former supplies the Python module required by the repository's import test.

## Create the environment

```bash
conda env create -f environment/environment.yml
```

## Activate it

```bash
conda activate finite-elements
```

## Update it

```bash
conda env update -f environment/environment.yml --prune
```

## Install TinyTeX

Install TinyTeX through the Quarto executable contained in this environment:

```bash
quarto install tinytex
```

## Register the Jupyter kernel

```bash
python -m ipykernel install \
    --user \
    --name finite-elements \
    --display-name "Python (Finite Elements)"
```

## Verify the environment

```bash
which python
which quarto
python --version
quarto --version

python -c "import dolfinx; print('DOLFINx:', dolfinx.__version__)"
python -c "from petsc4py import PETSc; print('PETSc:', PETSc.Sys.getVersion())"
python -c "from mpi4py import MPI; print('MPI:', MPI.Get_library_version())"
python -c "import pyvista; print('PyVista:', pyvista.__version__)"
python -c "import gmsh; print('Gmsh imported successfully')"

quarto check
quarto check jupyter
quarto check latex
```

Verify MPI with two processes:

```bash
mpirun -n 2 python -c \
"from mpi4py import MPI; print('rank', MPI.COMM_WORLD.rank, 'of', MPI.COMM_WORLD.size)"
```

Run the environment smoke test from the repository root:

```bash
pytest tests/test_environment.py
```
