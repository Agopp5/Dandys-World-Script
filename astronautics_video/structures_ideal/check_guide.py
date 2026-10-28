"""Every number in guide.tex, computed and asserted. Run: python3 check_guide.py"""
import numpy as np


def close(x, want, tol):
    assert abs(x - want) <= tol, (x, want)
    return x


# 1.1  web in bending
close(10 * 300 / 6 * (2 - 1), 500, 1e-9)
# 2.1  channel past booms 2, 3, 4
k = 4.8e3 / (4 * 300 * 200**2)
q12 = -k * 300 * 200; q23 = q12 - k * 300 * 200; q34 = q23 - k * 300 * (-200); q4 = q34 - k * 300 * (-200)
print("2.1", q12, q23, q34, q4); close(q23, -12, 1e-9); close(q34, -6, 1e-9); close(q4, 0, 1e-9)

# 3.1  practice box: 600 x 240; skins 8 mm; left web 6 mm; right web 5 mm; angles 50x50x6 (left), 40x30x5 (right)
W, H = 600, 240
aL, aR = (50 + 50 - 6) * 6, (40 + 30 - 5) * 5
sk, wl, wr = 8 * W / 6 * 3, 6 * H / 6 * 1, 5 * H / 6 * 1
BL, BR = aL + sk + wl, aR + sk + wr
Ixx = 2 * (BL + BR) * (H / 2) ** 2
qb23 = -BR * (H / 2) / Ixx
qb41 = BL * (H / 2) / Ixx
d = dict(top=W / 8, right=H / 5, bottom=W / 8, left=H / 6)
qs0 = -(qb23 * d['right'] + qb41 * d['left']) / sum(d.values())
q23, q41 = qb23 + qs0, qb41 + qs0
Fr, Fl = -q23 * H, q41 * H
couple = qs0 * W * H
xi = Fr * W - couple
print(f"3.1 angles {aL} {aR}; skin {sk}; webs {wl} {wr}; B {BL} {BR}; Ixx {Ixx:.4e}")
print(f"    qb23 {qb23*1e3:.4f}e-3  qb41 {qb41*1e3:.4f}e-3  ds/t {d}  sum {sum(d.values())}")
print(f"    terms {qb23*d['right']*1e3:.3f}e-3 {qb41*d['left']*1e3:.3f}e-3  qs0 {qs0*1e5:.3f}e-5")
print(f"    q23 {q23*1e3:.4f}e-3  q41 {q41*1e3:.4f}e-3  web forces {Fr:.4f} {Fl:.4f} (sum {Fr+Fl:.4f})")
print(f"    moment right web {Fr*W:.2f}  couple {couple:.2f}  xi {xi:.2f} mm")
assert (aL, aR, BL, BR) == (564, 325, 3204, 2925)
close(Ixx, 176.5152e6, 1); close(Fr + Fl, 1.0, 1e-9); close(xi, 276.3, 0.05)

# 4.1  symbolic (video reveals it); nothing to compute

# 5.1  practice two-cell: cell I 500 x 250, cell II 600 x 250, T = 15 kN m counterclockwise, G_REF = 27 000
Gr = 27000.
t_skin_I, t_skin_II = 24000 / Gr * 1.0, 24000 / Gr * 0.8
dl, ds, dr = 250 / 2.0, 250 / 2.5, 250 / 1.6
dsk1, dsk2 = 500 / t_skin_I, 600 / t_skin_II
dI, dII = dl + 2 * dsk1 + ds, dr + 2 * dsk2 + ds
AI, AII = 500 * 250., 600 * 250.
cI = AII * dI + AI * ds          # 150 000 (1350 qI - 100 qII) = 125 000 (-100 qI + 1943.75 qII)
cII = AI * dII + AII * ds
ratio = cII / cI
qII = 15e6 / (2 * AI * ratio + 2 * AII)
qI = ratio * qII
rate = (qI * dI - qII * ds) / (2 * AI)
rate2 = (-qI * ds + qII * dII) / (2 * AII)
print(f"5.1 t* skins {t_skin_I:.4f} {t_skin_II:.4f}; delta l {dl} s {ds} r {dr} skI {dsk1:.2f} skII {dsk2:.2f}; dI {dI:.2f} dII {dII:.2f}")
print(f"    coefs {cI:.4e} {cII:.4e} ratio {ratio:.5f}; torque coef {2*AI*ratio+2*AII:.1f}")
print(f"    qI {qI:.3f} qII {qII:.3f} spar {qI-qII:.3f}; Gref*rate {rate:.5f} = {rate2:.5f}; rate {rate/Gr:.4e} rad/mm = {np.degrees(rate/Gr)*1000:.4f} deg/m")
print(f"    tau: left {qI/2.0:.2f} skinsI {qI/1.0:.2f} spar {(qI-qII)/2.5:.2f} skinsII {qII/0.8:.2f} right {qII/1.6:.2f}")
close(qI, 30.0, 0.01); close(qII, 25.0, 0.01); close(rate, rate2, 1e-9)
print("all guide numbers check out")
