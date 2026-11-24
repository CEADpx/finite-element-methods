"""Plot one forward and backward Euler step for the transient lecture."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {"font.size": 15, "axes.labelsize": 16, "legend.fontsize": 13,
     "mathtext.fontset": "cm", "lines.linewidth": 2}
)

t_old, dt = 0.0, 0.5
t_new = t_old + dt
y_old = 1.0
time = np.linspace(0, 0.65, 301)
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7), layout="constrained")
for ax, method in zip(axes, ("Forward Euler", "Backward Euler")):
    if method == "Forward Euler":
        y_new = y_old - dt*y_old
        slope_label = r"Slope $f(t_n,y^n)=-1$"
        color = "#2166ac"
    else:
        y_new = y_old / (1+dt)
        slope_label = r"Slope $f(t_{n+1},y^{n+1})=-2/3$"
        color = "#b35806"
    ax.plot(time, np.exp(-time), color="black", label=r"Exact $y=e^{-t}$")
    ax.plot([t_old, t_new], [y_old, y_new], "o-", color=color,
            markersize=6, label=slope_label)
    ax.plot(t_new, np.exp(-t_new), "o", color="black", markersize=5)
    ax.axvline(t_new, color="0.7", linestyle=":", linewidth=1)
    ax.text(t_new+0.025, y_new, rf"$y^{{n+1}}={y_new:.3f}$",
            color=color, va="center", fontsize=15)
    ax.set(title=method, xlabel=r"$t$", ylabel=r"$y$",
           xlim=(-0.035, 0.77), ylim=(0.40, 1.10))
    ax.set_xticks([t_old, t_new], labels=[r"$t_n=0$", r"$t_{n+1}=0.5$"])
    ax.legend(loc="lower left", framealpha=0.95)
    ax.grid(alpha=0.15)

output = Path(__file__).resolve().parent / "euler_slopes.pdf"
fig.savefig(output, bbox_inches="tight")
plt.close(fig)
print(f"Forward Euler: {y_old-dt*y_old:.9f}")
print(f"Backward Euler: {y_old/(1+dt):.9f}")
print(f"Exact new value: {np.exp(-t_new):.9f}")
