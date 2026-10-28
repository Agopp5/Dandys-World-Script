import numpy as np
def box(W, H, tt, tb, tl, tr, aL, aR):
    BL = aL + tt*W/6*3 + tl*H/6*1; BR = aR + tt*W/6*3 + tr*H/6*1
    P = {1: (0, H/2), 2: (W, H/2), 3: (W, -H/2), 4: (0, -H/2)}; B = {1: BL, 2: BR, 3: BR, 4: BL}
    Ixx = sum(B[k]*P[k][1]**2 for k in P)
    walls = [(1, 2, tt), (2, 3, tr), (3, 4, tb), (4, 1, tl)]
    qb = {}; q = 0
    for a, b, t in walls:
        if a != 1: q -= B[a]*P[a][1]/Ixx
        qb[(a, b)] = q
    L = lambda a, b: np.hypot(P[b][0]-P[a][0], P[b][1]-P[a][1])
    d = {(a, b): L(a, b)/t for a, b, t in walls}
    qs0 = -sum(qb[k]*d[k] for k in d)/sum(d.values())
    cr = lambda a, b: P[a][0]*P[b][1]-P[a][1]*P[b][0]
    xi = sum((qb[k]+qs0)*cr(*k) for k in qb)
    return BL, BR, Ixx, qb, d, qs0, xi
# practice box: 600 x 240, top/bottom 8 mm, left web 6 mm, right web 5 mm; angles left 50x50x6, right 40x30x5
aL = (50+50-6)*6; aR = (40+30-5)*5
BL, BR, Ixx, qb, d, qs0, xi = box(600, 240, 8, 8, 6, 5, aL, aR)
print("angles", aL, aR, "booms", BL, BR, "Ixx", Ixx)
print("qb x1e6", {k: round(v*1e6, 4) for k, v in qb.items()}, "delta", d, "qs0 x1e6", qs0*1e6, "xi", xi)
# check the HW P1 with the same function
print("HW P1 xi", box(500, 300, 10, 10, 10, 8, 1000, 656)[-1])

# practice two-cell: rectangular cells, T = 15 kNm counterclockwise
Gref = 27000.
H = 250.; WI, WII = 500., 600.
walls = {'left web': (H, 2.0, 27000), 'spar': (H, 2.5, 27000), 'right web': (H, 1.6, 27000),
         'skins I (each)': (WI, 1.0, 24000), 'skins II (each)': (WII, 0.8, 24000)}
dd = {k: L/(G/Gref*t) for k, (L, t, G) in walls.items()}
for k, (L, t, G) in walls.items(): print(f"  {k}: t*={G/Gref*t:.4f} delta={dd[k]:.2f}")
AI, AII = WI*H, WII*H
dI = dd['left web'] + 2*dd['skins I (each)'] + dd['spar']; dII = dd['right web'] + 2*dd['skins II (each)'] + dd['spar']; ds = dd['spar']
M = np.array([[dI/AI + ds/AII, -(ds/AI + dII/AII)], [2*AI, 2*AII]])
qI, qII = np.linalg.solve(M, [0, 15e6])
print("AI", AI, "AII", AII, "dI", dI, "dII", dII, "ds", ds)
print(f"qI={qI:.3f} qII={qII:.3f} spar={qI-qII:.3f} N/mm; Gref dth/dz={(qI*dI-qII*ds)/(2*AI):.6f}; theta' rad/mm={(qI*dI-qII*ds)/(2*AI)/Gref:.3e}")
for k, (L, t, G) in walls.items():
    q = qI if 'I ' in k or k == 'left web' else (qII if 'II' in k or k == 'right web' else qI-qII)
    print(f"   tau {k}: {q/t:.3f} N/mm^2")
