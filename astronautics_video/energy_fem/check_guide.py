"""Every number in guide.tex, computed and asserted. Run: python3 check_guide.py"""
import numpy as np


def close(x, want, tol=1e-9):
    assert abs(x - want) <= tol, (x, want)
    return x


# 1.1  one spring, K = 20 N/mm, F = 100 N: Pi = 10 q^2 - 100 q, min at q = 5, Pi = -250
close(100 / 20, 5); close(10 * 25 - 100 * 5, -250)
# 2.1  k1 = 40, k2 = 20, F1 = 40, F2 = 20
q = np.linalg.solve([[60, -20], [-20, 20]], [40, 20]); assert np.allclose(q, [1.5, 2.5])
# 2.2  symbolic (row 3 = [0, -2k2, 2k2 + k3, -k3]); checked in solve.py
# 3.1  symbolic; 3.2  all K = 100, all P = 30
K = 100.; Pp = 30.
q2 = (Pp + 2 * 3 * Pp) / (2 * K + K); q1 = (Pp + K * q2) / (2 * K); q3 = q2 + Pp / K
assert np.allclose([q1, q2, q3], [0.5, 0.7, 1.0])
A = np.array([[2 * K, -K, 0], [-K, 3 * K, -K], [0, -K, K]]); assert np.allclose(A @ [q1, q2, q3], [Pp, 2 * Pp, Pp])
# 4.1  u = a x with a = fL/(2EA): u(L/2) = fL^2/(4EA); exact 3/8 fL^2/EA
close(0.5 / 2, 0.25); close(0.5 - 0.125, 0.375)
# 5.1  k = 70000 * 100 / 250
close(70000 * 100 / 250, 28000)
# 6.1  F = (cl/2) {1, 2, 2, 1} + {R, 0, 0, 0};  6.2  sigma_2 = -1/2 rho g L (solve.py)
# 7.1  stepped bar 4x4; 7.2  sigma_2 = 70000 (0.1 - 0.2)/500 = -14
close(70000 * (0.1 - 0.2) / 500, -14)
# 8.1  K = 1000 [[1,-1,0],[-1,2,-1],[0,-1,1]], F = {R - 50, -50, 50};  8.2  R = 50
q = np.linalg.solve(1000 * np.array([[2, -1], [-1, 1]]), [-50, 50]); assert np.allclose(q, [0, 0.05])
close(1000 * (0 - q[0]) + 50, 50)

# ---- After the video, practice A: wall - k1 - node 1 - k2 - node 2 - k3 - wall; F2 = 60 N at node 2 (to the right)
k1, k2, k3, F2 = 20., 20., 10., 60.
KA = np.array([[k1 + k2, -k2], [-k2, k2 + k3]])
qa = np.linalg.solve(KA, [0, F2]); assert np.allclose(qa, [1.5, 3.0]) and np.isclose(np.linalg.det(KA), 800)
RL, RR = -k1 * qa[0], -k3 * qa[1]                    # left wall pulls left 30 N, right wall pushes left 30 N
assert np.isclose(RL, -30) and np.isclose(RR, -30) and np.isclose(RL + RR + F2, 0)
PiA = 0.5 * k1 * qa[0]**2 + 0.5 * k2 * (qa[1] - qa[0])**2 + 0.5 * k3 * qa[1]**2 - F2 * qa[1]
assert np.isclose(PiA, -90)                          # = -(1/2) F . q

# ---- Practice B: steel bar, L = 1200 mm, A = 60 mm^2, E = 200 000 N/mm^2, fixed at x = 0, three elements of 400 mm,
# uniform f = 1.5 N/mm along +x, tip load P = 300 N along +x
E, Ab, L, f, P = 200000., 60., 1200., 1.5, 300.
l = L / 3; k = E * Ab / l; Q = f * l / 2
assert (k, Q) == (30000, 300)
KB = k * np.array([[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]])
FB = np.array([Q, 2 * Q, 2 * Q, Q + P])               # node 0 also gets R
assert np.allclose(FB, [300, 600, 600, 600])
qb = np.linalg.solve(KB[1:, 1:], FB[1:]); assert np.allclose(qb, [0.06, 0.10, 0.12])
R = KB[0] @ np.r_[0, qb] - FB[0]; assert np.isclose(R, -2100)  # = -(f L + P): the wall pulls left
sig = E * np.diff(np.r_[0, qb]) / l; assert np.allclose(sig, [30, 20, 10])
u_tip = P * L / (E * Ab) + f * L**2 / (2 * E * Ab); assert np.isclose(u_tip, 0.12)   # exact tip
u_ex = lambda x: (P * x + f * (L * x - x**2 / 2)) / (E * Ab)
assert np.allclose([u_ex(400), u_ex(800)], [0.06, 0.10])                            # nodes exact
print("practice A q =", qa, "R =", RL, RR, " practice B q =", qb, "sigma =", sig, "R =", R)
print("all guide numbers check out")
