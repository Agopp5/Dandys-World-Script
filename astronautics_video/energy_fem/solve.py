"""Every number in the energy-methods / FEM lesson, derived and asserted. Run: python3 solve.py"""
import numpy as np
import sympy as sp

# ---- Ep 1: one spring, K = 20 N/mm, F = 100 N
K, F = 20, 100
q = sp.symbols("q")
Pi = sp.Rational(1, 2) * K * q**2 - F * q
qs = sp.solve(sp.diff(Pi, q), q)[0]
assert qs == 5 and Pi.subs(q, 5) == -250
U, W = sp.Rational(1, 2) * K * 25, F * 5
assert (U, W) == (250, 500)                         # Pi = U - W = -250; U is half of W at equilibrium
assert [Pi.subs(q, v) for v in (0, 3, 5, 7, 10)] == [0, -210, -250, -210, 0]

# ---- Ep 2: two springs in series, k1 = 40, k2 = 20 N/mm, F1 = 40, F2 = 20 N
k1, k2, F1, F2 = 40, 20, 40, 20
Kg = np.array([[k1 + k2, -k2], [-k2, k2]], float)
q12 = np.linalg.solve(Kg, [F1, F2])
assert np.allclose(q12, [1.5, 2.5])
# Newton check: spring 1 carries F1 + F2 = 60 N -> stretch 1.5; spring 2 carries 20 N -> stretch 1.0
assert np.isclose(k1 * 1.5, 60) and np.isclose(k2 * 1.0, 20)

# slide 4-spring sample (k1, two k2 in parallel, k3), loads only F2, F4: symbolic matrix check
a1, a2, a3, Q1, Q2, Q3, Q4 = sp.symbols("k1 k2 k3 q1 q2 q3 q4")
P1, P2, P3, P4 = sp.symbols("P1 P2 P3 P4")
Ue = (a1 * (Q2 - Q1)**2 + 2 * a2 * (Q3 - Q2)**2 + a3 * (Q4 - Q3)**2) / 2
Pi4 = Ue - (P1 * Q1 + P2 * Q2 + P3 * Q3 + P4 * Q4)
M = sp.Matrix([[sp.diff(Pi4, v, w) for w in (Q1, Q2, Q3, Q4)] for v in (Q1, Q2, Q3, Q4)])
assert M == sp.Matrix([[a1, -a1, 0, 0], [-a1, a1 + 2 * a2, -2 * a2, 0],
                       [0, -2 * a2, 2 * a2 + a3, -a3], [0, 0, -a3, a3]])

# ---- Ep 3: HW P1. Wall-K1-bar(q2); wall-K2-node(q1)-K2-bar; bar-K3-node(q3).
# Assumptions (stated in the video): the unlabeled spring between q1 and the bar is a second K2;
# the vertical bar is rigid and translates, so everything attached to it moves q2.
K1, K2, K3 = sp.symbols("K1 K2 K3", positive=True)
q1, q2, q3 = sp.symbols("q1 q2 q3")
U1 = (K1 * q2**2 + K2 * q1**2 + K2 * (q2 - q1)**2 + K3 * (q3 - q2)**2) / 2
PiH = U1 - (P1 * q1 + (P2 + P3) * q2 + P4 * q3)
eqs = [sp.diff(PiH, v) for v in (q1, q2, q3)]
sol = sp.solve(eqs, (q1, q2, q3), dict=True)[0]
Ptot = P1 + 2 * (P2 + P3 + P4)
assert sp.simplify(sol[q2] - Ptot / (2 * K1 + K2)) == 0
assert sp.simplify(sol[q1] - (P1 + K2 * sol[q2]) / (2 * K2)) == 0
assert sp.simplify(sol[q1] - ((K1 + K2) * P1 + K2 * (P2 + P3 + P4)) / (K2 * (2 * K1 + K2))) == 0
assert sp.simplify(sol[q3] - (sol[q2] + P4 / K3)) == 0
assert sp.simplify(sp.Matrix(3, 3, lambda i, j: sp.diff(eqs[i], (q1, q2, q3)[j]))
                   - sp.Matrix([[2 * K2, -K2, 0], [-K2, K1 + K2 + K3, -K3], [0, -K3, K3]])) == sp.zeros(3)
# numeric sanity case: all K = 100 N/mm, all P = 30 N  -> q2 = 210/300 = 0.7, q1 = 0.5, q3 = 1.0
nums = {K1: 100, K2: 100, K3: 100, P1: 30, P2: 30, P3: 30, P4: 30}
assert [sol[v].subs(nums) for v in (q1, q2, q3)] == [sp.Rational(1, 2), sp.Rational(7, 10), 1]
print("HW P1:", {k: sp.factor(v) for k, v in sol.items()})

# ---- Ep 4: bar strain energy; Rayleigh-Ritz
# (a) bar with uniform f, assumed u = a x: tip exact, interior not
x, L, EA, f, a = sp.symbols("x L EA f a", positive=True)
Ub = sp.integrate(EA * sp.diff(a * x, x)**2 / 2, (x, 0, L))
Wb = sp.integrate(f * a * x, (x, 0, L))
asol = sp.solve(sp.diff(Ub - Wb, a), a)[0]
assert sp.simplify(asol - f * L / (2 * EA)) == 0
uex = f / EA * (L * x - x**2 / 2)
assert sp.simplify(uex.subs(x, L) - asol * L) == 0                     # tip: exact
assert sp.simplify(uex.subs(x, L / 2) - 3 * f * L**2 / (8 * EA)) == 0   # middle exact 3/8 vs assumed 1/4
assert sp.simplify(asol * L / 2 - f * L**2 / (4 * EA)) == 0
# (b) slide beam: v = vB sin(pi z / L)
z, EI, Wl, vB = sp.symbols("z EI W v_B", positive=True)
Ubm = sp.integrate(EI / 2 * sp.diff(vB * sp.sin(sp.pi * z / L), z, 2)**2, (z, 0, L))
assert sp.simplify(Ubm - sp.pi**4 * EI * vB**2 / (4 * L**3)) == 0
vs = sp.solve(sp.diff(Ubm - Wl * vB, vB), vB)[0]
assert sp.simplify(vs - 2 * Wl * L**3 / (sp.pi**4 * EI)) == 0
assert np.isclose(2 / np.pi**4, 0.020532, atol=1e-6) and np.isclose(1 / 48, 0.020833, atol=1e-6)
print(f"beam: 2/pi^4 = {2/np.pi**4:.5f}  1/48 = {1/48:.5f}  error {100*(1-48*2/np.pi**4):.2f}%")
assert np.isclose(100 * (1 - 96 / np.pi**4), 1.45, atol=0.01)

# ---- Ep 5: one element. N1 = 1 - s, N2 = s; k = EA/l [1 -1; -1 1]; uniform f = c: Q = cl/2 each
s, l, c, u1, u2 = sp.symbols("s l c u1 u2")
us = (1 - s) * u1 + s * u2
dudx = sp.diff(us, s) / l
Ue_ = sp.integrate(EA / 2 * dudx**2 * l, (s, 0, 1))
Ke = sp.Matrix(2, 2, lambda i, j: sp.diff(Ue_, (u1, u2)[i], (u1, u2)[j]))
assert sp.simplify(Ke - EA / l * sp.Matrix([[1, -1], [-1, 1]])) == sp.zeros(2)
Qe = [sp.integrate(c * Ni * l, (s, 0, 1)) for Ni in (1 - s, s)]
assert Qe == [c * l / 2, c * l / 2]
# numeric element used on screen: EA = 2e6 N, l = 500 mm -> k = 4000 N/mm
assert 2e6 / 500 == 4000

# ---- Ep 6: column under its own weight, 3 equal elements (slides). Exact u = rho g/E (x^2/2 - L x)
Kc = 3 * np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1]], float)        # EA/l with l = L/3, EA = L = 1
Fc = -(1 / 3) / 2 * np.array([2, 2, 1])                                # c = -rho g A, cl/2 per node; rho g A = 1
qc = np.linalg.solve(Kc, Fc)                                           # in units of rho g L^2 / E
assert np.allclose(qc * 2, [-5 / 9, -8 / 9, -1])                       # q = rho g L^2/(2E) * (-5/9, -8/9, -1)
ex = lambda X: X**2 / 2 - X                                            # exact u in units rho g L^2 / E
assert np.allclose([ex(1 / 3), ex(2 / 3), ex(1)], qc)                 # nodes exact (this case)
sig = 3 * np.diff(np.r_[0, qc])                                        # sigma = E (q_b - q_a)/l, units rho g L
assert np.allclose(sig, [-5 / 6, -1 / 2, -1 / 6])
assert np.allclose([-(1 - m) for m in (1 / 6, 1 / 2, 5 / 6)], sig)   # exact at element centres
# middle-of-element-1 displacement: FEM linear interp vs exact
assert np.isclose(qc[0] / 2, -5 / 36) and np.isclose(ex(1 / 6), -11 / 72)
# reaction from the deleted row: EA/l (q1 - q2) = cl/2 + R  -> R = rho g A L (holds the whole weight)
R = 3 * (0 - qc[0]) + 1 / 6                                            # row 1 of the full 4x4: 3(q1 - q2) = -1/6 + R
assert np.isclose(R, 1.0)

# ---- Ep 7: generated example. Stepped aluminum bar + end spring.
# wall | element 1: A = 200 mm^2, l = 500 mm | node 1 (P = 7000 N) | element 2: A = 100, l = 500 | node 2 | spring K = 14000 N/mm | wall
E = 70000.0
ka, kb, Ks, P = E * 200 / 500, E * 100 / 500, 14000.0, 7000.0
assert (ka, kb) == (28000, 14000)
Kfull = np.array([[ka, -ka, 0, 0], [-ka, ka + kb, -kb, 0], [0, -kb, kb + Ks, -Ks], [0, 0, -Ks, Ks]])
Kr = Kfull[1:3, 1:3]
assert np.allclose(Kr, [[42000, -14000], [-14000, 28000]])
assert np.isclose(np.linalg.det(Kr), 9.8e8)
qq = np.linalg.solve(Kr, [P, 0])
assert np.allclose(qq, [0.2, 0.1])
R0 = Kfull[0] @ np.r_[0, qq, 0]
R3 = Kfull[3] @ np.r_[0, qq, 0]
assert np.isclose(R0, -5600) and np.isclose(R3, -1400) and np.isclose(R0 + R3 + P, 0)
s1, s2 = E * qq[0] / 500, E * (qq[1] - qq[0]) / 500
assert np.isclose(s1, 28) and np.isclose(s2, -14)
# Newton check: the node 1 load splits between a 28000 path and a series path (14000 + 14000 -> 7000)
assert np.isclose(P * 28000 / 35000, 5600) and np.isclose(P * 7000 / 35000, 1400)
print("Ep7 stepped bar: q =", qq, " reactions", R0, R3, " stresses", s1, s2)

# ---- Ep 8: HW P2. E = 10e3 psi, A = 2 in^2, L = 40 in; P1 = 50 lb at x = L/2 (node 1), P2 = 100 lb at the tip
# (node 2); f = 5 lb/in acting in -x over the whole length. Two elements of 20 in.
EA2, l2, fv = 10e3 * 2, 20.0, -5.0
k = EA2 / l2
assert k == 1000
Qn = fv * l2 / 2
assert Qn == -50
Kf = k * np.array([[1, -1, 0], [-1, 2, -1], [0, -1, 1]])
Ff = np.array([Qn, 2 * Qn + 50, Qn + 100])      # node 0 also gets R
assert np.allclose(Ff, [-50, -50, 50])
qh = np.linalg.solve(Kf[1:, 1:], Ff[1:])
assert np.allclose(qh, [0.0, 0.05])
Rh = Kf[0] @ np.r_[0, qh] - Ff[0]
assert np.isclose(Rh, 50)
# exact solution: internal force at x = the loads to its right: P2 + P1 [x < 20] + f (40 - x), f = -5; u' = N/EA
X = sp.symbols("X")
Nint = lambda xv: 100 + (50 if xv < 20 else 0) - 5 * (40 - xv)
assert Nint(0) == -50 and Nint(39.999) > 99.9
u_ex = lambda xv: sp.integrate((100 + 50 - 5 * (40 - X)), (X, 0, min(xv, 20))) / EA2 + \
    (sp.integrate(100 - 5 * (40 - X), (X, 20, xv)) / EA2 if xv > 20 else 0)
assert u_ex(20) == 0 and np.isclose(float(u_ex(40)), 0.05)
assert np.isclose(float(u_ex(10)), -0.0125)                  # point 3 (x = L/4): FEM interpolation gives 0
print("HW P2: q1, q2 =", qh, " R =", Rh, " exact u(L/4) =", float(u_ex(10)))
print("all lesson numbers check out")
