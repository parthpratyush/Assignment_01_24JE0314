import time
import numpy as np


def augmented_rhs(state):
    f, fp, fpp, a, b, c = state
    fppp = fp * fp - f * fpp - 1.0
    c_prime = 2.0 * fp * b - fpp * a - f * c
    return np.array((fp, fpp, fppp, b, c, c_prime))


def rk4_path(s, eta_end, step):
    n = int(round(eta_end / step))
    h = eta_end / n
    eta = np.linspace(0.0, eta_end, n + 1)
    states = np.empty((6, n + 1))
    states[:, 0] = (0.0, 0.0, s, 0.0, 0.0, 1.0)

    for i in range(n):
        w = states[:, i]
        k1 = augmented_rhs(w)
        k2 = augmented_rhs(w + 0.5 * h * k1)
        k3 = augmented_rhs(w + 0.5 * h * k2)
        k4 = augmented_rhs(w + h * k3)
        states[:, i + 1] = w + (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

    return eta, states


def solve_rk4(eta_end=7.0, step=0.0125,
              initial_slope=1.15, tolerance=2e-9, max_iter=20):
    s = float(initial_slope)
    history = []
    start = time.perf_counter()

    for iteration in range(1, max_iter + 1):
        eta, state = rk4_path(s, eta_end, step)
        residual = float(state[1, -1] - 1.0)
        sensitivity = float(state[4, -1])
        correction = residual / sensitivity
        history.append((iteration, s, residual))

        if abs(residual) < tolerance:
            break

        s -= correction
    else:
        raise RuntimeError("RK4 shooting did not converge.")

    elapsed = time.perf_counter() - start

    return {
        "eta": eta,
        "f": state[0],
        "fp": state[1],
        "fpp": state[2],
        "wall_shear": s,
        "iterations": iteration,
        "history": history,
        "seconds": elapsed,
        "step": step,
    }


def trapezoid(x, y):
    return float(np.trapezoid(y, x))


def integral_properties(eta, fp):
    deficit = 1.0 - fp
    displacement = trapezoid(eta, deficit)
    momentum = trapezoid(eta, fp * deficit)
    shape = displacement / momentum

    crossing = np.searchsorted(fp, 0.99)
    if 0 < crossing < len(eta):
        x0, x1 = eta[crossing - 1], eta[crossing]
        y0, y1 = fp[crossing - 1], fp[crossing]
        delta99 = x0 + (0.99 - y0) * (x1 - x0) / (y1 - y0)
    else:
        delta99 = np.nan

    return {
        "delta_99": float(delta99),
        "displacement_thickness": displacement,
        "momentum_thickness": momentum,
        "shape_factor": float(shape),
    }
