# Numerical Study of Stagnation-Point Boundary-Layer Flow

**Assignment 01 — Viscous Flow**

**Student:** Pratyush Singh Parmar

**Roll No.:** 24JE0314

## 1. Objective

The aim is to obtain the similarity solution for the two-dimensional stagnation-point boundary layer and compare several numerical formulations.

The governing equation is

[
f''' + f f'' - (f')^2 + 1 = 0,
]

with

[
f(0)=0,qquad f'(0)=0,qquad f'(infty)=1.
]

For computation, the infinite boundary is replaced by eta infinity equal to 7.

## 2. First-order system

With (y_1=f, y_2=f', y_3=f''),

[
y_1'=y_2,qquad y_2'=y_3,qquad
y_3'=y_2^2-y_1y_3-1.
]

The unknown wall parameter is (f''(0)).

## 3. Numerical methods

### Direct BVP collocation

The complete boundary-value problem is solved using SciPy's boundary-value solver, starting from a smooth hyperbolic-tangent velocity estimate.

### Newton shooting

For a trial value (s=f''(0)), the system is integrated as an IVP. The terminal residual is

[
R(s)=f'(7;s)-1.
]

Newton's method uses

[
s_{k+1}=s_k-rac{R(s_k)}{R'(s_k)},
]

with (R'(s)) estimated from a small forward perturbation.

### Fixed-step RK4 with sensitivity

A classical fourth-order Runge–Kutta integrator is written directly. A sensitivity system for the derivative with respect to the initial shear is integrated alongside the physical solution, giving the Newton derivative from the same trajectory.

## 4. Boundary-layer measures

The displacement and momentum thicknesses are computed from the velocity profile:

[
delta^*=int_0^{eta_infty}(1-f'),deta,
]

[
	heta=int_0^{eta_infty}f'(1-f'),deta.
]

The shape factor is (H=delta^*/	heta). The 99 percent thickness is found by interpolation at (f'=0.99).

## 5. Expected result

A converged numerical calculation gives a wall-shear parameter close to

[
f''(0)approx 1.23258766.
]

The generated figures provide checks using profile agreement, Newton residual reduction, finite-domain sensitivity, and RK4 refinement.

## 6. Discussion

The direct BVP formulation treats all boundary conditions together, while shooting turns the unknown wall shear into a scalar root-finding variable. The third formulation is useful as an independent implementation because the RK4 integrator and sensitivity equations are explicit.

The domain study shows the effect of replacing the infinite boundary by a finite computational endpoint. The RK4 refinement study provides a numerical check of fourth-order convergence.

## 7. Conclusion

The stagnation-point boundary-layer equation can be solved consistently using direct collocation and two shooting formulations. Agreement of the wall-shear parameter and velocity profiles provides a useful numerical verification.

## References

1. H. Schlichting and K. Gersten, *Boundary-Layer Theory*, Springer.
2. F. M. White, *Viscous Fluid Flow*, McGraw-Hill.
3. V. M. Falkner and S. W. Skan, “Some approximate solutions of the boundary layer equations,” *Philosophical Magazine*.
