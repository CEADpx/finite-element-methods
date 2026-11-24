"""Reproduce the heated-bar results in the first transient lecture."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import numpy as np

FIGURES = Path(__file__).resolve().parent
HOT, COLD, AMPLITUDE = 400.0, 300.0, 20.0
plt.rcParams.update(
    {"font.size": 14, "axes.labelsize": 16, "legend.fontsize": 13,
     "lines.linewidth": 2, "savefig.bbox": "tight", "mathtext.fontset": "cm"}
)


def steady_temperature(x):
    return HOT + (COLD - HOT)*x


def exact_temperature(x, time):
    return steady_temperature(x) + AMPLITUDE*np.exp(-np.pi**2*time)*np.sin(np.pi*x)


def solve_bar(num_elements, dt, final_time, theta=0.5):
    """Solve T_t - T_xx = 0 with fixed hot and cold end temperatures."""
    nodes = np.linspace(0, 1, num_elements + 1)
    h = 1 / num_elements
    mass = np.zeros((num_elements + 1, num_elements + 1))
    stiffness = np.zeros_like(mass)
    for e in range(num_elements):
        mass[e:e+2, e:e+2] += h/6 * np.array([[2, 1], [1, 2]])
        stiffness[e:e+2, e:e+2] += 1/h * np.array([[1, -1], [-1, 1]])

    temperature = exact_temperature(nodes, 0)
    temperature[0], temperature[-1] = HOT, COLD
    left = mass + theta*dt*stiffness
    right = mass - (1-theta)*dt*stiffness
    num_steps = round(final_time / dt)
    if not np.isclose(num_steps*dt, final_time):
        raise ValueError("The final time must be an integer number of steps.")
    for n in range(num_steps):
        old_temperature = temperature.copy()
        rhs = right @ old_temperature
        # Move the prescribed endpoint-column terms to the right-hand side.
        interior_rhs = rhs[1:-1] - left[1:-1, 0]*HOT - left[1:-1, -1]*COLD
        temperature[1:-1] = np.linalg.solve(left[1:-1, 1:-1], interior_rhs)
        residual = -mass @ ((temperature-old_temperature)/dt)
        residual -= stiffness @ (theta*temperature + (1-theta)*old_temperature)
        assert np.max(np.abs(residual[1:-1])) < 1e-7
    assert temperature[0] == HOT and temperature[-1] == COLD
    return nodes, temperature


def temperature_error(nodes, temperature, final_time):
    xi, weights = np.polynomial.legendre.leggauss(8)
    error_squared = 0.0
    for e in range(len(nodes)-1):
        h = nodes[e+1] - nodes[e]
        x = nodes[e] + h*(xi+1)/2
        numerical = (1-xi)/2*temperature[e] + (1+xi)/2*temperature[e+1]
        error_squared += h/2 * np.sum(weights*(numerical-exact_temperature(x, final_time))**2)
    return np.sqrt(error_squared)


def make_figures():
    x = np.linspace(0, 1, 501)
    fig, ax = plt.subplots(figsize=(9.5, 3.4), layout="constrained")
    for time in (0, 0.025, 0.05, 0.1):
        ax.plot(x, exact_temperature(x, time), label=rf"$t={time:g}$")
    ax.plot(x, steady_temperature(x), "k--", linewidth=1.5, label=r"Steady $T_s$")
    ax.set(xlabel=r"$x$", ylabel=r"Temperature $T$ (K)", xlim=(0, 1), ylim=(295, 405))
    ax.grid(alpha=0.2)
    fig.legend(*ax.get_legend_handles_labels(), loc="outside upper center", ncols=5)
    fig.savefig(FIGURES / "exact_bar.pdf")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.5), layout="constrained")
    for ax, final_time in zip(axes, (0.04, 0.1)):
        ax.plot(x, exact_temperature(x, final_time), color="black", label="Exact")
        for num_elements, dt, style in ((4, 0.02, "o--"), (8, 0.01, "s--")):
            nodes, temperature = solve_bar(num_elements, dt, final_time)
            ax.plot(nodes, temperature, style, markersize=5,
                    label=rf"FE: $h=1/{num_elements}$, $\Delta t={dt:g}$")
        ax.set(xlabel=r"$x$", ylabel=r"Temperature $T$ (K)",
               title=rf"$t={final_time:g}$", xlim=(0, 1), ylim=(295, 405))
        ax.grid(alpha=0.2)
    fig.legend(*axes[0].get_legend_handles_labels(),
               loc="outside upper center", ncols=3)
    fig.savefig(FIGURES / "bar_temperatures.pdf")
    plt.close(fig)

    final_time = 0.1
    mesh_sizes, space_errors = [], []
    for num_elements in (4, 8, 16, 32):
        nodes, temperature = solve_bar(num_elements, 0.00025, final_time)
        mesh_sizes.append(1 / num_elements)
        space_errors.append(temperature_error(nodes, temperature, final_time))
    time_steps = np.array([0.05, 0.025, 0.0125, 0.00625])
    time_errors = []
    for dt in time_steps:
        nodes, temperature = solve_bar(256, dt, final_time)
        time_errors.append(temperature_error(nodes, temperature, final_time))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.3), layout="constrained")
    axes[0].loglog(mesh_sizes, space_errors, "o-")
    axes[0].set(title=r"Mesh refinement: $\Delta t=0.00025$",
                xlabel=r"Mesh size $h$", ylabel=r"$L^2$ error at $t=0.1$")
    axes[0].set_xticks(mesh_sizes, labels=["1/4", "1/8", "1/16", "1/32"])
    axes[1].loglog(time_steps, time_errors, "s-")
    axes[1].set(title=r"Time-step refinement: $h=1/256$",
                xlabel=r"Time step $\Delta t$", ylabel=r"$L^2$ error at $t=0.1$")
    axes[1].set_xticks(time_steps, labels=[f"{dt:g}" for dt in time_steps])
    for ax in axes:
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(which="both", alpha=0.2)
    fig.savefig(FIGURES / "bar_errors.pdf")
    plt.close(fig)

    nodes, first_step = solve_bar(4, 0.02, 0.02)
    h = 1/4
    eigenvalue = 6/h**2 * (1-np.cos(np.pi*h))/(2+np.cos(np.pi*h))
    factor = (1-0.01*eigenvalue)/(1+0.01*eigenvalue)
    expected = steady_temperature(nodes) + AMPLITUDE*factor*np.sin(np.pi*nodes)
    assert np.allclose(first_step, expected, atol=1e-10, rtol=0)
    print("Initial coefficients:", exact_temperature(nodes, 0))
    print("First CN step:", first_step)
    print("Space errors:", space_errors)
    print("Time errors:", time_errors)


if __name__ == "__main__":
    make_figures()
