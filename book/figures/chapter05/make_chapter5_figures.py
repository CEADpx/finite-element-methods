"""Generate selected Chapter 5 diagrams whose labels require precise placement."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUTPUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 15,
        "mathtext.fontset": "stix",
    }
)

BLUE = "#2f7fb8"
ORANGE = "#eb7a00"
DARK = "#202a35"


def save(figure, filename):
    figure.savefig(OUTPUT_DIR / filename, bbox_inches="tight", facecolor="white")
    plt.close(figure)


def make_mesh_partition():
    """Show the mesh endpoints with short dashed guides to x=0 and x=L."""
    figure, axis = plt.subplots(figsize=(12.0, 3.0))
    axis.set_xlim(-0.05, 1.05)
    axis.set_ylim(0.06, 0.94)
    axis.axis("off")

    nodes = (0.06, 0.35, 0.64, 0.93)
    colors = ("#2f7fb8", "#e67e22", "#2ca25f")
    baseline = 0.56
    for element, color in enumerate(colors):
        axis.plot(nodes[element : element + 2], (baseline, baseline), color=color, linewidth=7, solid_capstyle="round")
    axis.scatter(nodes, (baseline,) * 4, s=220, color=(colors[0], colors[1], colors[2], "#d7301f"), zorder=4)

    for index, coordinate in enumerate(nodes, start=1):
        axis.text(coordinate, 0.74, rf"$x_{index}$", ha="center", va="bottom", fontsize=21)
    for element, midpoint in enumerate(((nodes[0] + nodes[1]) / 2, (nodes[1] + nodes[2]) / 2, (nodes[2] + nodes[3]) / 2), start=1):
        axis.text(midpoint, 0.43, rf"$\mathcal{{K}}_{element}$", ha="center", va="top", fontsize=22)

    for coordinate in (nodes[0], nodes[-1]):
        axis.plot((coordinate, coordinate), (0.49, 0.25), color="#7b8792", linewidth=1.5, linestyle=(0, (4, 4)))
    axis.text(nodes[0], 0.19, r"$x=0$", ha="center", va="top", fontsize=19)
    axis.text(nodes[-1], 0.19, r"$x=L$", ha="center", va="top", fontsize=19)
    save(figure, "mesh_partition.svg")


def make_basis_overlap_sparsity():
    """Show the support-overlap pattern with readable row and column indices."""
    figure, axis = plt.subplots(figsize=(6.5, 6.1))
    axis.set_xlim(-1.32, 4.08)
    axis.set_ylim(-0.92, 4.58)
    axis.set_aspect("equal")
    axis.axis("off")

    for row in range(4):
        for column in range(4):
            overlaps = abs(row - column) <= 1
            axis.add_patch(
                Rectangle(
                    (column, 3 - row),
                    1.0,
                    1.0,
                    facecolor="#3b88bb" if overlaps else "#f7f7f7",
                    edgecolor="#4f5963",
                    linewidth=1.2,
                )
            )
            if not overlaps:
                axis.text(column + 0.5, 3.5 - row, r"$0$", fontsize=20, ha="center", va="center")

    for index in range(4):
        axis.text(index + 0.5, -0.16, rf"$j={index + 1}$", fontsize=18, ha="center", va="top")
        axis.text(-0.18, 3.5 - index, rf"$i={index + 1}$", fontsize=18, ha="right", va="center")

    axis.text(2.0, 4.42, r"$K_{ij}=0$ when the supports do not overlap", fontsize=19, ha="center", va="bottom")
    axis.text(2.0, -0.68, r"trial index $j$", fontsize=16, ha="center", va="top")
    axis.text(-1.08, 2.0, r"test index $i$", fontsize=16, ha="center", va="center", rotation=90)
    save(figure, "basis_overlap_sparsity.svg")


def make_linear_element_interpolation():
    """Show a linear element field without placing two node markers together."""
    figure, axis = plt.subplots(figsize=(11.5, 4.0))
    axis.set_xlim(-0.08, 1.08)
    axis.set_ylim(0.0, 1.02)
    axis.axis("off")

    baseline_y = 0.18
    field_y = (0.35, 0.78)
    axis.plot((0.0, 1.0), (baseline_y, baseline_y), color=BLUE, linewidth=7)
    axis.scatter((0.0, 1.0), (baseline_y, baseline_y), s=230, color=BLUE, zorder=3)

    axis.plot((0.0, 1.0), field_y, color=ORANGE, linewidth=6, zorder=4)
    axis.scatter((0.0, 1.0), field_y, s=250, color=ORANGE, zorder=5)
    axis.plot((0.0, 0.0), (baseline_y, field_y[0]), color="#9aa4ad", linestyle="--")
    axis.plot((1.0, 1.0), (baseline_y, field_y[1]), color="#9aa4ad", linestyle="--")

    axis.text(0.0, 0.07, r"$x_e$", ha="center", va="top", fontsize=22)
    axis.text(1.0, 0.07, r"$x_{e+1}$", ha="center", va="top", fontsize=22)
    axis.text(-0.025, field_y[0] + 0.08, r"$U_e$", ha="right", va="bottom", fontsize=22)
    axis.text(1.02, field_y[1] + 0.05, r"$U_{e+1}$", ha="left", va="bottom", fontsize=22)

    axis.text(
        0.20,
        0.91,
        r"$u_h|_{\mathcal{K}_e}=U_e\phi_1^e+U_{e+1}\phi_2^e$",
        ha="left",
        va="center",
        fontsize=21,
    )
    axis.annotate(
        "",
        xy=(0.60, 0.61),
        xytext=(0.54, 0.79),
        arrowprops={"arrowstyle": "-|>", "color": "black", "lw": 2.0},
    )
    axis.text(
        0.58,
        0.43,
        r"$u_h'=(U_{e+1}-U_e)/h_e$",
        ha="left",
        va="center",
        fontsize=20,
    )
    save(figure, "linear_element_interpolation.svg")


def make_reference_mapping_quadrature():
    """Place the mapping arrow and quadrature symbols in separate visual layers."""
    figure, axis = plt.subplots(figsize=(12.0, 3.25))
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 1.0)
    axis.axis("off")

    y = 0.40
    left_nodes = (0.05, 0.28, 0.40)
    right_nodes = (0.72, 0.84, 0.96)
    axis.plot((left_nodes[0], left_nodes[-1]), (y, y), color=DARK, linewidth=3)
    axis.scatter(left_nodes, (y, y, y), s=190, color=BLUE, zorder=3)
    axis.plot((right_nodes[0], right_nodes[-1]), (y, y), color=DARK, linewidth=3)
    axis.scatter(right_nodes, (y, y, y), s=190, color="#2ca25f", zorder=3)

    for x in (0.17, 0.35):
        axis.scatter(x, y, marker="x", s=280, color=ORANGE, linewidths=4, zorder=4)
    for x in (0.78, 0.90):
        axis.scatter(x, y, marker="x", s=280, color="#d62728", linewidths=4, zorder=4)

    axis.text(0.20, 0.91, r"reference element $\widehat{\mathcal{K}}$", ha="center", fontsize=20)
    axis.text(0.84, 0.91, r"physical element $\mathcal{K}_e$", ha="center", fontsize=20)
    arrow = FancyArrowPatch(
        (0.28, 0.52),
        (0.72, 0.52),
        connectionstyle="arc3,rad=-0.22",
        arrowstyle="Simple,tail_width=1.2,head_width=10,head_length=12",
        color=DARK,
    )
    axis.add_patch(arrow)
    axis.text(0.50, 0.80, r"$x=x^e(\xi)$", ha="center", fontsize=20)
    axis.text(
        0.50,
        0.44,
        r"$J_e=\mathrm{d}x/\mathrm{d}\xi$",
        ha="center",
        fontsize=18,
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5, "alpha": 0.78},
    )

    for x, label in zip(left_nodes, (r"$-1$", r"$0$", r"$1$")):
        axis.text(x, 0.22, label, ha="center", va="top", fontsize=18)
    for x, label in zip(right_nodes, (r"$x_e$", r"$x_m$", r"$x_{e+1}$")):
        axis.text(x, 0.22, label, ha="center", va="top", fontsize=18)
    axis.text(0.22, 0.03, r"quadrature points $\xi_r$", ha="center", fontsize=18)
    axis.text(0.84, 0.03, r"$x_r=x^e(\xi_r)$", ha="center", fontsize=18)
    save(figure, "reference_mapping_quadrature.svg")


def make_parametric_mapping_types():
    """Compare geometry and field interpolation without touching labels and nodes."""
    figure, axes = plt.subplots(1, 3, figsize=(12.0, 4.1))
    cases = (
        ("subparametric", 2, 3, r"$p_g<p_u$", "lower-order geometry"),
        ("isoparametric", 3, 3, r"$p_g=p_u$", "the same interpolation"),
        ("superparametric", 3, 2, r"$p_g>p_u$", "higher-order geometry"),
    )
    for axis, (title, geometry_nodes, field_nodes, relation, note) in zip(axes, cases):
        axis.set_xlim(0.0, 1.0)
        axis.set_ylim(0.0, 1.0)
        axis.axis("off")
        box = FancyBboxPatch(
            (0.02, 0.03),
            0.96,
            0.94,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=1.2,
            edgecolor="#c8d4df",
            facecolor="#fbfcfd",
        )
        axis.add_patch(box)
        axis.text(0.5, 0.88, title, ha="center", va="center", fontsize=18, fontweight="bold", color="#173a57")

        axis.text(0.11, 0.70, "geometry", ha="left", va="center", fontsize=15, color=DARK)
        axis.text(0.11, 0.44, "field", ha="left", va="center", fontsize=15, color=DARK)
        x0, x1 = 0.58, 0.91
        axis.plot((x0, x1), (0.70, 0.70), color="#d97728", linewidth=3)
        axis.plot((x0, x1), (0.44, 0.44), color="#245b85", linewidth=3)
        gx = [x0 + i * (x1 - x0) / (geometry_nodes - 1) for i in range(geometry_nodes)]
        fx = [x0 + i * (x1 - x0) / (field_nodes - 1) for i in range(field_nodes)]
        axis.scatter(gx, [0.70] * geometry_nodes, s=120, color="#d97728", zorder=3)
        axis.scatter(fx, [0.44] * field_nodes, s=120, color="#245b85", zorder=3)
        if geometry_nodes == field_nodes:
            for x in gx:
                axis.plot((x, x), (0.52, 0.62), color="#9aa8b5", linewidth=1.2, linestyle="--")

        axis.text(0.5, 0.25, relation, ha="center", va="center", fontsize=17, color=DARK)
        axis.text(0.5, 0.12, note, ha="center", va="center", fontsize=13, color="#4d5b6a")
    save(figure, "parametric_mapping_types.svg")


def make_assembly_scatter_add():
    """Show three element matrices entering distinct regions of the global matrix."""
    figure, axis = plt.subplots(figsize=(12.0, 7.5))
    axis.set_xlim(0.0, 12.0)
    axis.set_ylim(0.0, 7.5)
    axis.axis("off")

    def draw_matrix(origin_x, origin_y, entries, cell_size, facecolor="white", fontsize=14):
        rows = len(entries)
        columns = len(entries[0])
        for row in range(rows):
            for column in range(columns):
                x_coordinate = origin_x + column * cell_size
                y_coordinate = origin_y + (rows - 1 - row) * cell_size
                axis.add_patch(
                    Rectangle(
                        (x_coordinate, y_coordinate),
                        cell_size,
                        cell_size,
                        facecolor=facecolor,
                        edgecolor="#32383e",
                        linewidth=1.3,
                    )
                )
                axis.text(
                    x_coordinate + cell_size / 2,
                    y_coordinate + cell_size / 2,
                    entries[row][column],
                    ha="center",
                    va="center",
                    fontsize=fontsize,
                )

    local_data = (
        (1.05, r"$\mathcal{K}_1:\ I^1=(1,2)$", ((r"$K_{11}^1$", r"$K_{12}^1$"), (r"$K_{21}^1$", r"$K_{22}^1$"))),
        (5.05, r"$\mathcal{K}_2:\ I^2=(2,3)$", ((r"$K_{11}^2$", r"$K_{12}^2$"), (r"$K_{21}^2$", r"$K_{22}^2$"))),
        (9.05, r"$\mathcal{K}_3:\ I^3=(3,4)$", ((r"$K_{11}^3$", r"$K_{12}^3$"), (r"$K_{21}^3$", r"$K_{22}^3$"))),
    )
    for x_coordinate, title, entries in local_data:
        axis.text(x_coordinate + 0.85, 7.23, title, ha="center", fontsize=18)
        draw_matrix(x_coordinate, 5.25, entries, 0.85, fontsize=14)

    global_entries = (
        (r"$K_{11}^1$", r"$K_{12}^1$", r"$0$", r"$0$"),
        (r"$K_{21}^1$", r"$K_{22}^1+K_{11}^2$", r"$K_{12}^2$", r"$0$"),
        (r"$0$", r"$K_{21}^2$", r"$K_{22}^2+K_{11}^3$", r"$K_{12}^3$"),
        (r"$0$", r"$0$", r"$K_{21}^3$", r"$K_{22}^3$"),
    )
    global_x = 3.80
    global_y = 0.55
    global_cell = 1.10
    draw_matrix(global_x, global_y, global_entries, global_cell, fontsize=13)

    starts = ((1.90, 5.12), (5.90, 5.12), (9.90, 5.12))
    ends = ((4.90, 5.02), (6.45, 4.98), (7.10, 5.02))
    for start, end in zip(starts, ends):
        axis.add_patch(
            FancyArrowPatch(
                start,
                end,
                connectionstyle="arc3,rad=0.02",
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=1.8,
                color="#4b5157",
            )
        )

    axis.text(
        6.0,
        0.22,
        "shared entries accumulate contributions from adjacent elements",
        ha="center",
        fontsize=18,
    )
    save(figure, "assembly_scatter_add.svg")


if __name__ == "__main__":
    make_mesh_partition()
    make_basis_overlap_sparsity()
    make_linear_element_interpolation()
    make_reference_mapping_quadrature()
    make_parametric_mapping_types()
    make_assembly_scatter_add()
