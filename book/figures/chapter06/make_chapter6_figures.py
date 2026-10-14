"""Generate selected Chapter 6 diagrams with collision-free labels."""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

OUTPUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 15,
        "mathtext.fontset": "stix",
    }
)

BLUE = "#27577f"
LIGHT_BLUE = "#d8e9f3"
ORANGE = "#d97728"
GREEN = "#2ca25f"
DARK = "#202a35"
LABEL_BOX = {"facecolor": "white", "edgecolor": "none", "pad": 1.6, "alpha": 0.72}


def save(figure, filename):
    figure.savefig(OUTPUT_DIR / filename, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def make_p1_basis_functions():
    """Plot the three basis surfaces from a viewpoint that reveals every plane."""
    x = np.array((0.0, 2.0, 0.0))
    y = np.array((0.0, 0.0, 1.0))
    triangulation = mtri.Triangulation(x, y, ((0, 1, 2),))
    values = np.eye(3)
    figure = plt.figure(figsize=(12.0, 4.15), constrained_layout=True)
    axes = [figure.add_subplot(1, 3, index + 1, projection="3d") for index in range(3)]
    colors = ("#2f7fb8", "#e67e22", "#2ca25f")
    for index, axis in enumerate(axes):
        axis.plot_trisurf(
            triangulation,
            values[index],
            color=colors[index],
            edgecolor=BLUE,
            linewidth=1.6,
            alpha=0.92,
            shade=False,
        )
        axis.plot_trisurf(
            triangulation,
            np.zeros(3),
            color="#eef2f5",
            edgecolor="#77818b",
            linewidth=1.2,
            alpha=0.35,
            shade=False,
        )
        axis.set_title(rf"$\phi_{index + 1}$", fontsize=24, pad=2)
        axis.set_xlabel(r"$x$", fontsize=16, labelpad=1)
        axis.set_ylabel(r"$y$", fontsize=16, labelpad=1)
        axis.set_xlim(0.0, 2.0)
        axis.set_ylim(0.0, 1.0)
        axis.set_zlim(0.0, 1.0)
        axis.set_xticks((0.0, 1.0, 2.0))
        axis.set_yticks((0.0, 1.0))
        axis.set_zticks((0.0, 1.0))
        axis.tick_params(labelsize=11, pad=0)
        axis.set_box_aspect((2.0, 1.0, 1.05))
        axis.view_init(elev=27, azim=-125)
    save(figure, "p1_basis_functions.svg")


def make_triangular_mesh_concepts():
    """Label mesh entities without placing text on top of edges or vertices."""
    figure, axis = plt.subplots(figsize=(12.0, 4.8))
    axis.set_xlim(-0.22, 6.15)
    axis.set_ylim(-0.25, 2.62)
    axis.set_aspect("equal")
    axis.axis("off")

    for x_coordinate in range(4):
        axis.plot((x_coordinate, x_coordinate), (0, 2), color=BLUE, lw=2.2)
    for y_coordinate in range(3):
        axis.plot((0, 3), (y_coordinate, y_coordinate), color=BLUE, lw=2.2)
    for x_coordinate in range(3):
        axis.plot((x_coordinate, x_coordinate + 1), (0, 1), color=BLUE, lw=1.8)
        axis.plot((x_coordinate, x_coordinate + 1), (1, 2), color=BLUE, lw=1.8)

    axis.add_patch(Polygon(((0, 0), (1, 0), (1, 1)), closed=True, facecolor=LIGHT_BLUE, edgecolor="none"))
    axis.plot((0, 1), (2, 2), color=ORANGE, lw=6, solid_capstyle="round")
    axis.plot((1, 1), (0, 1), color=GREEN, lw=6, solid_capstyle="round")

    grid_x, grid_y = np.meshgrid(np.arange(4), np.arange(3))
    axis.scatter(grid_x.ravel(), grid_y.ravel(), s=85, color="#5796c5", zorder=4)

    axis.annotate(
        "boundary facet",
        xy=(0.5, 2.0),
        xytext=(0.5, 2.38),
        ha="center",
        fontsize=18,
        color=ORANGE,
        arrowprops={"arrowstyle": "-", "color": ORANGE, "lw": 1.8},
    )
    axis.annotate(
        "vertex",
        xy=(2.0, 1.0),
        xytext=(2.38, 1.34),
        ha="left",
        fontsize=18,
        color="#4d5965",
        bbox=LABEL_BOX,
        arrowprops={"arrowstyle": "->", "color": "#4d5965", "lw": 1.6},
    )
    axis.annotate(
        "shared facet",
        xy=(1.0, 0.40),
        xytext=(1.0, -0.15),
        va="top",
        ha="center",
        fontsize=18,
        color=GREEN,
        arrowprops={"arrowstyle": "-", "color": GREEN, "lw": 1.8},
    )
    axis.text(
        0.66,
        0.24,
        "element\n" + r"$\mathcal{K}_e$",
        fontsize=16,
        ha="center",
        va="center",
        linespacing=1.0,
        bbox=LABEL_BOX,
    )

    axis.text(3.55, 2.00, "element connectivity", fontsize=18, fontweight="bold", color=BLUE)
    axis.text(3.55, 1.68, r"$I^e=(i_1,i_2,i_3)$", fontsize=21)
    axis.text(
        3.55,
        1.20,
        "The three entries are the global\n" + r"vertices of element $\mathcal{K}_e$.",
        fontsize=17,
        linespacing=1.35,
    )
    axis.text(3.55, 0.71, "facet incidence", fontsize=18, fontweight="bold", color=BLUE)
    axis.text(
        3.55,
        0.18,
        "Shared facets belong to two elements;\nboundary facets belong to one.",
        fontsize=16,
        linespacing=1.35,
    )
    save(figure, "triangular_mesh_concepts.svg")


def make_shared_edge_continuity():
    """Separate the shared-edge callout from the element labels."""
    figure, axis = plt.subplots(figsize=(11.5, 4.3))
    axis.set_xlim(-0.12, 3.75)
    axis.set_ylim(-0.18, 1.32)
    axis.axis("off")

    left = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0))
    right = ((1.0, 0.0), (2.0, 0.0), (1.0, 1.0))
    axis.add_patch(Polygon(left, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2.8))
    axis.add_patch(Polygon(right, closed=True, facecolor="#f5dfbd", edgecolor=BLUE, linewidth=2.8))
    axis.plot((1.0, 1.0), (0.0, 1.0), color=GREEN, lw=6, solid_capstyle="round")
    axis.scatter((1.0, 1.0), (0.0, 1.0), s=115, color=BLUE, zorder=4)

    axis.text(0.58, 0.27, r"$\mathcal{K}^{-}$", fontsize=23, ha="center")
    axis.text(1.42, 0.27, r"$\mathcal{K}^{+}$", fontsize=23, ha="center")
    axis.text(1.0, -0.11, r"$U_i$", fontsize=18, ha="center", va="top")
    axis.text(1.0, 1.08, r"$U_j$", fontsize=18, ha="center", va="bottom")
    axis.text(
        1.09,
        0.55,
        "shared edge",
        fontsize=17,
        color=GREEN,
        ha="center",
        va="center",
        rotation=90,
        bbox=LABEL_BOX,
    )

    axis.text(
        2.35,
        0.95,
        "continuity across the shared edge",
        fontsize=18,
        fontweight="bold",
        color=BLUE,
        va="top",
    )
    axis.text(
        2.35,
        0.70,
        "Both restrictions are linear on the\nshared edge and use the same\nendpoint values.",
        fontsize=16,
        va="top",
        linespacing=1.35,
    )
    axis.text(2.35, 0.16, r"$u_h^-|_{\mathcal{F}}=u_h^+|_{\mathcal{F}}$", fontsize=22)
    save(figure, "shared_edge_continuity.svg")


def make_boundary_facet_load():
    """Display the boundary integral at a size comparable with the geometry labels."""
    figure, axis = plt.subplots(figsize=(11.5, 4.35))
    axis.set_xlim(-0.15, 3.9)
    axis.set_ylim(-0.18, 1.35)
    axis.axis("off")

    vertices = np.array(((0.0, 0.0), (1.45, 0.0), (0.34, 0.94)))
    axis.add_patch(Polygon(vertices, closed=True, facecolor="white", edgecolor=BLUE, linewidth=2.8))
    axis.plot((vertices[2, 0], vertices[1, 0]), (vertices[2, 1], vertices[1, 1]), color=ORANGE, lw=6)
    axis.scatter(vertices[:, 0], vertices[:, 1], s=115, color=BLUE, zorder=4)

    facet_start = vertices[2]
    facet_end = vertices[1]
    tangent = facet_end - facet_start
    normal = np.array((-tangent[1], tangent[0]))
    normal = normal / np.linalg.norm(normal)
    for fraction in (0.28, 0.52, 0.76):
        point = facet_start + fraction * tangent
        axis.add_patch(
            FancyArrowPatch(
                point,
                point + 0.22 * normal,
                arrowstyle="-|>",
                mutation_scale=16,
                color=ORANGE,
                lw=2.0,
            )
        )

    axis.text(-0.03, -0.08, r"$\mathbf{x}_1$", fontsize=18, ha="right", va="top")
    axis.text(1.50, -0.08, r"$\mathbf{x}_2$", fontsize=18, ha="left", va="top")
    axis.text(0.32, 1.05, r"$\mathbf{x}_3$", fontsize=18, ha="center", va="bottom")
    axis.text(0.95, 1.07, r"$q$", fontsize=22, color=ORANGE, ha="center")

    axis.text(1.82, 0.95, "prescribed normal flux", fontsize=20, color=ORANGE)
    axis.text(
        1.82,
        0.59,
        r"$F_a^{\mathcal{F}}=-\int_{\mathcal{F}}\;q\,\phi_a^e\,\mathrm{d}s$",
        fontsize=27,
        color=DARK,
    )
    axis.text(1.82, 0.18, "Only basis functions attached to the\nboundary facet contribute.", fontsize=17, linespacing=1.35)
    save(figure, "boundary_facet_load.svg")


def make_two_triangle_patch_test():
    """Connect the prescribed data, nodal values, and reproduced linear field."""
    figure, axis = plt.subplots(figsize=(11.8, 4.65))
    axis.set_xlim(-0.30, 4.60)
    axis.set_ylim(-0.28, 1.32)
    axis.axis("off")

    vertices = np.array(((0.0, 0.0), (1.45, 0.0), (0.0, 1.0), (1.45, 1.0)))
    axis.add_patch(
        Polygon(vertices[[0, 1, 2]], closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2.8)
    )
    axis.add_patch(
        Polygon(vertices[[1, 3, 2]], closed=True, facecolor="#f5e2c9", edgecolor=BLUE, linewidth=2.8)
    )

    axis.plot((0.0, 0.0), (0.0, 1.0), color="#c84a3a", lw=6.0, solid_capstyle="butt")
    axis.text(-0.18, 0.50, r"$u=0$", color="#c84a3a", fontsize=21, rotation=90, ha="center", va="center")
    for vertical_coordinate in (0.23, 0.50, 0.77):
        axis.add_patch(
            FancyArrowPatch(
                (1.77, vertical_coordinate),
                (1.48, vertical_coordinate),
                arrowstyle="-|>",
                mutation_scale=19,
                color=GREEN,
                lw=2.3,
            )
        )
    axis.text(1.87, 0.50, r"$q=-1$", color=GREEN, fontsize=21, rotation=90, ha="center", va="center")
    axis.text(0.73, 1.10, r"$q=0$", color=GREEN, fontsize=19, ha="center", va="bottom")
    axis.text(0.73, -0.14, r"$q=0$", color=GREEN, fontsize=19, ha="center", va="top")

    axis.scatter(vertices[:, 0], vertices[:, 1], s=125, color=BLUE, zorder=4)
    node_labels = (
        ("1", (-0.10, -0.10), "right", "top"),
        ("2", (1.55, -0.10), "left", "top"),
        ("3", (-0.10, 1.10), "right", "bottom"),
        ("4", (1.55, 1.10), "left", "bottom"),
    )
    for label, position, horizontal_alignment, vertical_alignment in node_labels:
        axis.text(
            *position,
            label,
            fontsize=18,
            color=DARK,
            ha=horizontal_alignment,
            va=vertical_alignment,
        )

    explanation_x = 2.30
    axis.text(explanation_x, 1.08, "nodal values", fontsize=19, fontweight="bold", color=BLUE)
    axis.text(explanation_x, 0.84, r"$U_1=U_3=0,\qquad U_2=U_4=1$", fontsize=22, color=DARK)
    axis.text(explanation_x, 0.52, "resulting finite element field", fontsize=19, fontweight="bold", color=BLUE)
    axis.text(explanation_x, 0.27, r"$u_h(x,y)=x$", fontsize=23, color=DARK)
    axis.text(
        explanation_x,
        -0.03,
        "Both triangles reproduce this linear field exactly.",
        fontsize=17,
        color=DARK,
        va="top",
    )
    save(figure, "two_triangle_patch_test.svg")


def make_reference_3d_numbering():
    """Offset all three-dimensional node labels from intersecting edges."""
    figure, axes = plt.subplots(1, 2, figsize=(12.0, 5.0))
    for axis in axes:
        axis.set_aspect("equal")
        axis.axis("off")

    axes[0].set_xlim(-0.25, 1.45)
    axes[0].set_ylim(-0.18, 1.35)
    axes[0].set_title("reference tetrahedron", fontsize=20, pad=10)
    tetra = np.array(((0.0, 0.0), (1.0, 0.0), (0.48, 0.36), (0.0, 1.0)))
    tetra_edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    for first, second in tetra_edges:
        axes[0].plot(tetra[[first, second], 0], tetra[[first, second], 1], color=BLUE, lw=2.4)
    axes[0].scatter(tetra[:, 0], tetra[:, 1], s=115, color=ORANGE, zorder=4)
    tetra_labels = ((-0.08, -0.12), (1.09, -0.11), (0.65, 0.51), (-0.10, 1.08))
    for number, position in enumerate(tetra_labels, start=1):
        axes[0].text(*position, str(number), fontsize=18, ha="center")

    axes[1].set_xlim(-0.22, 1.68)
    axes[1].set_ylim(-0.20, 1.45)
    axes[1].set_title("reference hexahedron", fontsize=20, pad=10)
    cube = np.array(
        ((0.0, 0.0), (1.0, 0.0), (1.43, 0.30), (0.43, 0.30), (0.0, 1.0), (1.0, 1.0), (1.43, 1.30), (0.43, 1.30))
    )
    cube_edges = (
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    )
    for first, second in cube_edges:
        axes[1].plot(cube[[first, second], 0], cube[[first, second], 1], color=BLUE, lw=2.2)
    axes[1].scatter(cube[:, 0], cube[:, 1], s=105, color=ORANGE, zorder=4)
    cube_labels = (
        (-0.09, -0.12), (1.09, -0.12), (1.54, 0.27), (0.34, 0.43),
        (-0.09, 1.07), (0.90, 1.14), (1.54, 1.34), (0.32, 1.34),
    )
    for number, position in enumerate(cube_labels, start=1):
        axes[1].text(*position, str(number), fontsize=18, ha="center")
    save(figure, "reference_3d_numbering.svg")


def make_physical_p1_triangle():
    """Show a physical P1 triangle with labels separated from the vertices."""
    figure, axis = plt.subplots(figsize=(11.5, 4.2))
    axis.set_xlim(-0.15, 2.95)
    axis.set_ylim(-0.22, 1.28)
    axis.axis("off")

    vertices = np.array(((0.0, 0.0), (1.55, 0.0), (0.0, 0.95)))
    axis.add_patch(Polygon(vertices, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=3.0))
    axis.scatter(vertices[:, 0], vertices[:, 1], s=170, color=BLUE, zorder=3)
    axis.text(0.55, 0.35, r"$\mathcal{K}_e$", ha="center", va="center", fontsize=24)
    axis.text(-0.02, -0.10, r"$\mathbf{x}_1=(0,0)$", ha="center", va="top", fontsize=18)
    axis.text(1.66, -0.05, r"$\mathbf{x}_2=(2,0)$", ha="left", va="center", fontsize=18)
    axis.text(-0.02, 1.06, r"$\mathbf{x}_3=(0,1)$", ha="center", va="bottom", fontsize=18)

    axis.text(1.90, 0.98, "local polynomial space", ha="left", fontsize=18, fontweight="bold", color=BLUE)
    axis.text(1.90, 0.70, r"$\mathbb{P}_1(\mathcal{K}_e)=\operatorname{span}\{1,x,y\}$", ha="left", fontsize=21)
    axis.text(1.90, 0.38, "nodal property", ha="left", fontsize=18, fontweight="bold", color=BLUE)
    axis.text(1.90, 0.13, r"$\phi_a^e(\mathbf{x}_b^e)=\delta_{ab}$", ha="left", fontsize=21)
    save(figure, "physical_p1_triangle.svg")


def make_reference_p1_triangle():
    """Show reference coordinates without placing an axis through a vertex label."""
    figure, axis = plt.subplots(figsize=(11.5, 6.0))
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.axis("off")

    origin = np.array((0.14, 0.16))
    x_vertex = np.array((0.62, 0.16))
    y_vertex = np.array((0.14, 0.76))
    triangle = np.vstack((origin, x_vertex, y_vertex))
    axis.add_patch(Polygon(triangle, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=3.0))
    axis.scatter(triangle[:, 0], triangle[:, 1], s=190, color=BLUE, zorder=3)

    axis.add_patch(FancyArrowPatch((0.08, 0.08), (0.72, 0.08), arrowstyle="-|>", mutation_scale=22, color=BLUE, lw=2.5))
    axis.add_patch(FancyArrowPatch((0.08, 0.08), (0.08, 0.88), arrowstyle="-|>", mutation_scale=22, color=BLUE, lw=2.5))
    axis.text(0.75, 0.07, r"$\xi$", ha="left", va="center", fontsize=24, color=BLUE)
    axis.text(0.07, 0.91, r"$\eta$", ha="center", va="bottom", fontsize=24, color=BLUE)

    axis.text(0.13, 0.05, r"$1:(0,0)$", ha="center", va="top", fontsize=20)
    axis.text(0.62, 0.05, r"$2:(1,0)$", ha="center", va="top", fontsize=20)
    axis.text(0.16, 0.82, r"$3:(0,1)$", ha="left", va="bottom", fontsize=20)

    axis.text(0.77, 0.68, r"$\widehat{\phi}_1=1-\xi-\eta$", ha="center", fontsize=22)
    axis.text(0.77, 0.50, r"$\widehat{\phi}_2=\xi$", ha="center", fontsize=22)
    axis.text(0.77, 0.32, r"$\widehat{\phi}_3=\eta$", ha="center", fontsize=22)
    save(figure, "reference_p1_triangle.svg")


def make_reference_triangle_mapping():
    """Separate mapping labels from the corresponding triangle vertices."""
    figure, axis = plt.subplots(figsize=(12.0, 4.6))
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.axis("off")

    reference = np.array(((0.07, 0.14), (0.32, 0.14), (0.07, 0.70)))
    physical = np.array(((0.67, 0.15), (0.93, 0.27), (0.75, 0.72)))
    axis.add_patch(Polygon(reference, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2.8))
    axis.add_patch(Polygon(physical, closed=True, facecolor="#f5dfbd", edgecolor="#a55c20", linewidth=2.8))
    axis.scatter(reference[:, 0], reference[:, 1], s=170, color=BLUE, zorder=3)
    axis.scatter(physical[:, 0], physical[:, 1], s=170, color=ORANGE, zorder=3)

    axis.text(0.18, 0.93, "reference triangle", ha="center", fontsize=19, fontweight="bold", color="#173a57")
    axis.text(0.82, 0.93, "physical triangle", ha="center", fontsize=19, fontweight="bold", color="#173a57")
    axis.text(0.04, 0.08, r"$\widehat{\mathbf{x}}_1$", ha="center", va="top", fontsize=18)
    axis.text(0.34, 0.08, r"$\widehat{\mathbf{x}}_2$", ha="center", va="top", fontsize=18)
    axis.text(0.04, 0.75, r"$\widehat{\mathbf{x}}_3$", ha="center", va="bottom", fontsize=18)
    axis.text(0.64, 0.08, r"$\mathbf{x}_1^e$", ha="center", va="top", fontsize=18)
    axis.text(0.96, 0.25, r"$\mathbf{x}_2^e$", ha="left", va="center", fontsize=18)
    axis.text(0.75, 0.77, r"$\mathbf{x}_3^e$", ha="center", va="bottom", fontsize=18)

    axis.add_patch(
        FancyArrowPatch(
            (0.39, 0.47),
            (0.62, 0.47),
            connectionstyle="arc3,rad=-0.28",
            arrowstyle="Simple,tail_width=1.0,head_width=10,head_length=12",
            color=BLUE,
        )
    )
    axis.text(0.50, 0.68, r"$\mathbf{x}=\mathbf{x}^e(\boldsymbol{\xi})$", ha="center", fontsize=18, color="#173a57")
    axis.text(0.50, 0.30, r"$\mathbf{x}^e(\widehat{\mathbf{x}}_a)=\mathbf{x}_a^e$", ha="center", fontsize=16, color="#4d5b6a")
    save(figure, "reference_triangle_mapping.svg")


def make_triangle_quadrature():
    """Place quadrature labels away from triangle edges."""
    figure, axes = plt.subplots(1, 2, figsize=(11.5, 5.0))
    for axis, title in zip(axes, ("one-point rule", "three-point rule")):
        axis.set_xlim(-0.08, 1.08)
        axis.set_ylim(-0.08, 1.08)
        axis.set_aspect("equal")
        axis.axis("off")
        axis.add_patch(Polygon(((0, 0), (1, 0), (0, 1)), closed=True, fill=False, edgecolor=BLUE, linewidth=3.0))
        axis.set_title(title, fontsize=20, pad=12)

    axes[0].scatter((1.0 / 3.0,), (1.0 / 3.0,), s=220, color=ORANGE, zorder=3)
    axes[0].text(0.13, 0.22, r"$(1/3,1/3)$", color=ORANGE, ha="left", va="top", fontsize=18)

    points = ((1.0 / 6.0, 1.0 / 6.0), (2.0 / 3.0, 1.0 / 6.0), (1.0 / 6.0, 2.0 / 3.0))
    axes[1].scatter(*zip(*points), s=160, color=GREEN, zorder=3)
    axes[1].text(0.54, 0.57, r"$w_r=1/6$", color=GREEN, ha="left", fontsize=18)
    save(figure, "triangle_quadrature.svg")


def make_vector_dofs_triangle():
    """Show vector degrees of freedom with every component label clear of edges."""
    figure, axis = plt.subplots(figsize=(11.5, 4.8))
    axis.set_xlim(-0.18, 1.70)
    axis.set_ylim(-0.18, 1.20)
    axis.axis("off")
    vertices = np.array(((0.0, 0.0), (0.82, 0.08), (0.16, 0.92)))
    axis.add_patch(Polygon(vertices, closed=True, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=3.0))
    axis.scatter(vertices[:, 0], vertices[:, 1], s=150, color="#5796c5", zorder=4)

    arrow_specs = (
        ((0.0, 0.0), (0.16, 0.0), ORANGE, r"$U_{11}$", (0.08, -0.10), "center", "top"),
        ((0.0, 0.0), (0.0, 0.22), GREEN, r"$U_{12}$", (-0.05, 0.16), "right", "center"),
        ((0.82, 0.08), (1.00, 0.08), ORANGE, r"$U_{21}$", (0.91, -0.03), "center", "top"),
        ((0.82, 0.08), (0.82, 0.31), GREEN, r"$U_{22}$", (0.87, 0.27), "left", "center"),
        ((0.16, 0.92), (0.34, 0.92), ORANGE, r"$U_{31}$", (0.37, 0.96), "left", "center"),
        ((0.16, 0.92), (0.16, 1.14), GREEN, r"$U_{32}$", (0.11, 1.08), "right", "center"),
    )
    for start, end, color, label, position, ha, va in arrow_specs:
        axis.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=18, color=color, lw=2.4, zorder=5))
        axis.text(*position, label, color=color, ha=ha, va=va, fontsize=18, zorder=6)

    axis.text(1.10, 0.82, r"$\mathbf{U}_i=(U_{i1},U_{i2})^T$", fontsize=24, fontweight="bold")
    axis.text(1.10, 0.47, "two displacement degrees\nof freedom at each vertex", fontsize=18, va="top", linespacing=1.3)
    save(figure, "vector_dofs_triangle.svg")


if __name__ == "__main__":
    make_p1_basis_functions()
    make_triangular_mesh_concepts()
    make_physical_p1_triangle()
    make_shared_edge_continuity()
    make_reference_p1_triangle()
    make_reference_triangle_mapping()
    make_triangle_quadrature()
    make_boundary_facet_load()
    make_two_triangle_patch_test()
    make_reference_3d_numbering()
    make_vector_dofs_triangle()
