"""Generate the instructional diagrams used in Chapter 3."""

from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

OUTPUT_DIR = Path(__file__).resolve().parent


def save_figure(fig: plt.Figure, stem: str) -> None:
    """Save editable vector and high-resolution raster versions."""
    fig.savefig(OUTPUT_DIR / f"{stem}.svg", bbox_inches="tight", facecolor="white")
    fig.savefig(
        OUTPUT_DIR / f"{stem}.png",
        bbox_inches="tight",
        facecolor="white",
        dpi=240,
    )
    plt.close(fig)


def make_formulation_process() -> None:
    """Draw the stages from a strong problem to a variational problem."""
    fig, ax = plt.subplots(figsize=(12.5, 2.8))
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        (
            "Strong\nproblem",
            "PDE and boundary\nconditions",
            "#f5f9fd",
            "#8eb6d8",
            "#002554",
        ),
        (
            "Weighted\nresidual",
            "Multiply by a weight\nand integrate",
            "#fffaf0",
            "#d4a72c",
            "#5f4800",
        ),
        (
            "Integration by\nparts",
            "Transfer derivatives and\nexpose boundary terms",
            "#f6f7f8",
            "#9ca3a8",
            "#343a40",
        ),
        (
            "Spaces and\nboundary data",
            "Choose trial and\ntest spaces",
            "#f2faf8",
            "#4f9d8f",
            "#17675c",
        ),
        (
            "Variational\nproblem",
            (
                "Find $u\\in\\mathcal{U}$ such that\n"
                "$a(u,v)=\\ell(v)$ for all $v\\in\\mathcal{V}$"
            ),
            "#eef3f8",
            "#002554",
            "#002554",
        ),
    ]

    width = 0.16
    height = 0.58
    y = 0.21
    x_positions = [0.05, 0.252, 0.454, 0.656, 0.858]

    for index, (title, body, fill, edge, title_color) in enumerate(boxes):
        x = x_positions[index]
        patch = FancyBboxPatch(
            (x, y),
            width,
            height,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            linewidth=2.2,
            edgecolor=edge,
            facecolor=fill,
        )
        ax.add_patch(patch)
        title_y = y + 0.42
        ax.text(
            x + width / 2,
            title_y,
            title,
            ha="center",
            va="center",
            fontsize=11.5,
            fontweight="bold",
            color=title_color,
            linespacing=1.08,
        )
        ax.text(
            x + width / 2,
            y + 0.15,
            body,
            ha="center",
            va="center",
            fontsize=9.2,
            color="#40464b",
            linespacing=1.25,
        )

        if index < len(boxes) - 1:
            arrow = FancyArrowPatch(
                (x + width + 0.008, 0.5),
                (x_positions[index + 1] - 0.008, 0.5),
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=1.8,
                color="#687078",
            )
            ax.add_patch(arrow)

    save_figure(fig, "variational-formulation-process")


def make_boundary_partition() -> None:
    """Draw the Dirichlet--Neumann partition for the diffusion problem."""
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    left, bottom, right, top = 0.20, 0.19, 0.78, 0.79
    domain = Rectangle(
        (left, bottom),
        right - left,
        top - bottom,
        facecolor="#f5f7fa",
        edgecolor="none",
    )
    ax.add_patch(domain)

    dirichlet = "#266aa6"
    neumann = "#d9792b"
    line_width = 8

    ax.plot([left, left], [bottom, top], color=dirichlet, linewidth=line_width)
    ax.plot([left, right], [bottom, bottom], color=dirichlet, linewidth=line_width)
    ax.plot([left, right], [top, top], color=neumann, linewidth=line_width)
    ax.plot([right, right], [bottom, top], color=neumann, linewidth=line_width)

    interface_style = {
        "marker": "o",
        "markersize": 10,
        "markerfacecolor": "white",
        "markeredgecolor": "#687078",
        "markeredgewidth": 2,
    }
    ax.plot(left, top, **interface_style)
    ax.plot(right, bottom, **interface_style)

    normal = FancyArrowPatch(
        (right, 0.50),
        (0.91, 0.50),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=2.2,
        color="#40464b",
    )
    ax.add_patch(normal)

    text_style = {"ha": "center", "va": "center"}
    ax.text(0.49, 0.50, r"$\Omega$", fontsize=34, color="#4b5359", **text_style)
    ax.text(
        0.49,
        0.90,
        r"$k\nabla u\cdot\mathbf{n}=h$ on $\Gamma_N$",
        fontsize=15,
        color="#b65e18",
        **text_style,
    )
    ax.text(
        0.49,
        0.08,
        r"$u=g$ on $\Gamma_D$",
        fontsize=15,
        color="#1f5f96",
        **text_style,
    )
    ax.text(0.12, 0.50, r"$\Gamma_D$", fontsize=19, color="#1f5f96", **text_style)
    ax.text(0.49, 0.82, r"$\Gamma_N$", fontsize=19, color="#b65e18", **text_style)
    ax.text(
        0.925,
        0.50,
        r"$\mathbf{n}$",
        ha="left",
        va="center",
        fontsize=17,
        color="#40464b",
    )

    save_figure(fig, "diffusion-boundary-partition")


if __name__ == "__main__":
    make_formulation_process()
    make_boundary_partition()
