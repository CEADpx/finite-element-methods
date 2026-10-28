"""Regenerate Chapter 8 figures in the finite-elements Conda environment.

Reuse the companion notebook's numerical functions without executing its
presentation cells or changing the notebook. Use --concepts-only to rebuild
the explanatory figures without rerunning the adaptive computations.
"""

import ast
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "finite-elements-matplotlib")
)
if sys.platform == "darwin":
    os.environ.setdefault("CC", "/usr/bin/clang")
    os.environ.setdefault("LDSHARED", "/usr/bin/clang -bundle -undefined dynamic_lookup")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.collections import PolyCollection
from matplotlib.patches import Polygon, Rectangle
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parent
ROOT = OUTPUT_DIR.parents[2]
BLUE = "#2f638f"
ORANGE = "#c65b2a"
EDGE = "#707b85"


def notebook_functions():
    notebook = json.loads(
        (ROOT / "notebooks/adaptivity/residual_adaptivity.ipynb").read_text()
    )
    namespace = {}
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        tree = ast.parse("".join(cell["source"]))
        definitions = [
            node for node in tree.body
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        ]
        exec(compile(ast.Module(body=definitions, type_ignores=[]),
                     "residual_adaptivity.ipynb", "exec"), namespace)
    namespace["quadrature_degree"] = 20
    return namespace


def save(figure, name):
    figure.savefig(
        OUTPUT_DIR / f"{name}.svg", bbox_inches="tight", pad_inches=0.05,
        metadata={"Date": None},
    )
    plt.close(figure)


def patch_figure():
    figure, ax = plt.subplots(figsize=(4.25, 3.35))
    ax.set_aspect("equal")
    ax.add_patch(Polygon(
        [(-1, -1), (1, -1), (1, 1), (-1, 1)],
        facecolor="#e6f0f7", edgecolor=BLUE, linewidth=1.35,
    ))
    ax.plot([-1, 1], [-1, 1], color=BLUE, linewidth=1.1)
    ax.plot([-1, 1], [1, -1], color=BLUE, linewidth=1.1)
    corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    ax.plot(corners[:, 0], corners[:, 1], "o", color=BLUE, markersize=3)
    ax.plot(0, 0, "o", color=ORANGE, markersize=4)
    ax.text(0.25, 0.05, r"$(0,0)$", fontsize=10.5, va="bottom")
    for x, y in corners:
        ax.annotate(
            rf"$({x},{y})$", (x, y),
            xytext=(5 if x > 0 else -5, 6 if y > 0 else -7),
            textcoords="offset points", ha="left" if x > 0 else "right",
            va="bottom" if y > 0 else "top", fontsize=10.5,
        )
    for label, xy in zip(
        [r"$\mathcal{K}_1$", r"$\mathcal{K}_2$", r"$\mathcal{K}_3$", r"$\mathcal{K}_4$"],
        [(0, -0.66), (0.67, 0), (0, 0.66), (-0.67, 0)],
    ):
        ax.text(*xy, label, ha="center", va="center", color=BLUE, fontsize=11)
    ax.set_title(r"Center-vertex patch: $\omega_1=\Omega$", fontsize=11, pad=13)
    ax.set(xlim=(-1.4, 1.4), ylim=(-1.2, 1.2))
    ax.axis("off")
    save(figure, "patch-average")


def facet_normals():
    figure, ax = plt.subplots(figsize=(6.4, 3.3))
    for vertices, fill in [
        ([(-1.8, 0), (0, -1.2), (0, 1.2)], "#e6f0f7"),
        ([(1.8, 0), (0, -1.2), (0, 1.2)], "#f5e8db"),
    ]:
        ax.add_patch(Polygon(vertices, facecolor=fill, edgecolor=EDGE, linewidth=1.1))
    ax.plot([0, 0], [-1.2, 1.2], color=BLUE, linewidth=2)
    ax.text(-0.9, 0, r"$\mathcal{K}^+$", ha="center", fontsize=15)
    ax.text(0.9, 0, r"$\mathcal{K}^-$", ha="center", fontsize=15)
    for y, end, label in [
        (0.43, 0.65, r"$\mathbfit{n}^+$"),
        (-0.43, -0.65, r"$\mathbfit{n}^-$"),
    ]:
        ax.annotate("", (end, y), (0, y),
                    arrowprops={"arrowstyle": "-|>", "color": ORANGE, "lw": 1.7})
        ax.text(end/2, y + (0.17 if y > 0 else -0.23), label,
                ha="center", fontsize=12)
    ax.text(0, 1.3, r"Shared facet $\mathcal{F}$", ha="center", fontsize=12)
    ax.text(0, -1.63,
            r"$j_{\mathcal{F}}=-(\mathbfit{q}_h^+\!\cdot\mathbfit{n}^+"
            r"+\mathbfit{q}_h^-\!\cdot\mathbfit{n}^-)$",
            ha="center", fontsize=15)
    ax.set(xlim=(-2.05, 2.05), ylim=(-1.82, 1.62), aspect="equal")
    ax.axis("off")
    save(figure, "facet-normals")


def bar_residuals():
    figure, axes = plt.subplots(1, 2, figsize=(8.5, 3.5), layout="constrained")
    nodes = np.linspace(0, 1, 5)
    x = np.linspace(0, 1, 501)
    exact = x - x*x/2
    nodal = nodes - nodes*nodes/2
    axes[0].plot(x, exact, color=ORANGE, label=r"Exact $u$")
    axes[0].plot(nodes, nodal, "o-", color=BLUE, markersize=4, label=r"FE $u_h$")
    axes[0].set_title("(a) Displacement")
    axes[0].set_ylabel("Displacement")
    axes[0].set_ylim(-0.015, 0.56)
    axes[1].plot(x, 1-x, color=ORANGE, label=r"Exact $u'$")
    for a, b in zip(nodes[:-1], nodes[1:]):
        axes[1].plot([a, b], [1-(a+b)/2]*2, color=BLUE, lw=2,
                     label=r"FE $u_h'$" if a == 0 else None)
    axes[1].set_title(r"(b) Axial force ($AE=1$)")
    axes[1].set_ylabel("Axial force")
    axes[1].set_ylim(-0.02, 1.13)
    for ax in axes:
        ax.set_xlabel(r"$x$")
        ax.set_xticks(nodes, [r"$0$", r"$1/4$", r"$1/2$", r"$3/4$", r"$1$"])
        ax.grid(color="#d8dce0", lw=0.5)
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.12),
                  ncol=2, frameon=False, fontsize=10)
    save(figure, "bar-residuals")


def approximation_patches():
    points = np.array([(i, j) for j in range(7) for i in range(7)], dtype=float)
    triangles = []
    for j in range(6):
        for i in range(6):
            a = 7*j+i
            triangles.extend([[a, a+1, a+8], [a, a+8, a+7]])
    triangles = np.array(triangles)
    vertex = 7*3+3
    element_nodes = np.array([7*2+2, 7*2+3, 7*3+3])
    facet_nodes = np.array([7*2+2, 7*3+3])
    masks = [np.any(triangles == vertex, axis=1),
             np.any(np.isin(triangles, element_nodes), axis=1),
             np.any(np.isin(triangles, facet_nodes), axis=1)]
    assert masks[0].sum() == 6
    figure, axes = plt.subplots(1, 3, figsize=(9.2, 3.35), layout="constrained")
    titles = [r"(a) Vertex patch $\omega_i$", r"(b) Element patch $\omega_e$",
              r"(c) Facet patch $\omega_{\mathcal{F}}$"]
    for ax, mask, title in zip(axes, masks, titles):
        ax.add_collection(PolyCollection(points[triangles[mask]],
                          facecolor="#d9eaf5", edgecolor="none"))
        ax.triplot(points[:, 0], points[:, 1], triangles, color=EDGE, lw=0.55)
        ax.set(aspect="equal", xlim=(-0.05, 6.05), ylim=(-0.05, 6.05))
        ax.axis("off")
        ax.set_title(title, fontsize=13, pad=10)
    axes[0].plot(*points[vertex], "o", color=ORANGE, markersize=6)
    axes[0].text(3.2, 2.55, r"$\mathbfit{x}_i$", fontsize=13,
                 bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1})
    axes[1].add_patch(Polygon(points[element_nodes], facecolor=BLUE, edgecolor=BLUE))
    axes[2].plot(*points[facet_nodes].T, color=ORANGE, lw=3)
    axes[2].text(3.25, 2.25, r"$\mathcal{F}$", fontsize=13, color=ORANGE,
                 bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none", "pad": 1})
    save(figure, "approximation-patches")


def quasi_interpolant():
    figure = plt.figure(figsize=(10.2, 3.8), layout="constrained")
    surface_axes = [figure.add_subplot(131, projection="3d"),
                    figure.add_subplot(132, projection="3d")]
    t = np.linspace(-1, 1, 51)
    x, y = np.meshgrid(t, t)
    v = (1-x*x)*(1-y*y)
    for panel, (ax, title) in enumerate(zip(surface_axes,
            [r"(a) Function $v$", r"(b) Averaging $\mathcal{Q}_h v$"])):
        if panel == 0:
            ax.plot_surface(x, y, v, cmap="Blues", vmin=0, vmax=1,
                            linewidth=0, antialiased=True, rcount=51, ccount=51)
        else:
            ax.plot_trisurf([-1,1,1,-1,0], [-1,-1,1,1,0], [0,0,0,0,4/9],
                            triangles=[[0,1,4], [1,2,4], [2,3,4], [3,0,4]],
                            color="#78b1d3", edgecolor=BLUE, linewidth=0.8,
                            shade=True, antialiased=True)
        ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(0, 1))
        ax.set_xticks([-1, 0, 1]); ax.set_yticks([0, 1]); ax.set_zticks([0, .5, 1])
        ax.set_xlabel(r"$x_1$", fontsize=14, labelpad=0)
        ax.set_ylabel(r"$x_2$", fontsize=14, labelpad=0)
        ax.tick_params(labelsize=12, pad=0)
        ax.set_title(title, fontsize=14, pad=12)
        ax.view_init(elev=25, azim=-55)
        ax.set_box_aspect((1, 1, .7))
    ax = figure.add_subplot(133)
    ax.plot(t, 1-t*t, color=ORANGE, label=r"$v$")
    ax.plot(t, 1-np.abs(t), color=EDGE, ls="--", label=r"$\mathcal{I}_h v$")
    ax.plot(t, (4/9)*(1-np.abs(t)), color=BLUE, label=r"$\mathcal{Q}_h v$")
    ax.set(ylim=(0, 1.08))
    ax.set_title(r"(c) Section at $x_2=0$", fontsize=14)
    ax.set_xlabel(r"$x_1$", fontsize=14)
    ax.set_yticks([0, 4/9, 1], [r"$0$", r"$4/9$", r"$1$"])
    ax.set_xticks([-1, 0, 1])
    ax.tick_params(labelsize=12)
    ax.legend(frameon=False, loc="upper right", fontsize=13)
    ax.grid(color="#d8dce0", lw=0.5)
    save(figure, "quasi-interpolant")


def facet_allocation():
    figure, ax = plt.subplots(figsize=(7.8, 3.2))
    for coords, fill, name, x in [
        ([(-2.2,0), (0,-1.2), (0,1.2)], "#e6f0f7", r"$\mathcal{K}^+$", -.9),
        ([(2.2,0), (0,-1.2), (0,1.2)], "#f5e8db", r"$\mathcal{K}^-$", .9),
    ]:
        ax.add_patch(Polygon(coords, facecolor=fill, edgecolor=EDGE, lw=1.2))
        ax.text(x, .35, name, fontsize=15, ha="center")
        ax.text(x, -.12, r"$\frac{1}{2} S_{\mathcal{F}}$", fontsize=19, ha="center")
    ax.plot([0,0], [-1.2,1.2], color=ORANGE, lw=3)
    ax.text(0, 1.45, r"$S_{\mathcal{F}}=h_{\mathcal{F}}"
            r"\Vert j_{\mathcal{F}}\Vert_{L^2(\mathcal{F})}^2$", ha="center", fontsize=15)
    ax.text(0, -1.6, r"Global facet contribution: $\frac{1}{2}S_{\mathcal{F}}"
            r"+\frac{1}{2}S_{\mathcal{F}}=S_{\mathcal{F}}$", ha="center", fontsize=14)
    ax.set(xlim=(-2.6, 2.6), ylim=(-1.85, 1.85), aspect="equal")
    ax.axis("off")
    save(figure, "facet-allocation")


def four_triangle_indicators():
    figure, axes = plt.subplots(1, 2, figsize=(8.4, 3.8),
                                gridspec_kw={"width_ratios": [1, 1.15]},
                                layout="constrained")
    ax = axes[0]
    corners = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
    for a in range(4):
        ax.add_patch(Polygon([corners[a], corners[(a + 1) % 4], [0, 0]],
                             facecolor="#e6f0f7", edgecolor=BLUE, lw=1.2))
    ax.plot([0, 1], [0, -1], color=ORANGE, lw=2.5)
    ax.plot(0, 0, "o", color=ORANGE, ms=4)
    for i, (x, y, dx, dy) in enumerate([
        (0, -.58, 0, .25), (.58, 0, -.25, 0),
        (0, .58, 0, -.25), (-.58, 0, .25, 0),
    ], 1):
        ax.text(x * 1.4, y * 1.4, rf"$\mathcal{{K}}_{i}$",
                ha="center", va="center", fontsize=14)
        ax.annotate("", (x + dx, y + dy), (x, y),
                    arrowprops={"arrowstyle": "-|>", "lw": 1.5, "color": BLUE})
    for x, y in corners:
        ax.annotate(rf"$({x},{y})$", (x, y),
                    xytext=(4 if x > 0 else -4, 6 if y > 0 else -7),
                    textcoords="offset points", ha="left" if x > 0 else "right",
                    va="bottom" if y > 0 else "top", fontsize=12)
    ax.set_title(r"(a) $u_h=\phi_1$, $U_1=1$", pad=17, fontsize=14)
    ax.text(0, -1.44, r"Arrows: $\mathbfit{q}_h=\nabla u_h$", ha="center", fontsize=14)
    ax.text(0, -1.72, r"Orange edge: $h_{\mathcal{F}}\Vert j_{\mathcal{F}}\Vert_{L^2(\mathcal{F})}^2=4$",
            ha="center", fontsize=14)
    ax.set(aspect="equal", xlim=(-1.55, 1.55), ylim=(-1.85, 1.35))
    ax.axis("off")

    ax = axes[1]
    x = np.arange(1, 5)
    ax.bar(x, np.full(4, 36), color=BLUE, width=.62, label="Element residual")
    ax.bar(x, np.full(4, 4), bottom=36, color="#e6ab7c", width=.62,
           label="Two half-facet contributions")
    for i in x:
        ax.text(i, 18, r"$36$", ha="center", va="center", color="white", fontsize=12)
        ax.text(i, 38, r"$4$", ha="center", va="center", fontsize=14)
    ax.set_title(r"(b) $\eta_e^2=36+4=40$", pad=17, fontsize=14)
    ax.set_xticks(x, [rf"$\mathcal{{K}}_{i}$" for i in x], fontsize=13)
    ax.tick_params(axis="y", labelsize=12)
    ax.yaxis.label.set_size(13)
    ax.set(ylabel=r"Squared indicator $\eta_e^2$", ylim=(0, 44), yticks=[0, 20, 40])
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(.5, -.43), frameon=False,
              fontsize=12)
    save(figure, "four-triangle-indicators")


def bar_refinement_step():
    figure, axes = plt.subplots(2, 2, figsize=(8.2, 3.9),
                                gridspec_kw={"width_ratios": [3.7, 1]},
                                layout="constrained")
    rows = [
        ([0, .25, 1], [r"$1/4$", r"$3/4$"],
         [r"$1/64$", r"$27/64$"], r"(a) Coarse mesh: mark $\mathcal{K}_2$",
         r"$\eta_{\mathrm{1D}}^2=\frac{7}{16}$"),
        ([0, .25, .625, 1], [r"$1/4$", r"$3/8$", r"$3/8$"],
         [r"$1/64$", r"$27/512$", r"$27/512$"], "(b) Bisect the marked element and solve again",
         r"$\eta_{\mathrm{1D,new}}^2=\frac{31}{256}$"),
    ]
    coordinates = {0: r"$0$", .25: r"$1/4$", .625: r"$5/8$", 1: r"$1$"}
    for row, (nodes, lengths, values, title, total) in enumerate(rows):
        ax = axes[row, 0]
        for e, (a, b) in enumerate(zip(nodes[:-1], nodes[1:])):
            color = ORANGE if row == 0 and e == 1 else BLUE
            ax.plot([a, b], [.6, .6], color=color, lw=6, solid_capstyle="butt")
            ax.text((a + b)/2, .96, rf"$h_{e+1}=$" + lengths[e],
                    ha="center", va="center", fontsize=14)
            ax.text((a + b)/2, .03, values[e], ha="center", fontsize=14)
        for x in nodes:
            ax.plot(x, .6, "o", markerfacecolor=ORANGE if x == .625 else "white",
                    markeredgecolor=BLUE, markeredgewidth=1.2, ms=6, zorder=3)
            ax.text(x, .32, coordinates[x], ha="center", va="center", fontsize=12)
        ax.text(-.035, .03, r"$h_e^3:$", ha="right", fontsize=14)
        ax.set_title(title, loc="left", pad=10, fontsize=14)
        ax.set(xlim=(-.1, 1.05), ylim=(-.12, 1.15))
        ax.axis("off")
        axes[row, 1].text(.5, .48, total, ha="center", va="center", fontsize=16)
        axes[row, 1].axis("off")
    save(figure, "bar-refinement-step")


def conforming_refinement():
    figure, axes = plt.subplots(1, 3, figsize=(9, 3), layout="constrained")
    for ax in axes:
        ax.plot([0,1,1,0,0], [0,0,1,1,0], color=BLUE, lw=1.3)
        ax.plot([0,1], [0,1], color=BLUE, lw=1.3)
        ax.set(aspect="equal", xlim=(-.05,1.05), ylim=(-.08,1.05))
        ax.axis("off")
    axes[0].add_patch(Polygon([(0,0),(1,0),(1,1)], facecolor="#d9eaf5",
                             edgecolor="none", zorder=-1))
    for ax in axes[1:]:
        ax.plot([.5,1], [.5,0], color=BLUE, lw=1.3)
        ax.plot(.5, .5, "o", color=ORANGE, ms=5)
    axes[2].plot([.5,0], [.5,1], color=BLUE, lw=1.3)
    axes[2].plot(.5, .5, "o", color=ORANGE, ms=5, zorder=4)
    for ax, title in zip(axes, ["(a) Mark one triangle", "(b) Split the marked triangle",
                               "(c) Split its neighbor"]):
        ax.set_title(title, fontsize=12, pad=13)
    axes[1].annotate("Hanging node", (.5,.5), (.36,-.22), ha="center", fontsize=11,
                     arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 1.1})
    save(figure, "conforming-refinement")


def concept_figures():
    facet_normals()
    bar_residuals()
    approximation_patches()
    quasi_interpolant()
    facet_allocation()
    four_triangle_indicators()
    bar_refinement_step()
    conforming_refinement()


def draw_mesh(ax, domain, api, title, marked=None, corner=False, zoom=False):
    triangles = api["mesh_triangles"](domain)
    if marked is not None:
        points = np.column_stack((triangles.x, triangles.y))
        ax.add_collection(PolyCollection(
            points[triangles.triangles[marked]], facecolor="#78b1d3", edgecolor="none",
        ))
    count = len(triangles.triangles)
    ax.triplot(triangles, color=EDGE, linewidth=0.42 if count < 350 else 0.27)
    boundary = (
        [(-1, -1), (0, -1), (0, 0), (1, 0), (1, 1), (-1, 1)]
        if corner else [(0, 0), (1, 0), (1, 1), (0, 1)]
    )
    ax.add_patch(Polygon(boundary, closed=True, fill=False, edgecolor=BLUE,
                         linewidth=1.05, zorder=3))
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=10.5, pad=8)
    ax.set_xlabel(r"$x_1$", labelpad=3)
    ax.set_ylabel(r"$x_2$", labelpad=3)
    ax.tick_params(labelsize=9.5, length=3, pad=3)
    for spine in ax.spines.values():
        spine.set_color("#9aa4ad")
        spine.set_linewidth(0.6)
    if corner:
        limit = 0.2 if zoom else 1.06
        ax.set(xlim=(-limit, limit), ylim=(-limit, limit))
        ticks = [-0.2, 0, 0.2] if zoom else [-1, 0, 1]
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.plot(0, 0, "o", color=ORANGE, markersize=3.3, zorder=4)
        if not zoom:
            ax.add_patch(Rectangle(
                (-0.2, -0.2), 0.4, 0.4, fill=False, edgecolor=ORANGE,
                linestyle=(0, (4, 2.5)), linewidth=1.0, zorder=4,
            ))
    else:
        ax.set(xlim=(-0.025, 1.025), ylim=(-0.025, 1.025))
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])


def mesh_figures(api, domains, marked, corner_domain):
    figure, axes = plt.subplots(1, 2, figsize=(6.5, 3.25), layout="constrained")
    draw_mesh(axes[0], domains[0], api, "(a) Marked elements\n3 of 128 triangles", marked)
    draw_mesh(axes[1], domains[1], api, "(b) Refined mesh\n148 triangles")
    save(figure, "pulse-marked-refined")

    figure, axes = plt.subplots(1, 3, figsize=(6.5, 2.65), layout="constrained")
    for ax, cycle, label in zip(axes, [0, 3, 6], ["a", "b", "c"]):
        count = domains[cycle].topology.index_map(2).size_local
        draw_mesh(ax, domains[cycle], api, f"({label}) Cycle {cycle}\n{count:,} triangles")
    save(figure, "pulse-mesh-history")

    figure, axes = plt.subplots(1, 2, figsize=(6.5, 3.35), layout="constrained")
    draw_mesh(axes[0], corner_domain, api, "(a) Adaptive L-shaped mesh", corner=True)
    draw_mesh(axes[1], corner_domain, api, "(b) Enlarged corner region", corner=True, zoom=True)
    save(figure, "corner-mesh")


def convergence_figures(adaptive, uniform):
    figure, ax = plt.subplots(figsize=(6.4, 4.0), layout="constrained")
    for data, color, marker, name in [
        (uniform, ORANGE, "s", "Uniform"), (adaptive, BLUE, "o", "Adaptive"),
    ]:
        ax.loglog(data[0], data[2], color=color, marker=marker, markersize=4,
                  linewidth=1.4, label=f"{name}: energy error")
        ax.loglog(data[0], data[1], color=color, marker=marker, markersize=4,
                  linewidth=1.2, linestyle="--", label=rf"{name}: estimator $\eta$")
    handles, labels = ax.get_legend_handles_labels()
    order = [0, 2, 1, 3]
    figure.legend(
        [handles[i] for i in order], [labels[i] for i in order],
        loc="outside upper center", ncol=2, frameon=False, fontsize=10,
        columnspacing=1.6, handlelength=2.6,
    )
    ax.set_xlabel("Total scalar FE degrees of freedom")
    ax.set_ylabel("Energy error or estimator")
    ax.grid(which="major", color="#d8dce0", linewidth=0.5)
    ax.set_axisbelow(True)
    save(figure, "pulse-verification")

    figure, ax = plt.subplots(figsize=(6.4, 3.55), layout="constrained")
    for data, color, marker, name in [
        (uniform, ORANGE, "s", "Uniform"), (adaptive, BLUE, "o", "Adaptive"),
    ]:
        ax.semilogx(
            data[0], np.asarray(data[1]) / data[2], color=color, marker=marker,
            markersize=4, linewidth=1.4, label=name,
        )
    figure.legend(loc="outside upper center", ncol=2, frameon=False, fontsize=10)
    ax.set_xlabel("Total scalar FE degrees of freedom")
    ax.set_ylabel(r"$I_{\mathrm{eff}}=\eta/\Vert u-u_h\Vert_a$", fontsize=12)
    ax.set_ylim(4.3, 10.2)
    ax.grid(which="major", color="#d8dce0", linewidth=0.5)
    ax.set_axisbelow(True)
    save(figure, "pulse-effectivity")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--concepts-only", action="store_true")
    args = parser.parse_args()
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["STIX Two Text", "STIXGeneral"],
        "font.size": 11, "axes.labelsize": 11, "xtick.labelsize": 10,
        "ytick.labelsize": 10, "mathtext.fontset": "cm", "svg.fonttype": "path",
        "svg.hashsalt": "finite-elements-chapter08", "axes.linewidth": 0.7,
    })
    concept_figures()
    if args.concepts_only:
        print("Regenerated explanatory vector figures.")
        return
    api = notebook_functions()
    domains, adaptive_dofs, adaptive_eta, adaptive_error = [], [], [], []
    domain = api["create_square_mesh"]()
    for cycle in range(9):
        exact, source = api["pulse_data"](domain)
        space, solution = api["solve_diffusion"](domain, source)
        volume, facet = api["estimate_error"](domain, solution, source)
        squared = volume + facet
        domains.append(domain)
        adaptive_dofs.append(space.dofmap.index_map.size_global)
        adaptive_eta.append(np.sqrt(np.sum(squared)))
        adaptive_error.append(api["energy_error"](domain, solution, exact))
        if cycle < 8:
            marked = api["mark_elements"](squared, 0.5)
            if cycle == 0:
                first_marked = marked.copy()
            domain = api["refine_marked_elements"](domain, marked)

    uniform_dofs, uniform_eta, uniform_error = [], [], []
    domain = api["create_square_mesh"]()
    for level in range(5):
        exact, source = api["pulse_data"](domain)
        space, solution = api["solve_diffusion"](domain, source)
        volume, facet = api["estimate_error"](domain, solution, source)
        uniform_dofs.append(space.dofmap.index_map.size_global)
        uniform_eta.append(np.sqrt(np.sum(volume + facet)))
        uniform_error.append(api["energy_error"](domain, solution, exact))
        if level < 4:
            domain, _, _ = api["mesh"].refine(domain)

    corner_domain = api["create_l_shaped_mesh"]()
    for cycle in range(7):
        source = api["fem"].Constant(corner_domain, api["PETSc"].ScalarType(1.0))
        _, solution = api["solve_diffusion"](corner_domain, source)
        volume, facet = api["estimate_error"](corner_domain, solution, source)
        if cycle < 6:
            marked = api["mark_elements"](volume + facet, 0.5)
            corner_domain = api["refine_marked_elements"](corner_domain, marked)

    assert len(first_marked) == 3
    assert domains[1].topology.index_map(2).size_local == 148
    assert adaptive_dofs[-1] == 2869
    assert np.isclose(adaptive_error[-1], 0.0831066, rtol=1e-5)
    assert np.isclose(uniform_error[-1], 0.166056, rtol=1e-5)
    patch_figure()
    mesh_figures(api, domains, first_marked, corner_domain)
    convergence_figures(
        (adaptive_dofs, adaptive_eta, adaptive_error),
        (uniform_dofs, uniform_eta, uniform_error),
    )
    print("Regenerated thirteen vector figures; mesh counts and reported errors verified.")


if __name__ == "__main__":
    main()
