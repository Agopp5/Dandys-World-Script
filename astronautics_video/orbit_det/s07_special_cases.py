"""S07: when an angle does not exist (BRIEF.md S07)."""
from orbit3d import *          # re-exports everything from mtk, plus the 3D orbit kit (Lato font set there)
import mtk.core as core
core.VOICE = "Achird"
core.STYLE = "patient, friendly tutor explaining to a student seeing this for the first time; warm and clear; unhurried, moderate pace, with a short pause after each sentence"
colors(**{r"\Omega": SKY, "i": EMBER, r"\omega": MINT, r"\theta": GOLD, r"\theta_0": GOLD, r"\vec h": LILAC,
          r"\hat h": LILAC, r"\vec e": ROSE, r"\hat p": ROSE, r"\hat q": LIME, r"\vec n": LIME, "u": GOLD})

D = np.pi / 180
VARPI_C, L_C = ROSE, ACCENT     # longitude of periapsis -> periapsis hue; true longitude -> accent

# ---- left: circular inclined orbit (generic Omega = 50, i = 40; omega undefined, so measure from the node)
A_C, OM_L, I_L, U_SAT = 2.4, 50 * D, 40 * D, 110 * D
CL = cpn(OM_L, I_L, 0.0)                  # rows: n-hat (as p-hat with omega = 0), in-plane 90 deg ahead, h-hat
N_HAT, Q_L, H_L = CL[0], CL[1], CL[2]
f_left = orbit(A_C, 0.0, OM_L, I_L, 0.0)  # theta here is measured from the node, so it is u
sat_L = f_left(U_SAT)
assert np.isclose(np.linalg.norm(sat_L), A_C)
assert np.isclose(np.dot(N_HAT, [0, 0, 1]), 0) and np.isclose(np.dot(N_HAT, [1, 0, 0]), np.cos(OM_L))
# the u arc ends on the satellite: angle from n-hat to the satellite equals u
assert np.isclose(np.arccos(np.dot(N_HAT, sat_L) / A_C), U_SAT)
assert np.isclose(np.dot(H_L, [0, 0, 1]), np.cos(I_L))

# ---- right: elliptical orbit in the equator (a = 2.4, e = 0.5), longitude of periapsis 60, satellite at theta 80
A_E, E_E, VARPI, TH_R = 2.4, 0.5, 60 * D, 80 * D
f_right = orbit(A_E, E_E, 0.0, 0.0, VARPI)
peri_R = f_right(0.0)
sat_R = f_right(TH_R)
assert np.isclose(np.linalg.norm(peri_R), A_E * (1 - E_E))
assert np.isclose(np.arctan2(peri_R[1], peri_R[0]), VARPI) and np.isclose(peri_R[2], 0)
assert np.isclose(np.arctan2(sat_R[1], sat_R[0]), VARPI + TH_R)       # true longitude l = varpi + theta = 140 deg
assert np.isclose(np.degrees(VARPI + TH_R), 140)


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


class S07_Special_Cases(VScene):
    budget = 120

    def construct(self):
        vL = View(elev=24, azim=-55, scale=1.0, center=(-3.6, .15))
        vR = View(elev=32, azim=30, scale=1.0, center=(3.6, .15))

        # left view
        gL = globe(vL)
        axL = axes3(vL, 2.7)
        eqL = curve(vL, lambda t: (1.25 * np.cos(t), 1.25 * np.sin(t), 0), 0, TAU, MUTED, width=2, R=1)
        orbL = curve(vL, f_left, 0, TAU, INK, width=4, R=1)
        nodeL = line3(vL, -2.9 * N_HAT, 2.9 * N_HAT, SKY, dashed=True)
        nodeDot = dot3(vL, A_C * N_HAT, SKY)
        satL = dot3(vL, sat_L, INK)
        titleL = T("circular, inclined", 28, INK2).move_to([-3.6, 3.65, 0])
        left = Group(eqL, gL, axL, orbL, nodeL, nodeDot, satL)

        # right view
        gR = globe(vR)
        axR = axes3(vR, 2.7)
        orbR = curve(vR, f_right, 0, TAU, INK, width=4, R=1)
        periDot = dot3(vR, peri_R, ROSE)
        satR = dot3(vR, sat_R, INK)
        titleR = T("elliptical, equatorial", 28, INK2).move_to([3.6, 3.65, 0])
        right = Group(gR, axR, orbR, periDot, satR)

        self.beat("Two kinds of orbit break these definitions.",
                  [FadeIn(left), FadeIn(titleL)], [FadeIn(right), FadeIn(titleR)], w=(.5, .5))

        # beat 2: argument of latitude on the left
        noP = T("no periapsis", 26, MUTED).move_to([-6.05, -2.75, 0])
        uArc = arc3(vL, H_L, N_HAT, U_SAT, 1.7, GOLD)
        mid = unit(np.cos(U_SAT / 2) * N_HAT + np.sin(U_SAT / 2) * Q_L)
        rL = line3(vL, (0, 0, 0), sat_L, INK2, dashed=True)
        uLab = label3(vL, "u", 2.05 * mid, GOLD, 36)
        uEq = E(r"u|=|\omega|+|\theta", size=52).move_to([-3.6, -2.75, 0])
        uArc.k.set_value(0)
        self.add(uArc)
        self.beat("A circular orbit has no periapsis, so little omega and theta have nothing to measure from. "
                  "Instead we use the argument of latitude, u, measured from the ascending node straight to "
                  "the satellite. For any orbit, u equals little omega plus theta.",
                  FadeIn(noP), [Indicate(nodeDot, color=SKY), Create(rL)], uArc.k.animate.set_value(1), FadeIn(uLab),
                  Write(uEq), w=(.2, .15, .25, .1, .3))

        # beat 3: longitude of periapsis on the right
        noN = T("no node", 26, MUTED).move_to([6.15, -2.75, 0])
        pDir = unit(peri_R)
        pLine = line3(vR, (0, 0, 0), 2.3 * pDir, ROSE, dashed=True)
        vArc = arc3(vR, (0, 0, 1), (1, 0, 0), VARPI, 1.35, VARPI_C)
        vmid = (np.cos(VARPI / 2), np.sin(VARPI / 2), 0)
        vLab = label3(vR, r"\varpi", 1.95 * np.array(vmid), VARPI_C, 36)
        vEq = E(r"\varpi|=|\Omega|+|\omega", size=52, cmap={r"\varpi": VARPI_C}).move_to([3.6, -2.75, 0])
        vArc.k.set_value(0)
        self.add(vArc)
        self.beat("An equatorial orbit never crosses the equator, so it has no ascending node, and capital "
                  "Omega is undefined. Then we use the longitude of periapsis, measured from I straight to the "
                  "periapsis. It equals capital Omega plus little omega.",
                  FadeIn(noN), Create(pLine), vArc.k.animate.set_value(1), FadeIn(vLab), Write(vEq),
                  w=(.25, .15, .25, .1, .25))

        # beat 4: true longitude, on both views
        omArc = arc3(vL, (0, 0, 1), (1, 0, 0), OM_L, 1.35, SKY)
        omLab = label3(vL, r"\Omega", 1.75 * np.array([np.cos(OM_L / 2), np.sin(OM_L / 2), 0]), SKY, 32)
        sDir = unit(sat_R)
        sLine = line3(vR, (0, 0, 0), 2.8 * sDir, MUTED, dashed=True)
        lArc = arc3(vR, (0, 0, 1), (1, 0, 0), VARPI + TH_R, 2.6, L_C)
        lmid = (np.cos(115 * D), np.sin(115 * D), 0)
        lLab = label3(vR, "l", 2.95 * np.array(lmid), L_C, 36)
        lEq = E(r"l|=|\Omega|+|\omega|+|\theta", size=52, cmap={"l": L_C}).move_to([0, -3.55, 0])
        lGlow = glow(lEq, L_C)
        omArc.k.set_value(0)
        lArc.k.set_value(0)
        self.add(omArc, lArc)
        self.beat("And the true longitude, capital Omega plus little omega plus theta, measures from I all the "
                  "way to the satellite. It always exists.",
                  Write(lEq), [omArc.k.animate.set_value(1), FadeIn(omLab), Create(sLine)],
                  [lArc.k.animate.set_value(1), FadeIn(lLab)], FadeIn(lGlow),
                  w=(.3, .25, .25, .2))

        # beat 5: the summary
        self.drop(left, right, titleL, titleR, noP, noN, rL, uArc, uLab, uEq, pLine, vArc, vLab, vEq,
                  omArc, omLab, sLine, lArc, lLab, lEq, lGlow)
        rows = VGroup(*[E(t, size=38) for t in (
            r"a|:\ \text{size}",
            r"e|:\ \text{shape}",
            r"i|:\ \text{tilt},\ 0\text{ to }180^\circ",
            r"\Omega|:\ \text{node},\ 0\text{ to }360^\circ",
            r"\omega|:\ \text{node to periapsis},\ 0\text{ to }360^\circ",
            r"\theta_0|:\ \text{periapsis to satellite},\ 0\text{ to }360^\circ")])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=.32)
        head = T("THE SIX ELEMENTS", 30, ACCENT, weight=BOLD)
        box = panel(VGroup(head, rows).arrange(DOWN, buff=.4), color=ACCENT)
        fit(box, 13, 7.2)
        box.move_to([0, 0, 0])
        self.beat("That's every orbital element and what it looks like.", FadeIn(box), .5)
        self.wipe()
