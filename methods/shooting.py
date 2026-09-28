import time
import numpy as np
from scipy.integrate import solve_ivp


def ode(_, y):
    f, fp, fpp = y
    return np.array((fp, fpp, fp**2 - f * fpp - 1.0))


def integrate(s, eta_end, points=650):
    grid = np.linspace(0.0, eta_end, points)
    sol = solve_ivp(
        ode,
        (0.0, eta_end),
        (0.0, 0.0, s),
        t_eval=grid,
        rtol=2e-9,
        atol=2e-11,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol


def solve_shooting(eta_end=7.0, initial_slope=1.15,
                   derivative_step=2e-4, tolerance=2e-8, max_iter=20):
    s = float(initial_slope)
    history = []
    start = time.perf_counter()

    for iteration in range(1, max_iter + 1):
        base = integrate(s, eta_end)
        shifted = integrate(s + derivative_step, eta_end)

        residual = float(base.y[1, -1] - 1.0)
        derivative = float(
            (shifted.y[1, -1] - base.y[1, -1]) / derivative_step
        )
        correction = residual / derivative
        history.append((iteration, s, residual))

        if abs(residual) < tolerance:
            break

        s -= correction
    else:
        raise RuntimeError("Newton shooting did not converge.")

    elapsed = time.perf_counter() - start

    return {
        "eta": base.t,
        "f": base.y[0],
        "fp": base.y[1],
        "fpp": base.y[2],
        "wall_shear": s,
        "iterations": iteration,
        "history": history,
        "seconds": elapsed,
    }
