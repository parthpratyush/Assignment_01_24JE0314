"""Generate submission-quality plots and a numerical results table."""

import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from methods.direct_bvp import solve_direct
from methods.shooting import solve_shooting
from methods.rk4_shoot import solve_rk4, integral_properties

ETA_END = 7.0
REFERENCE = 1.23258766
OUT_DIR = "figures"
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams.update({
    "font.size": 11,
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

direct = solve_direct(ETA_END)
shoot = solve_shooting(ETA_END)
rk = solve_rk4(ETA_END)
properties = integral_properties(rk["eta"], rk["fp"])


def save(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, name), dpi=220, bbox_inches="tight")
    plt.savefig(os.path.join(OUT_DIR, name.replace(".png", ".svg")), bbox_inches="tight")
    plt.close()


# 1. Similarity profiles.
fig, axes = plt.subplots(1, 3, figsize=(13, 4.1))
for ax, key, ylabel, title in zip(
    axes,
    ["f", "fp", "fpp"],
    [r"$f(\eta)$", r"$f'(\eta)$", r"$f''(\eta)$"],
    ["Similarity function", "Velocity profile", "Wall-normal shear"],
):
    ax.plot(direct["eta"], direct[key], label="Direct BVP", lw=2.0)
    ax.plot(shoot["eta"], shoot[key], "--", label="IVP shooting", lw=1.7)
    ax.plot(rk["eta"], rk[key], ":", label="RK4 shooting", lw=2.0)
    ax.set_xlabel(r"$\eta$")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
save("solution_profiles.png")

# 2. Newton convergence.
fig, ax = plt.subplots(figsize=(6.4, 4.2))
for history, label, marker in [
    (shoot["history"], "IVP shooting", "o"),
    (rk["history"], "RK4 shooting", "s"),
]:
    ax.semilogy(
        [row[0] for row in history],
        [abs(row[2]) for row in history],
        marker + "-",
        label=label,
    )
ax.axhline(2e-8, ls="--", label="tolerance")
ax.set_xlabel("Newton iteration")
ax.set_ylabel(r"$|R(s)|$")
ax.set_title("Newton-Raphson residual history")
ax.grid(True, which="both", alpha=0.25)
ax.legend()
save("newton_convergence.png")

# 3. Computational-domain sensitivity.
eta_ends = np.array([3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0, 8.0, 10.0])
wall_values = np.array(
    [solve_direct(float(value))["wall_shear"] for value in eta_ends]
)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot(eta_ends, wall_values, "o-", lw=1.8)
ax.axhline(REFERENCE, ls="--", label="reference")
ax.set_xlabel(r"$\eta_\infty$")
ax.set_ylabel(r"$f''(0)$")
ax.set_title("Domain truncation study")
ax.grid(alpha=0.25)
ax.legend()
save("domain_truncation.png")

# 4. RK4 refinement.
steps = np.array([0.1, 0.05, 0.025, 0.0125, 0.00625])
estimates = np.array(
    [solve_rk4(ETA_END, step=float(h))["wall_shear"] for h in steps]
)
errors = np.maximum(np.abs(estimates - estimates[-1]), 1e-14)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.loglog(steps, errors, "o-", label="computed difference")
guide = errors[1] * (steps / steps[1]) ** 4
ax.loglog(steps, guide, "--", label=r"$O(h^4)$ reference")
ax.invert_xaxis()
ax.set_xlabel("RK4 step size $h$")
ax.set_ylabel(r"Difference in $f''(0)$")
ax.set_title("RK4 refinement study")
ax.grid(True, which="both", alpha=0.25)
ax.legend()
save("rk4_refinement.png")

# 5. Wall-shear deviation.
fig, ax = plt.subplots(figsize=(7.2, 4.3))
names = ["BVP", "IVP + Newton", "RK4 + sensitivity"]
deviation = np.array([
    direct["wall_shear"],
    shoot["wall_shear"],
    rk["wall_shear"],
]) - REFERENCE
ax.bar(names, deviation)
ax.axhline(0, ls="--", lw=1)
ax.set_ylabel(r"$f''(0)$ - reference")
ax.set_title("Wall-shear deviation from reference")
ax.grid(axis="y", alpha=0.25)
save("wall_shear_error.png")

# 6. Boundary-layer measures.
fig, ax = plt.subplots(figsize=(7.4, 4.3))
labels = [r"$\delta_{99}$", r"$\delta^*$", r"$\theta$", "H"]
values = [
    properties["delta_99"],
    properties["displacement_thickness"],
    properties["momentum_thickness"],
    properties["shape_factor"],
]
ax.bar(labels, values)
ax.set_title("Boundary-layer integral measures")
ax.set_ylabel("Dimensionless value")
ax.grid(axis="y", alpha=0.25)
save("boundary_layer_measures.png")

# 7. Flow schematic.
x = np.linspace(-4, 4, 17)
y = np.linspace(0.05, 4, 9)
X, Y = np.meshgrid(x, y)
U = 0.75 * X
V = -0.75 * Y

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.streamplot(X, Y, U, V, density=1.1, linewidth=0.8, arrowsize=0.9)
ax.axhline(0, color="black", lw=3)
ax.scatter([0], [0], s=45, zorder=5)
ax.text(-3.8, 0.25, "solid wall")
ax.text(0.15, 0.25, "stagnation point")
ax.text(-3.8, 3.6, r"$U_e=ax$")
ax.set_xlim(-4, 4)
ax.set_ylim(0, 4)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Two-dimensional stagnation-point flow schematic")
ax.set_aspect("equal")
ax.grid(alpha=0.15)
save("stagnation_flow_schematic.png")

with open("results.csv", "w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["quantity", "value"])
    writer.writerow(["Direct BVP f''(0)", direct["wall_shear"]])
    writer.writerow(["IVP + Newton f''(0)", shoot["wall_shear"]])
    writer.writerow(["RK4 + sensitivity f''(0)", rk["wall_shear"]])
    writer.writerow(["Reference f''(0)", REFERENCE])
    for key, value in properties.items():
        writer.writerow([key, value])

print("Numerical study complete.")
print(f"Direct BVP       : {direct['wall_shear']:.12f}")
print(f"IVP + Newton     : {shoot['wall_shear']:.12f}")
print(f"RK4 + sensitivity: {rk['wall_shear']:.12f}")
print(f"delta_99         : {properties['delta_99']:.6f}")
print(f"delta_star       : {properties['displacement_thickness']:.6f}")
print(f"theta            : {properties['momentum_thickness']:.6f}")
print(f"H                : {properties['shape_factor']:.6f}")
