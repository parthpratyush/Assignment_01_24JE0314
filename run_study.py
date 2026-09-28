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
FIG_DIR = "figures"


def save_figure(name):
    os.makedirs(FIG_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, name), dpi=220)
    plt.close()


def main():
    direct = solve_direct(ETA_END)
    shooting = solve_shooting(ETA_END)
    rk = solve_rk4(ETA_END)
    props = integral_properties(rk["eta"], rk["fp"])

    print("\nWall-shear comparison")
    print("-" * 58)
    print(f"BVP collocation : {direct['wall_shear']:.9f}")
    print(f"IVP + Newton    : {shooting['wall_shear']:.9f}")
    print(f"RK4 + sensitivity: {rk['wall_shear']:.9f}")
    print(f"Reference        : {REFERENCE:.9f}")
    print(f"RK4 abs. error  : {abs(rk['wall_shear'] - REFERENCE):.3e}")

    print("\nBoundary-layer quantities from the RK4 solution")
    for name, value in props.items():
        print(f"{name:24s}: {value:.6f}")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    data = [
        ("f", r"$f(\eta)$", "Similarity streamfunction"),
        ("fp", r"$f'(\eta)$", "Dimensionless velocity"),
        ("fpp", r"$f''(\eta)$", "Dimensionless shear"),
    ]

    for ax, (key, ylabel, title) in zip(axes, data):
        ax.plot(direct["eta"], direct[key], label="BVP")
        ax.plot(shooting["eta"], shooting[key], "--", label="Shooting")
        ax.plot(rk["eta"], rk[key], ":", linewidth=2.2, label="RK4")
        ax.set_xlabel(r"$\eta$")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8)

    save_figure("solution_profiles.png")

    plt.figure(figsize=(6.3, 4.1))
    for history, label, marker in [
        (shooting["history"], "IVP shooting", "o"),
        (rk["history"], "RK4 shooting", "s"),
    ]:
        it = [row[0] for row in history]
        res = [abs(row[2]) for row in history]
        plt.semilogy(it, res, marker + "-", label=label)

    plt.xlabel("Newton iteration")
    plt.ylabel(r"$|f'(\eta_\infty)-1|$")
    plt.title("Residual reduction during shooting")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    save_figure("newton_residuals.png")

    ends = np.array([3.5, 4.5, 5.5, 6.5, 7.0, 8.0])
    values = [solve_direct(float(end))["wall_shear"] for end in ends]

    plt.figure(figsize=(6.3, 4.1))
    plt.plot(ends, values, "o-")
    plt.axhline(REFERENCE, linestyle="--", label="reference")
    plt.xlabel(r"$\eta_\infty$")
    plt.ylabel(r"$f''(0)$")
    plt.title("Effect of finite-domain truncation")
    plt.grid(alpha=0.3)
    plt.legend()
    save_figure("domain_study.png")

    steps = np.array([0.05, 0.025, 0.0125, 0.00625])
    estimates = [solve_rk4(ETA_END, step=float(h))["wall_shear"] for h in steps]
    fine = estimates[-1]
    errors = np.maximum(np.abs(np.array(estimates) - fine), 1e-13)

    plt.figure(figsize=(6.3, 4.1))
    plt.loglog(steps, errors, "^-", label="computed difference")
    guide = errors[1] * (steps / steps[1]) ** 4
    plt.loglog(steps, guide, "--", label=r"$O(h^4)$ guide")
    plt.xlabel("RK4 step size")
    plt.ylabel("Difference in $f''(0)$")
    plt.title("RK4 mesh refinement")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    save_figure("rk4_refinement.png")

    print("\nFigures saved in figures/.")


if __name__ == "__main__":
    main()
