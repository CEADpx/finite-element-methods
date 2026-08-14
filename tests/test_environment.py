"""Smoke tests for the repository's Conda environment."""

import dolfinx
import gmsh
import matplotlib
import meshio
import mpi4py
import numpy
import pandas
import petsc4py
import pyvista
import scipy
import sympy
from mpi4py import MPI
from petsc4py import PETSc


def test_required_packages_import() -> None:
    """Verify that the required packages can be imported."""
    assert all(
        module is not None
        for module in (
            dolfinx,
            mpi4py,
            petsc4py,
            numpy,
            scipy,
            sympy,
            matplotlib,
            pyvista,
            gmsh,
            meshio,
            pandas,
        )
    )
    assert PETSc.Sys.getVersion()


def test_mpi_communicator_is_available() -> None:
    """Verify that MPI has initialized a nonempty world communicator."""
    assert MPI.COMM_WORLD.size >= 1
