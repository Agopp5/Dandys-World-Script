import numpy as np
np.set_printoptions(suppress=True, precision=4)
print("=== HW P1: idealize box, shear center ===")
aL = (60+50-10)*10; aR = (50+40-8)*8
BL = aL + 10*500/6*(2+1) + 10*300/6*(2-1)
BR = aR + 10*500/6*(2+1) + 8*300/6*(2-1)
print("angle areas", aL, aR, " booms left", BL, " right", BR)
P = {1: (0, 150), 2: (500, 150), 3: (500, -150), 4: (0, -150)}
B = {1: BL, 2: BR, 3: BR, 4: BL}
Ixx = sum(B[k]*P[k][1]**2 for k in P); print("Ixx", Ixx)
walls = [(1, 2, 10), (2, 3, 8), (3, 4, 10), (4, 1, 10)]
Sy = 1.0
qb = {}; q = 0.0
for (a, b, t) in walls:
    if a != 1: q = q - Sy/Ixx*B[a]*P[a][1]
    qb[(a, b)] = q
L = lambda a, b: np.hypot(P[b][0]-P[a][0], P[b][1]-P[a][1])
qs0 = -sum(qb[(a, b)]*L(a, b)/t for a, b, t in walls)/sum(L(a, b)/t for a, b, t in walls)
cr = lambda a, b: P[a][0]*P[b][1]-P[a][1]*P[b][0]
M = sum((qb[(a, b)]+qs0)*cr(a, b) for a, b, t in walls)
print("qb per unit Sy", {k: round(v*1e6, 4) for k, v in qb.items()}, "(x1e-6)")
print("qs0", qs0*1e6, "; total q", {k: round((v+qs0)*1e6, 4) for k, v in qb.items()})
print("xi (shear center from left web) =", M/Sy, "mm")
print("  delta per wall ds/t:", [L(a, b)/t for a, b, t in walls])

print("\n=== HW P2: two-cell torsion, different G ===")
Gref = 27600.
walls2 = {'16': (254, 1.625, 27600), '25': (406, 2.032, 27600), '34': (202, 1.220, 27600),
          '12': (647, .915, 24200), '56': (647, .915, 24200), '23': (775, .559, 24200), '45': (775, .559, 24200)}
d = {}
for k, (Lw, t, G) in walls2.items():
    ts = G/Gref*t; d[k] = Lw/ts; print(f"  wall {k}: t*={ts:.4f}  delta={d[k]:.1f}")
AI, AII = 232000., 258000.
dI = d['16']+d['12']+d['56']+d['25']; dII = d['23']+d['34']+d['45']+d['25']; d25 = d['25']
print(" dI", dI, " dII", dII, " d25", d25)
# twist equality: (qI dI - qII d25)/AI = (qII dII - qI d25)/AII ; torque T = 2AI qI + 2AII qII
A = np.array([[dI/AI + d25/AII, -(d25/AI + dII/AII)], [2*AI, 2*AII]])
sol = np.linalg.solve(A, [0, 1.0])  # per N.mm of torque
print(" per unit T (N.mm): qI", sol[0], " qII", sol[1], " ratio qI/qII", sol[0]/sol[1])
for T in (1e6, 10e6, 11.3e6):
    qI, qII = sol*T; print(f" T={T/1e6} kNm: qI={qI:.3f} qII={qII:.3f} q25={qI-qII:.3f} N/mm; dtheta/dz*Gref={(qI*dI-qII*d25)/(2*AI):.5f}")

print("\n=== slide check: 3-cell example ===")
Gr = 27600.
dd = {'12o': 1650/(24200/Gr*1.22), '12i': 508/(27600/Gr*2.03), '13': 775/(24200/Gr*1.22), '34': 380/(27600/Gr*1.63),
      '35': 508/(20700/Gr*.92), '56': 254/(20700/Gr*.92)}
print({k: round(v) for k, v in dd.items()})
A1, A2, A3 = 258000., 355000., 161000.
dI, d12i = dd['12o']+dd['12i'], dd['12i']; dII = dd['12i']+2*dd['13']+dd['34']; dIII = dd['34']+2*dd['35']+dd['56']
# unknowns qI qII qIII k(=Gref dtheta/dz)
M3 = np.array([[dI/(2*A1), -d12i/(2*A1), 0, -1], [-d12i/(2*A2), dII/(2*A2), -dd['34']/(2*A2), -1],
               [0, -dd['34']/(2*A3), dIII/(2*A3), -1], [2*A1, 2*A2, 2*A3, 0]])
print("q I,II,III, k =", np.linalg.solve(M3, [0, 0, 0, 11.3e6]))

print("\n=== slide check: channel with booms ===")
Ixx = 4*300*200**2; k = 4.8e3/Ixx
print("Ixx", Ixx, " q12", -k*300*200, " q23", -k*300*200-k*300*200, " q34", -2*k*300*200+k*300*200)
