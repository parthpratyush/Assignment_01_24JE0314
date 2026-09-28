# Assignment 01 — Stagnation-Point Boundary Layer

**Student:** Pratyush Singh Parmar
**Roll No.:** 24JE0314

This repository contains an independent numerical study of the Hiemenz/Falkner–Skan stagnation-point boundary-layer equation.

## Problem

Solve

`f''' + f f'' - (f')^2 + 1 = 0`

with

`f(0) = 0`, `f'(0) = 0`, `f'(eta_inf) = 1`.

The semi-infinite domain is truncated at `eta_inf = 7`.

## Structure

- `run_study.py` — runs the numerical study and creates plots
- `methods/direct_bvp.py` — direct boundary-value solution
- `methods/shooting.py` — IVP shooting with Newton correction
- `methods/rk4_shoot.py` — fixed-step RK4 with sensitivity equation
- `report/report.md` — technical report
- `figures/` — generated plots

## Setup

```bash
pip install -r requirements.txt
python run_study.py
```
