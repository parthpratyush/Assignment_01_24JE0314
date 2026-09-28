import time
import numpy as np
from scipy.integrate import solve_bvp


def rhs(eta, y):
    f, fp, fpp = y
    return np.vstack((fp, fpp, fp**2 - f * fpp - 1.0))


def bc(left, right):
    return np.array((left[0], left[1], right[1] - 1.0))


def solve_direct(eta_end=7.0, mesh_points=80, tol=2e-8):
    mesh = np.linspace(0.0, eta_end, mesh_points)

    guess = np.empty((3, mesh.size))
    guess[0] = np.log(np.cosh(mesh))
    guess[1] = np.tanh(mesh)
    guess[2] = 1.0 / np.cosh(mesh) ** 2

    start = time.perf_counter()
    sol = solve_bvp(rhs, bc, mesh, guess, tol=tol, max_nodes=20000)
    elapsed = time.perf_counter() - start

    if not sol.success:
        raise RuntimeError(sol.message)

    return {
        "eta": sol.x,
        "f": sol.y[0],
        "fp": sol.y[1],
        "fpp": sol.y[2],
        "wall_shear": float(sol.y[2, 0]),
        "mesh_size": len(sol.x),
        "seconds": elapsed,
    }
