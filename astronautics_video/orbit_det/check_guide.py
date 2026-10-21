"""Every number in guide.tex, computed and asserted. Run: python3 check_guide.py"""
import numpy as np
from orbit3d import C1, C3, cpn, rv_perifocal, MU

d, deg = np.radians, np.degrees
RE, J2 = 6378.137, 1.08263e-3
DAY = 86400.0


def close(x, want, tol):
    assert abs(x - want) <= tol, (x, want)
    return x


# ---- the practice orbit (designed as a = 12,000 km, e = 0.2, i = 50, Omega = 230, omega = 300, theta0 = 75)
r0 = np.array([-5404.7, -9275.9, 2171.6])
v0 = np.array([3.4111, -2.2048, 4.8031])

# 4.1  a, h, e
r, v = np.linalg.norm(r0), np.linalg.norm(v0)
E = v * v / 2 - MU / r
a = -MU / (2 * E)
h = np.cross(r0, v0)
hn = np.linalg.norm(h)
vxh = np.cross(v0, h) / MU
ev = vxh - r0 / r
e = np.linalg.norm(ev)
print("4.1  r0 = %.1f  v0 = %.4f  v^2/2 = %.4f  mu/r = %.4f  E = %.4f  a = %.1f" % (r, v, v * v / 2, MU / r, E, a))
print("     h terms x: %.1f %.1f  y: %.1f %.1f  z: %.1f %.1f" % (
    r0[1] * v0[2], r0[2] * v0[1], r0[2] * v0[0], r0[0] * v0[2], r0[0] * v0[1], r0[1] * v0[0]))
print("     h = (%.0f, %.0f, %.0f)  |h| = %.0f" % (*h, hn))
print("     v x h / mu = (%.4f, %.4f, %.4f)  r/r = (%.4f, %.4f, %.4f)" % (*vxh, *(r0 / r)))
print("     e vec = (%.4f, %.4f, %.4f)  e = %.4f  check sqrt(1+2Eh^2/mu^2) = %.4f" % (
    *ev, e, np.sqrt(1 + 2 * E * hn ** 2 / MU ** 2)))
print("     rp = %.0f  ra = %.0f  perigee alt = %.0f  T = %.2f h" % (
    a * (1 - e), a * (1 + e), a * (1 - e) - RE, 2 * np.pi * np.sqrt(a ** 3 / MU) / 3600))
close(r, 10953.0, 0.1); close(v, 6.2902, 1e-4); close(a, 12000, 1); close(hn, 67763, 1); close(e, 0.2000, 1e-4)

# 4.2  the frame, C_PN, i, Omega, omega
p = ev / e
hh = h / hn
q = np.cross(hh, p)
C = np.vstack([p, q, hh])
i = deg(np.arccos(C[2, 2]))
Om = deg(np.arctan2(C[2, 0], -C[2, 1])) % 360
w = deg(np.arctan2(C[0, 2], C[1, 2])) % 360
print("4.2  p = (%.4f, %.4f, %.4f)  hhat = (%.4f, %.4f, %.4f)  q = (%.4f, %.4f, %.4f)" % (*p, *hh, *q))
print("     i = acos(%.4f) = %.2f" % (C[2, 2], i))
print("     Omega = atan2(%.4f, %.4f) = %.2f  (raw %.2f)" % (C[2, 0], -C[2, 1], Om, deg(np.arctan2(C[2, 0], -C[2, 1]))))
print("     omega = atan2(%.4f, %.4f) = %.2f  (raw %.2f)" % (C[0, 2], C[1, 2], w, deg(np.arctan2(C[0, 2], C[1, 2]))))
n = np.cross([0, 0, 1], h)
nn = np.linalg.norm(n)
print("     node vector n = (%.0f, %.0f, 0)  |n| = %.0f  cos Om = %.4f -> acos %.2f, n_Y < 0 so %.2f" % (
    n[0], n[1], nn, n[0] / nn, deg(np.arccos(n[0] / nn)), 360 - deg(np.arccos(n[0] / nn))))
cw = n @ ev / (nn * e)
print("     n.e = %.1f  cos omega = %.4f -> acos %.2f, e_Z = %.4f < 0 so %.2f" % (
    n @ ev, cw, deg(np.arccos(cw)), ev[2], 360 - deg(np.arccos(cw))))
close(i, 50.0, 0.02); close(Om, 230.0, 0.02); close(w, 300.0, 0.05)
assert n[1] < 0 and ev[2] < 0

# 4.3  theta0
c0 = ev @ r0 / (e * r)
rv = r0 @ v0
th = deg(np.arccos(c0))
print("4.3  e.r0 terms %.1f %.1f %.1f = %.1f  e r0 = %.1f  cos th = %.4f -> %.2f ; r.v terms %.1f %.1f %.1f = %.1f" % (
    *(ev * r0), ev @ r0, e * r, c0, th, *(r0 * v0), rv))
assert rv > 0
close(th, 75.0, 0.05)

# 5.1  back from the rounded elements a = 12,000, e = 0.2, i = 50, Omega = 230, omega = 300, theta = 75
A, Ee, I, OM, W, TH = 12000.0, 0.2, 50.0, 230.0, 300.0, 75.0
pp = A * (1 - Ee ** 2)
hp = np.sqrt(MU * pp)
rr = pp / (1 + Ee * np.cos(d(TH)))
rP, vP = rv_perifocal(A, Ee, d(TH))
CC = cpn(d(OM), d(I), d(W))
print("5.1  p = %.0f  h = %.0f  r = %.1f  rP = (%.1f, %.1f, 0)  mu/h = %.4f  vP = (%.4f, %.4f, 0)" % (
    pp, hp, rr, rP[0], rP[1], MU / hp, vP[0], vP[1]))
print("     C3(Om) =", np.round(C3(d(OM)), 4).tolist())
print("     C1(i)  =", np.round(C1(d(I)), 4).tolist())
print("     C3(w)  =", np.round(C3(d(W)), 4).tolist())
print("     C_PN   =", np.round(CC, 4).tolist())
assert np.allclose(np.round(CC, 4), np.round(C, 4), atol=2e-4)
rN, vN = CC.T @ rP, CC.T @ vP
print("     rN = (%.1f, %.1f, %.1f)  vN = (%.4f, %.4f, %.4f)" % (*rN, *vN))
assert np.allclose(rN, r0, atol=0.6) and np.allclose(vN, v0, atol=2e-4)

# 6.1  node drift for the practice orbit, and a sun-synchronous orbit at 600 km
nm = np.sqrt(MU / A ** 3)
k = 3 * nm * J2 * RE ** 2 / (2 * A ** 2 * (1 - Ee ** 2) ** 2)
Omd = -k * np.cos(d(I)) * deg(1) * DAY
print("6.1  n = %.4e rad/s  k = %.4e rad/s  Omega dot = %.3f deg/day" % (nm, k, Omd))
close(Omd, -0.761, 0.001)
a6 = RE + 600
n6 = np.sqrt(MU / a6 ** 3)
k6 = 3 * n6 * J2 * RE ** 2 / (2 * a6 ** 2)
want = d(360 / 365.2422) / DAY
ci = -want / k6
print("     600 km: n = %.4e  k = %.4e rad/s = %.3f deg/day  want %.4f deg/day  cos i = %.4f  i = %.2f" % (
    n6, k6, deg(k6) * DAY, 360 / 365.2422, ci, deg(np.arccos(ci))))
close(deg(np.arccos(ci)), 97.79, 0.02)

# 6.2  critical inclination, and omega dot for the practice orbit
ic = deg(np.arcsin(np.sqrt(0.8)))
print("6.2  sin i = %.4f  i = %.2f or %.2f" % (np.sqrt(0.8), ic, 180 - ic))
br = 2.5 * np.sin(d(I)) ** 2 - 2
wd = -k * br * deg(1) * DAY
print("     bracket = %.4f  omega dot = %.3f deg/day" % (br, wd))
close(ic, 63.43, 0.005); assert br < 0 and wd > 0
print("all guide numbers check out")
