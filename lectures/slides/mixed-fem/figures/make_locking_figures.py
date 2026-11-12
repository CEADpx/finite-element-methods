"""Compute the manufactured plane-strain locking example for Lecture 1.

Run in the finite-elements environment. The load and exact displacement are
independent of the bulk modulus. No mixed solver is used in this first lecture.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ufl
from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc

HERE = Path(__file__).resolve().parent
MU = 1.0
AMPLITUDE = 1e-3


def solve(n, nu):
    domain = mesh.create_unit_square(MPI.COMM_SELF, n, n)
    V = fem.functionspace(domain, ("Lagrange", 1, (2,)))
    x = ufl.SpatialCoordinate(domain)
    exact = AMPLITUDE * ufl.as_vector((
        ufl.sin(np.pi*x[0])**2 * ufl.sin(2*np.pi*x[1]),
        -ufl.sin(2*np.pi*x[0]) * ufl.sin(np.pi*x[1])**2))
    # div(exact)=0, so -div(sigma(exact))=-mu*Delta(exact), independent of nu.
    force = -MU * ufl.div(ufl.grad(exact))
    lame_lambda = 2*MU*nu/(1-2*nu)
    kappa = lame_lambda + 2*MU/3
    trial = ufl.TrialFunction(V)
    test = ufl.TestFunction(V)
    dx = ufl.Measure("dx", domain=domain, metadata={"quadrature_degree": 10})
    a = (2*MU*ufl.inner(ufl.sym(ufl.grad(trial)), ufl.sym(ufl.grad(test)))
         + lame_lambda*ufl.div(trial)*ufl.div(test)) * dx
    L = ufl.dot(force, test)*dx
    boundary = mesh.locate_entities_boundary(
        domain, 1, lambda X: np.ones(X.shape[1], dtype=bool))
    dofs = fem.locate_dofs_topological(V, 1, boundary)
    bc = fem.dirichletbc(np.zeros(2, dtype=PETSc.ScalarType), dofs, V)
    problem = LinearProblem(a, L, bcs=[bc], petsc_options_prefix="locking_",
                            petsc_options={"ksp_type": "preonly", "pc_type": "lu"})
    solution = problem.solve()
    error_squared = fem.assemble_scalar(fem.form(ufl.inner(solution-exact, solution-exact)*dx)).real
    norm_squared = fem.assemble_scalar(fem.form(ufl.inner(exact, exact)*dx)).real
    coordinates = V.tabulate_dof_coordinates()
    probe = np.flatnonzero(np.isclose(coordinates[:, 0], .5)
                          & np.isclose(coordinates[:, 1], .25))
    assert V.dofmap.index_map_bs == 2 and len(probe) == 1
    response = solution.x.array.reshape(-1, 2)[probe[0], 0].real / AMPLITUDE
    # Check the prescribed boundary values and the analytic divergence identity.
    assert np.max(np.abs(solution.x.array.reshape(-1, 2)[dofs])) < 1e-12
    exact_div_squared = fem.assemble_scalar(fem.form(ufl.div(exact)**2*dx)).real
    assert exact_div_squared < 1e-20
    return dict(n=n, nu=nu, h=np.sqrt(2)/n, kappa_over_mu=kappa/MU,
                response=response, relative_L2=np.sqrt(error_squared/norm_squared))


def main():
    rows = []
    for n in [8, 16, 32]:
        for nu in [.3, .49, .499, .4999, .49999]:
            result = solve(n, nu)
            rows.append(result)
            print(result, flush=True)
    data = pd.DataFrame(rows)
    data.to_csv(HERE / "locking_results.csv", index=False)
    assert data.query('nu == 0.49999')['response'].max() < .2
    assert data.query('n == 32 and nu == 0.3')['relative_L2'].iloc[0] < .03
    plt.rcParams.update({"font.size": 15, "axes.titlesize": 16,
                         "mathtext.fontset": "cm", "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(8.6, 4.2), layout="constrained")
    for n, marker in [(8, 'o'), (16, 's'), (32, '^')]:
        part = data[data.n == n]
        ax.semilogx(part.kappa_over_mu, part.response, marker+'-', label=rf"$n={n}$")
    ax.axhline(1, color='0.2', linestyle='--', label="Exact response")
    ax.set(xlabel=r"bulk-to-shear modulus ratio $\kappa/\mu$",
           ylabel=r"$u_{h,1}(1/2,1/4)/a_0$", ylim=(0, 1.09))
    ax.grid(True, which='both', alpha=.2)
    ax.legend(loc='center left', bbox_to_anchor=(1.01, .5), fontsize=13)
    fig.savefig(HERE/'locking_response.pdf', bbox_inches='tight')
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8.6, 4.2), layout="constrained")
    for nu, marker in [(.3, 'o'), (.49, 's'), (.4999, '^')]:
        part = data[data.nu == nu]
        ax.loglog(part.h, part.relative_L2, marker+'-', label=rf"$\nu={nu}$")
    ax.set(xlabel=r"mesh size $h$", ylabel=r"$\|\boldsymbol{u}-\boldsymbol{u}_h\|_{L^2}/\|\boldsymbol{u}\|_{L^2}$")
    ax.grid(True, which='both', alpha=.2)
    ax.legend(loc='center left', bbox_to_anchor=(1.01, .5), fontsize=13)
    fig.savefig(HERE/'locking_mesh_error.pdf', bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    main()
