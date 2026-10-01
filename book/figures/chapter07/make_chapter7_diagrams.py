"""Generate the interpolation diagrams used in Chapter 7."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parent


def target_function(x, y=None):
    """Positive concave quadratic used in the interpolation diagrams."""
    if y is None:
        return 1.0 + x * (1.0 - x)
    return 1.0 + x * (1.0 - x) + y * (1.0 - y)


def structured_triangular_mesh(cells_per_side=3):
    """Return a structured triangular mesh of the unit square."""
    coordinates = np.linspace(0.0, 1.0, cells_per_side + 1)
    x_nodes, y_nodes = np.meshgrid(coordinates, coordinates, indexing="xy")
    x_nodes = x_nodes.ravel()
    y_nodes = y_nodes.ravel()

    triangles = []
    nodes_per_row = cells_per_side + 1
    for j in range(cells_per_side):
        for i in range(cells_per_side):
            lower_left = j * nodes_per_row + i
            lower_right = lower_left + 1
            upper_left = lower_left + nodes_per_row
            upper_right = upper_left + 1
            triangles.append((lower_left, lower_right, upper_right))
            triangles.append((lower_left, upper_right, upper_left))

    return x_nodes, y_nodes, np.asarray(triangles)


def make_two_dimensional_figure(cells_per_side, filename):
    """Plot the mesh, a P1 interpolant, the exact function, and their error."""
    x_nodes, y_nodes, triangles = structured_triangular_mesh(cells_per_side)
    triangulation = mtri.Triangulation(x_nodes, y_nodes, triangles)
    nodal_values = target_function(x_nodes, y_nodes)

    plotting_coordinates = np.linspace(0.0, 1.0, 121)
    x_plot, y_plot = np.meshgrid(
        plotting_coordinates, plotting_coordinates, indexing="xy"
    )
    exact = target_function(x_plot, y_plot)
    interpolator = mtri.LinearTriInterpolator(triangulation, nodal_values)
    interpolated = np.ma.asarray(interpolator(x_plot, y_plot)).filled(np.nan)
    error = exact - interpolated

    figure = plt.figure(figsize=(15.4, 4.35), constrained_layout=True)
    grid = figure.add_gridspec(2, 4, width_ratios=(0.72, 1.0, 1.0, 1.0))
    domain_axis = figure.add_subplot(grid[0, 0])
    mesh_axis = figure.add_subplot(grid[1, 0])
    axes = [
        figure.add_subplot(grid[:, index], projection="3d")
        for index in range(1, 4)
    ]
    value_limits = (float(np.nanmin(interpolated)), float(np.nanmax(exact)))

    domain_axis.fill(
        (0.0, 1.0, 1.0, 0.0),
        (0.0, 0.0, 1.0, 1.0),
        facecolor="#dbeaf3",
        edgecolor="#264f70",
        linewidth=1.5,
    )
    domain_axis.text(0.5, 0.5, r"$\Omega$", ha="center", va="center", fontsize=15)
    domain_axis.set_title("Domain", pad=5)

    mesh_axis.triplot(
        triangulation,
        color="#264f70",
        linewidth=1.0 if cells_per_side == 3 else 0.65,
    )
    number_of_triangles = len(triangles)
    mesh_axis.set_title(
        rf"Mesh $\mathcal{{T}}_h$ ({number_of_triangles} triangles)",
        pad=5,
    )

    for axis in (domain_axis, mesh_axis):
        axis.set_aspect("equal")
        axis.set_xlim(-0.03, 1.03)
        axis.set_ylim(-0.03, 1.03)
        axis.set_xlabel(r"$x_1$", labelpad=0)
        axis.set_ylabel(r"$x_2$", labelpad=0)
        axis.set_xticks((0.0, 1.0))
        axis.set_yticks((0.0, 1.0))
        axis.tick_params(labelsize=8, pad=1)

    axes[0].plot_trisurf(
        triangulation,
        nodal_values,
        cmap="viridis",
        vmin=value_limits[0],
        vmax=value_limits[1],
        edgecolor="#253746",
        linewidth=0.65 if cells_per_side == 3 else 0.35,
        antialiased=True,
    )
    axes[0].set_title(r"Interpolant $\mathcal{I}_h u$", pad=9)

    axes[1].plot_surface(
        x_plot,
        y_plot,
        exact,
        cmap="viridis",
        vmin=value_limits[0],
        vmax=value_limits[1],
        linewidth=0,
        antialiased=True,
    )
    axes[1].set_title(r"Exact function $u$", pad=9)

    axes[2].plot_surface(
        x_plot,
        y_plot,
        error,
        cmap="magma",
        linewidth=0,
        antialiased=True,
    )
    axes[2].set_title(r"Error $u-\mathcal{I}_h u$", pad=9)

    for index, axis in enumerate(axes):
        axis.set_xlabel(r"$x_1$", labelpad=2)
        axis.set_ylabel(r"$x_2$", labelpad=2)
        axis.set_zlabel("value" if index < 2 else "error", labelpad=3)
        axis.set_xlim(0.0, 1.0)
        axis.set_ylim(0.0, 1.0)
        axis.set_xticks((0.0, 0.5, 1.0))
        axis.set_yticks((0.0, 0.5, 1.0))
        axis.tick_params(labelsize=8, pad=0)
        axis.view_init(elev=25, azim=-125)
        axis.set_box_aspect((1.0, 1.0, 0.65))

    axes[0].set_zlim(*value_limits)
    axes[1].set_zlim(*value_limits)
    axes[2].set_zlim(0.0, 0.06)

    figure.savefig(OUTPUT_DIR / filename, dpi=240)
    plt.close(figure)


def make_one_dimensional_figure(number_of_elements, filename):
    """Plot linear interpolation and its error on a uniform partition."""
    nodes = np.linspace(0.0, 1.0, number_of_elements + 1)
    nodal_values = target_function(nodes)
    x_plot = np.linspace(0.0, 1.0, 501)
    exact = target_function(x_plot)
    interpolated = np.interp(x_plot, nodes, nodal_values)
    error = exact - interpolated

    figure, axes = plt.subplots(1, 3, figsize=(11.2, 3.05), constrained_layout=True)

    axes[0].plot(x_plot, interpolated, color="#2463a0", linewidth=2.2)
    axes[0].plot(
        nodes,
        nodal_values,
        linestyle="none",
        marker="o",
        color="#172a3a",
        markersize=5,
        zorder=3,
    )
    axes[0].set_title(r"(a) Interpolant $\mathcal{I}_h u$")

    axes[1].plot(x_plot, exact, color="#9a4d16", linewidth=2.2)
    axes[1].set_title(r"(b) Exact function $u$")

    axes[2].plot(x_plot, error, color="#8c2d64", linewidth=2.2)
    axes[2].fill_between(x_plot, 0.0, error, color="#8c2d64", alpha=0.18)
    axes[2].axhline(0.0, color="#4f5964", linewidth=0.8)
    axes[2].set_title(r"(c) Error $u-\mathcal{I}_h u$")

    value_limits = (0.98, 1.28)
    for index, axis in enumerate(axes):
        axis.set_xlabel(r"$x$")
        axis.set_ylabel("value" if index < 2 else "error")
        axis.set_xlim(0.0, 1.0)
        axis.set_xticks(np.linspace(0.0, 1.0, 5))
        axis.grid(color="#d6dce1", linewidth=0.6, alpha=0.8)
        if index < 2:
            axis.set_ylim(*value_limits)
        else:
            axis.set_ylim(-0.0005, 0.0165)

    figure.savefig(OUTPUT_DIR / filename)
    plt.close(figure)


if __name__ == "__main__":
    make_two_dimensional_figure(3, "interpolation-2d.png")
    make_two_dimensional_figure(6, "interpolation-2d-fine.png")
    make_one_dimensional_figure(4, "interpolation-1d.svg")
    make_one_dimensional_figure(8, "interpolation-1d-fine.svg")
