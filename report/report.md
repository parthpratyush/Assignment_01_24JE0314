# Numerical Study of Stagnation-Point Boundary-Layer Flow

**Assignment 01 - Viscous Flow**  
**Student:** Pratyush Singh Parmar  
**Roll No.:** 24JE0314

## 1. Objective

The objective is to obtain the similarity solution for two-dimensional stagnation-point flow and verify it using several numerical formulations.

The governing equation is

$$
f''' + f f'' - (f')^2 + 1 = 0,
$$

with

$$
f(0)=0,qquad f'(0)=0,qquad f'(\infty)=1.
$$

For computation the infinite boundary is replaced by the finite endpoint \(\eta_\infty=7\).

## 2. Governing equation and first-order form

Define

$$
y_1=f,qquad y_2=f',qquad y_3=f''.
$$

Then

$$
y_1'=y_2,qquad
y_2'=y_3,qquad
y_3'=y_2^2-y_1y_3-1.
$$

The unknown wall parameter is \(s=f''(0)\).

## 3. Numerical methods

### 3.1 Direct BVP collocation

The complete boundary-value problem is solved with SciPy's collocation-based BVP solver. A smooth \(\tanh\)-type velocity profile provides the starting estimate.

### 3.2 IVP shooting with Newton correction

For a trial \(s\), the system is integrated from \(0\) to \(7\). The scalar residual is

$$
R(s)=f'(7;s)-1.
$$

Newton's method updates the wall-shear guess according to

$$
s_{k+1}=s_k-\frac{R(s_k)}{R'(s_k)}.
$$

The derivative \(R'(s)\) is approximated with a small forward perturbation.

### 3.3 Fixed-step RK4 with sensitivity

The third method uses a classical fourth-order RK scheme written explicitly in Python. A sensitivity system for \(\partial f/\partial s\), \(\partial f'/\partial s\), and \(\partial f''/\partial s\) is integrated simultaneously so that the Newton derivative is obtained from the same solution.

## 4. Boundary-layer quantities

The solution is also used to evaluate

$$
\delta^*=\int_0^{\eta_\infty}(1-f')\,d\eta,
$$

$$
\theta=\int_0^{\eta_\infty}f'(1-f')\,d\eta,
$$

and

$$
H=\frac{\delta^*}{\theta}.
$$

The 99-percent thickness \(\delta_{99}\) is obtained by interpolation at \(f'=0.99\).

## 5. Numerical results

| Method | \(f''(0)\) | Absolute error against 1.23258766 |
|---|---:|---:|
| Direct BVP | 1.232587656759 | 3.68e-9 |
| IVP + Newton | 1.232587656723 | 3.65e-9 |
| RK4 + sensitivity | 1.232587656595 | 3.59e-9 |

The RK4 solution gives:

- \(\delta_{99}=2.37946\)
- \(\delta^*=0.647917\)
- \(\theta=0.292328\)
- \(H=2.21641\)

### Solution profiles

![solution profiles](../figures/solution_profiles.svg)

### Newton convergence

![Newton convergence](../figures/newton_convergence.svg)

### Domain truncation

![domain truncation](../figures/domain_truncation.svg)

### RK4 refinement

![RK4 refinement](../figures/rk4_refinement.svg)

### Boundary-layer measures

![Boundary-layer measures](../figures/boundary_layer_measures.svg)

### Flow schematic

![Flow schematic](../figures/stagnation_flow_schematic.svg)

## 6. Discussion

The three formulations give essentially identical values of the wall-shear parameter. The direct BVP formulation avoids a shooting guess, whereas shooting exposes the unknown wall shear explicitly. The sensitivity-based RK4 implementation provides an independent check because both the integrator and Newton derivative are constructed directly.

The domain study shows the effect of replacing an infinite far-field condition by a finite endpoint. The RK4 refinement study checks the expected fourth-order trend of the fixed-step implementation.

## 7. Conclusion

The stagnation-point similarity problem was solved with three independently organized numerical approaches. The computed wall shear agrees with the accepted benchmark to the digits relevant for the present study, and the supplementary convergence studies provide consistency checks on the computational domain and RK4 step size.

## References

1. H. Schlichting and K. Gersten, *Boundary-Layer Theory*, Springer.
2. F. M. White, *Viscous Fluid Flow*, McGraw-Hill.
3. V. M. Falkner and S. W. Skan, “Some approximate solutions of the boundary layer equations,” *Philosophical Magazine*.
