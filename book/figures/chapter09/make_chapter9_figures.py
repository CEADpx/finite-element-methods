"""Reproduce the scalar Newton and constrained-stretch figures in Chapter 9."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUTPUT = Path(__file__).resolve().parent
BLUE, ORANGE = "#2f638f", "#c65b2a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 17,
                     "mathtext.fontset": "cm", "svg.fonttype": "path"})


def newton_tangent():
    fig, ax = plt.subplots(figsize=(8.0, 4.5), layout="constrained")
    z = np.linspace(0.7, 1.9, 200)
    ax.plot(z, z*z - 2, color=BLUE, lw=2.5, label=r"$r(z)=z^2-2$")
    ax.plot(z, 2*z - 3, color=ORANGE, lw=2, label=r"Tangent at $z^0=1$")
    ax.axhline(0, color="0.5", lw=1)
    ax.plot([1, 1], [-1, 0], ls="--", color="0.5", lw=1)
    ax.scatter([1, 1.5, np.sqrt(2)], [-1, 0, 0],
               c=[BLUE, ORANGE, BLUE], s=45, zorder=4)
    ax.annotate(r"$z^0=1$", (1, -1), xytext=(1.06, -1.26),
                arrowprops={"arrowstyle": "-", "color": "0.3"})
    ax.annotate(r"$z^1=1.5$", (1.5, 0), xytext=(1.57, -0.43),
                arrowprops={"arrowstyle": "-", "color": "0.3"})
    ax.annotate(r"$\sqrt{2}$", (np.sqrt(2), 0), xytext=(1.21, 0.34),
                arrowprops={"arrowstyle": "-", "color": "0.3"})
    ax.set(xlabel=r"$z$", ylabel=r"$r(z)$", xlim=(0.7, 1.9), ylim=(-1.6, 1.75))
    ax.legend(loc="upper left", fontsize=15, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUTPUT / "newton-tangent.svg", facecolor="white")
    plt.close(fig)


def stretch_solution():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.7), layout="constrained")
    s = 1.0
    iterates = []
    for _ in range(5):
        iterates.append(s)
        P = s - 1/s + 2*np.log(s)/s
        dP = 1 + 1/s**2 + 2*(1-np.log(s))/s**2
        s += (1-P)/dP
    x = np.linspace(0, 1, 200)
    nodes = np.linspace(0, 1, 3)
    axes[0].plot(x, (s-1)*x, color=BLUE, lw=2.5, label="Exact displacement")
    axes[0].plot(nodes, (s-1)*nodes, "o", color=ORANGE,
                 markersize=7, label="FE nodal values")
    axes[0].set(xlabel=r"$X_1$ (mm)", ylabel=r"$u_1$ (mm)",
                title="(a) Two linear elements", xlim=(-.025, 1.025), ylim=(-0.015, .38))
    axes[0].legend(loc="upper left", fontsize=14, frameon=False)
    curve_s = np.linspace(1, 1.44, 200)
    axes[1].plot(curve_s, curve_s - 1/curve_s + 2*np.log(curve_s)/curve_s,
                 color=BLUE, lw=2.5, label=r"$P_{11}(s)$")
    axes[1].axhline(1, color="0.4", ls="--", label=r"$\tau=1$ MPa")
    for k in (0, 1, 2):
        sk = iterates[k]
        pk = sk - 1/sk + 2*np.log(sk)/sk
        axes[1].plot(sk, pk, "o", color=ORANGE, ms=6)
        axes[1].annotate(rf"$k={k}$", (sk, pk), xytext=(8, -22),
                         textcoords="offset points", fontsize=15)
    axes[1].set(xlabel=r"Stretch $s$", ylabel=r"$P_{11}$ (MPa)",
                title="(b) Stress and Newton iterates", xlim=(.98, 1.44),
                ylim=(-.17, 1.35))
    axes[1].legend(loc="upper left", fontsize=14, frameon=False)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUTPUT / "stretch-solution.svg", facecolor="white")
    plt.close(fig)


def cube_boundary_data():
    fig = plt.figure(figsize=(8, 5.3), layout="constrained")
    ax = fig.add_subplot(projection="3d", computed_zorder=False)
    corners = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
                        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]])
    faces = [[0, 3, 7, 4], [1, 2, 6, 5], [0, 1, 5, 4],
             [3, 2, 6, 7], [0, 1, 2, 3], [4, 5, 6, 7]]
    colors = ["#b9d6ec", "#f5d6bf"] + ["#f4f4f4"] * 4
    for ids, color in zip(faces, colors):
        ax.add_collection3d(Poly3DCollection([corners[ids]], facecolor=color,
                             edgecolor="0.3", linewidth=1, alpha=.65, zorder=1))
    for y in (.25, .75):
        for z in (.25, .75):
            ax.quiver(1, y, z, .32, 0, 0, color=ORANGE,
                      arrow_length_ratio=.25, linewidth=2, zorder=4)
    ax.set(xlabel=r"$X_1$ (mm)", ylabel=r"$X_2$ (mm)",
           zlabel=r"$X_3$ (mm)", xlim=(0, 1.4), ylim=(0, 1), zlim=(0, 1),
           xticks=[0, 1], yticks=[0, 1], zticks=[0, 1])
    ax.set_box_aspect((1.4, 1, 1))
    ax.view_init(elev=20, azim=-58)
    ax.grid(False)
    fig.text(.04, .94, r"$\boldsymbol{u}=\boldsymbol{0}$ on $X_1=0$", color=BLUE)
    fig.text(.49, .94, r"$\overline{\boldsymbol{t}}_0=0.2\zeta\boldsymbol{e}_1$ MPa",
             color=ORANGE)
    fig.savefig(OUTPUT / "cube-boundary-data.svg", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    newton_tangent()
    stretch_solution()
    cube_boundary_data()
