"""Plot the exact traveling pulse in the first transient lecture."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update(
    {"font.size": 13, "axes.labelsize": 14, "legend.fontsize": 11,
     "lines.linewidth": 2, "savefig.bbox": "tight",
     "mathtext.fontset": "cm", "font.family": "DejaVu Sans"}
)


def wave_pulse(s):
    return np.maximum(1 - 100*(s - 0.25)**2, 0)**3


x = np.linspace(0, 1, 501)
fig, ax = plt.subplots(figsize=(9.5, 3.4), layout="constrained")
for time in (0, 0.2, 0.4, 0.6):
    ax.plot(x, wave_pulse(x-time), label=rf"$t={time:g}$")
ax.set(xlabel=r"$x$", ylabel=r"Displacement $u_{\mathrm{exact}}$",
       xlim=(0, 1), ylim=(0, 1.08))
ax.tick_params(labelsize=14)
ax.xaxis.label.set_size(16)
ax.yaxis.label.set_size(16)
ax.grid(alpha=0.2)
fig.legend(*ax.get_legend_handles_labels(),
           loc="outside upper center", ncols=4, fontsize=14)
fig.savefig(Path(__file__).resolve().parent / "exact_wave.pdf")
plt.close(fig)
