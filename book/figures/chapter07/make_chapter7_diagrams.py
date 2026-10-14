"""Generate the interpolation diagrams used in Chapter 7."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from matplotlib.patches import Circle, Polygon

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


def make_shape_regularity_figure(filename):
    """Compare cells with the same diameter but different shape parameters."""
    figure, axes = plt.subplots(1, 2, figsize=(10.8, 3.45), constrained_layout=True)

    triangle_data = (
        {
            "vertices": np.array(((-1.0, 0.0), (1.0, 0.0), (0.0, np.sqrt(3.0)))),
            "center": (0.0, 1.0 / np.sqrt(3.0)),
            "radius": 1.0 / np.sqrt(3.0),
            "facecolor": "#dbeaf3",
            "edgecolor": "#2f628d",
            "title": "Well-shaped triangle",
        },
        {
            "vertices": np.array(((-1.0, 0.0), (1.0, 0.0), (0.0, 0.25))),
            "center": (0.0, 0.25 / (1.0 + np.sqrt(1.0 + 0.25**2))),
            "radius": 0.25 / (1.0 + np.sqrt(1.0 + 0.25**2)),
            "facecolor": "#f4e3d1",
            "edgecolor": "#9a5a22",
            "title": "Flat triangle",
        },
    )

    for axis, data in zip(axes, triangle_data):
        vertices = data["vertices"]
        radius = data["radius"]
        axis.add_patch(
            Polygon(
                vertices,
                closed=True,
                facecolor=data["facecolor"],
                edgecolor=data["edgecolor"],
                linewidth=2.0,
            )
        )
        axis.add_patch(
            Circle(
                data["center"],
                radius,
                facecolor="none",
                edgecolor=data["edgecolor"],
                linewidth=1.8,
            )
        )
        axis.annotate(
            "",
            xy=(-1.0, -0.12),
            xytext=(1.0, -0.12),
            arrowprops={"arrowstyle": "<->", "color": "#253746", "lw": 1.2},
        )
        axis.text(0.0, -0.22, r"$h_e=2$", ha="center", va="top", fontsize=12)
        axis.plot(
            (data["center"][0] - radius, data["center"][0] + radius),
            (data["center"][1], data["center"][1]),
            color=data["edgecolor"],
            linewidth=1.25,
        )
        if data["title"] == "Flat triangle":
            label_position = (
                data["center"][0] + radius + 0.10,
                data["center"][1],
            )
            horizontal_alignment = "left"
            vertical_alignment = "center"
        else:
            label_position = (
                data["center"][0],
                data["center"][1] + 0.08,
            )
            horizontal_alignment = "center"
            vertical_alignment = "bottom"
        axis.text(
            *label_position,
            r"$\rho_e$",
            ha=horizontal_alignment,
            va=vertical_alignment,
            fontsize=12,
            color=data["edgecolor"],
        )
        axis.set_title(data["title"], fontsize=14, pad=6)
        axis.set_xlim(-1.18, 1.18)
        axis.set_ylim(-0.34, 1.88)
        axis.set_aspect("equal")
        axis.axis("off")

    figure.savefig(OUTPUT_DIR / filename, bbox_inches="tight")
    plt.close(figure)


def make_best_approximation_figure(filename):
    """Show the energy projection with separated labels and a clear right angle."""
    figure, axis = plt.subplots(figsize=(9.6, 4.8))
    axis.set_xlim(0.25, 6.15)
    axis.set_ylim(0.20, 3.35)
    axis.axis("off")

    line_start = np.array((0.65, 0.62))
    line_end = np.array((5.65, 1.72))
    tangent = line_end - line_start
    tangent = tangent / np.linalg.norm(tangent)
    normal = np.array((-tangent[1], tangent[0]))

    u_h = np.array((3.62, 1.2734))
    u = u_h + 1.58 * normal
    v_h = np.array((1.72, 0.8554))

    axis.plot(
        (line_start[0], line_end[0]),
        (line_start[1], line_end[1]),
        color="#2f638f",
        linewidth=4.2,
        solid_capstyle="round",
    )
    axis.text(5.63, 1.88, r"$V_h$", fontsize=24, color="#2f638f", ha="right", va="bottom")

    axis.plot((u[0], u_h[0]), (u[1], u_h[1]), color="#c65b2a", linewidth=2.8, linestyle=(0, (6, 5)))
    axis.plot((u[0], v_h[0]), (u[1], v_h[1]), color="#3b9665", linewidth=2.8, linestyle=(0, (6, 5)))

    axis.scatter((u[0],), (u[1],), s=115, color="#c65b2a", zorder=5)
    axis.scatter((u_h[0],), (u_h[1],), s=115, color="#2f638f", zorder=5)
    axis.scatter((v_h[0],), (v_h[1],), s=115, color="#3b9665", zorder=5)

    axis.text(u[0] + 0.12, u[1] + 0.08, r"$u$", fontsize=24, color="#733417", ha="left", va="bottom")
    axis.text(u_h[0] + 0.13, u_h[1] - 0.13, r"$u_h$", fontsize=23, color="#244a6b", ha="left", va="top")
    axis.text(v_h[0] - 0.10, v_h[1] - 0.14, r"$v_h$", fontsize=23, color="#286746", ha="right", va="top")

    marker_size = 0.20
    corner_1 = u_h - marker_size * tangent
    corner_2 = corner_1 + marker_size * normal
    corner_3 = u_h + marker_size * normal
    axis.plot(
        (corner_1[0], corner_2[0], corner_3[0]),
        (corner_1[1], corner_2[1], corner_3[1]),
        color="#303840",
        linewidth=3.0,
        solid_capstyle="round",
        zorder=6,
    )

    orange_midpoint = 0.54 * u + 0.46 * u_h
    green_midpoint = 0.53 * u + 0.47 * v_h
    axis.text(
        orange_midpoint[0] + 0.28,
        orange_midpoint[1] + 0.02,
        r"$\Vert u-u_h\Vert_a$",
        fontsize=20,
        color="#733417",
        ha="left",
        va="center",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5, "alpha": 0.92},
    )
    axis.text(
        green_midpoint[0] - 0.18,
        green_midpoint[1] + 0.14,
        r"$\Vert u-v_h\Vert_a$",
        fontsize=20,
        color="#286746",
        ha="right",
        va="center",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5, "alpha": 0.92},
    )

    figure.savefig(OUTPUT_DIR / filename, bbox_inches="tight", facecolor="white")
    plt.close(figure)


if __name__ == "__main__":
    make_two_dimensional_figure(3, "interpolation-2d.png")
    make_two_dimensional_figure(6, "interpolation-2d-fine.png")
    make_one_dimensional_figure(4, "interpolation-1d.svg")
    make_one_dimensional_figure(8, "interpolation-1d-fine.svg")
    make_shape_regularity_figure("shape-regularity-comparison.svg")
    make_best_approximation_figure("best-approximation-geometry.svg")
